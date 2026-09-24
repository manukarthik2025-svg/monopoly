# Quest 21: React to every space type

## Why this quest
Right now landing on a space just logs its name. This quest makes every space type actually do something — the "resolve the space" step PLAN.md's phase list calls `RESOLVING_SPACE`.

## Your tasks

1. In `monopoly/rules.py`, write `resolve_space(state)` that looks at the current player's `position`, finds that `Space`, and branches on `space.space_type`.
2. `"GO"`, `"FREE_PARKING"`, `"JAIL"` (visiting, not sent there): do nothing beyond logging.
3. `"GO_TO_JAIL"`: call `send_to_jail` (from Quest 18) and end the turn immediately — no further action, no Go money even if crossed on the way conceptually (there's no "way," it's an instant teleport).
4. `"TAX"`: `pay(state, player, "BANK", space.price, "tax")`.
5. `"STREET"`, `"RAILROAD"`, `"UTILITY"`: if `space.owner is None`, set phase to `AWAITING_PURCHASE` (new phase — add it to your constants) so the UI can offer Buy/Auction (Quest 22). If owned by someone else and not mortgaged, calculate and pay rent (full rent logic comes in Quest 24 — for now, pay a placeholder flat rent equal to `space.price // 10` so the turn loop keeps working; you'll replace this placeholder in Quest 24). If owned by the current player, or mortgaged, do nothing.
6. `"CHANCE"`, `"COMMUNITY_CHEST"`: for now, just log "drew a card" — real card logic is Quest 27-28.
7. Call `resolve_space(state)` from `GameScreen.update()`'s `MOVING` branch, replacing the plain "landed on X" log, and only advance to `TURN_END` if `resolve_space` didn't set a different phase itself (like `AWAITING_PURCHASE`).

## Starter code
```python
AWAITING_PURCHASE = "AWAITING_PURCHASE"  # add this to your phase constants

def resolve_space(state):
    player = state.current_player()
    space = state.spaces[player.position]
    state.log(f"{player.name} landed on {space.name}")

    if space.space_type == "GO_TO_JAIL":
        send_to_jail(player, state.spaces)
        state.log(f"{player.name} is sent to jail")
        state.phase = TURN_END
        return

    if space.space_type == "TAX":
        # TODO: pay(state, player, "BANK", space.price, "tax"), then set phase to TURN_END
        pass

    elif space.is_property():
        if space.owner is None:
            state.phase = AWAITING_PURCHASE
            return
        elif space.owner != player.player_id and not space.mortgaged:
            placeholder_rent = space.price // 10
            # TODO: pay(state, player, owning_player, placeholder_rent, "rent"),
            # then set phase to TURN_END. You'll need to look up the owning
            # Player object from space.owner (a player_id) in state.players.
            pass
        else:
            state.phase = TURN_END

    else:
        state.phase = TURN_END
```

## Test it yourself
Add to `tests/test_spaces.py` (new file), constructing a small fake state with a `"TAX"` space and confirming `pay` was applied (check `player.cash` dropped by exactly the tax amount and phase became `TURN_END`). Then play manually: land on Income Tax and Luxury Tax and confirm cash drops correctly; land on Go To Jail and confirm you're teleported to jail with the turn ending immediately; land on an unowned property and confirm the phase becomes `AWAITING_PURCHASE` (nothing will happen yet in the UI until Quest 22 — that's expected).

## Checkpoint
```text
git commit -m "Resolve basic space actions: tax, jail, and property detection"
```
Every space on the board now has real behavior — the last piece missing is what to actually do about unowned and owned properties, which is next.

## Stuck? Try this
- Game gets stuck after landing on tax → confirm you're setting `state.phase = TURN_END` inside the `TAX` branch, not leaving it at `RESOLVING_SPACE` forever.
- `owner` lookup crashes → `space.owner` stores a `player_id` (an integer), not a `Player` object — you need something like `next(p for p in state.players if p.player_id == space.owner)`, or simpler, a loop with an `if`.
