# Quest 28: Make every card actually do something

## Why this quest
A drawn card is currently just text. This quest turns each `action` code from your JSON into real game effects, and wires card-drawing into `resolve_space`.

## Your tasks

1. Fill out `data/chance.json` and `data/community_chest.json` with the complete standard 16-card sets (look them up rather than guessing — accuracy matters for tests). Use these `action` names consistently: `MOVE_TO` (params: `target` index), `MOVE_TO_NEAREST` (params: `space_type`, either `"RAILROAD"` or `"UTILITY"`), `MOVE_BACK` (params: `spaces`), `RECEIVE` (params: `amount`), `PAY` (params: `amount`), `RECEIVE_FROM_EACH_PLAYER` (params: `amount`), `PAY_EACH_PLAYER` (params: `amount`), `GO_TO_JAIL`, `REPAIRS` (params: `per_house`, `per_hotel`), `KEEP_JAIL_CARD`.
2. In `monopoly/cards.py`, write `apply_card(card, player, state)` that branches on `card["action"]` and calls the matching rule from `rules.py` (movement cards should reuse `move_player`, and must correctly pay or skip Go money exactly like a normal move would).
3. `MOVE_TO_NEAREST` needs a small board search: from the player's current position, walk forward (wrapping with `%`) until you find a space whose `space_type` matches, then move there.
4. `REPAIRS` needs to count the current player's total houses and hotels across all their properties and multiply by the given per-house/per-hotel rates.
5. `KEEP_JAIL_CARD`: increment `player.jail_cards` and do NOT put this card back in the discard pile — it stays "in the player's hand" until used (Quest 26) or lost to bankruptcy (Quest 34). Track held-out cards in a new `GameState` list, e.g. `held_jail_cards` (a list of `(card, deck_name)` so you know which deck to return it to later).
6. In `resolve_space`, replace the placeholder `"CHANCE"`/`"COMMUNITY_CHEST"` branch with a real draw + apply.

## Starter code
```python
def apply_card(card, player, state):
    action = card["action"]

    if action == "MOVE_TO":
        old_position = player.position
        passed_go = player.position > card["target"] or (old_position == 0 and card["target"] != 0)
        player.position = card["target"]
        if passed_go and card["target"] != 0:
            pay(state, "BANK", player, 200, "passed Go")
        # Note: resolve whatever space they land on afterward too — call
        # resolve_space(state) again after this, since landing via a card
        # still means resolving that new space's action.

    elif action == "MOVE_TO_NEAREST":
        target_type = card["space_type"]
        position = player.position
        for _ in range(40):
            position = (position + 1) % 40
            if state.spaces[position].space_type == target_type:
                break
        # TODO: move the player to `position` the same way MOVE_TO does,
        # including passing Go if applicable

    elif action == "RECEIVE":
        pay(state, "BANK", player, card["amount"], card["text"])

    elif action == "PAY":
        # TODO: pay(state, player, "BANK", card["amount"], card["text"])
        pass

    elif action == "RECEIVE_FROM_EACH_PLAYER":
        for other in state.players:
            if other is not player and other.is_active():
                pay(state, other, player, card["amount"], card["text"])

    elif action == "PAY_EACH_PLAYER":
        # TODO: same idea as RECEIVE_FROM_EACH_PLAYER, but reversed
        pass

    elif action == "GO_TO_JAIL":
        from monopoly.rules import send_to_jail
        send_to_jail(player, state.spaces)

    elif action == "REPAIRS":
        houses = sum(s.houses for i in player.owned for s in [state.spaces[i]] if s.houses < 5)
        hotels = sum(1 for i in player.owned for s in [state.spaces[i]] if s.houses == 5)
        amount = houses * card["per_house"] + hotels * card["per_hotel"]
        pay(state, player, "BANK", amount, "repairs")

    elif action == "KEEP_JAIL_CARD":
        player.jail_cards += 1
```

## Test it yourself
Add to `tests/test_cards.py`:
```python
from monopoly.models import Player, GameState, Space
from monopoly.cards import apply_card

def test_receive_card_adds_cash():
    player = Player(0, "Alice", "hat")
    state = GameState([player], [Space(0, "Go", "GO")])
    apply_card({"text": "test", "action": "RECEIVE", "amount": 50}, player, state)
    assert player.cash == 1550

def test_keep_jail_card_increments_count():
    player = Player(0, "Alice", "hat")
    state = GameState([player], [Space(0, "Go", "GO")])
    apply_card({"text": "test", "action": "KEEP_JAIL_CARD"}, player, state)
    assert player.jail_cards == 1
```
Run `python -m pytest tests/test_cards.py -v`. Then write one test per card action type in your two JSON files — tedious, but exactly what PLAN.md means by "every card has a focused automated test."

## Checkpoint
```text
git commit -m "Implement all Chance and Community Chest card actions"
```
Every card in both decks now genuinely changes the game, matching the real rules.

## Stuck? Try this
- Movement cards don't pay Go correctly → the "did we pass Go" logic for cards is trickier than plain dice movement since it's an absolute jump, not a relative one; test both directions (moving forward past Go, and moving to a target index lower than your current one).
- `REPAIRS` counts the wrong number of houses → check you're only counting properties actually in `player.owned`, and treating `houses == 5` (a hotel) separately from `houses` 1-4.
