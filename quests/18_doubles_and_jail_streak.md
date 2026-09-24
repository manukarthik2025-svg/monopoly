# Quest 18: Doubles give another turn (mostly)

## Why this quest
Rolling doubles is one of the most Monopoly-specific rules: it usually means "roll again," but three in a row sends you straight to jail instead. This quest teaches the game to count.

## Your tasks

1. In `GameScreen.roll()` (from Quest 16), after rolling, check if the two dice match.
2. If they match, increment `state.doubles_count`. If they don't match, reset it to `0`.
3. If `state.doubles_count` reaches `3`, don't move the player at all — instead send them directly to jail (set `player.position` to the Jail space's index, `player.in_jail = True`, reset `state.doubles_count` to `0`, log it, and skip straight to `TURN_END`, since going directly to jail never pays Go even if the position number would otherwise cross it).
4. Otherwise, proceed with movement as before. After the move resolves, if the roll was doubles (and didn't trigger the three-in-a-row jail rule), set the phase back to `WAITING_FOR_ROLL` instead of `TURN_END`, so the same player rolls again.
5. Make sure `state.doubles_count` resets to `0` whenever a turn actually ends (Quest 19 will formalize "ending a turn" — for now, reset it wherever you currently transition into `TURN_END`).

## Starter code

Update the roll logic in `monopoly/screens.py`:
```python
def roll(self):
    if self.state.phase != rules.WAITING_FOR_ROLL:
        return
    dice = rules.roll_dice()
    self.state.dice = dice
    self.state.log(f"{self.state.current_player().name} rolled {dice[0]} and {dice[1]}")

    is_double = dice[0] == dice[1]
    # TODO: if is_double, increment self.state.doubles_count; otherwise reset it to 0

    if self.state.doubles_count == 3:
        # TODO: send player directly to jail (see rules.send_to_jail below),
        # log it, reset doubles_count to 0, set phase to rules.TURN_END,
        # and return early — this player does not move normally this turn
        pass

    self.state.phase = rules.MOVING
    self.pending_double = is_double  # remember this for use in update()
```

Add to `monopoly/rules.py`:
```python
def find_jail_index(spaces):
    for space in spaces:
        if space.space_type == "JAIL":
            return space.index
    raise ValueError("No JAIL space found in board data")


def send_to_jail(player, spaces):
    # TODO: set player.position to find_jail_index(spaces), player.in_jail = True
    pass
```

Update `GameScreen.update()`'s `MOVING` branch: after logging what space was landed on, instead of always setting `TURN_END`, do:
```python
if getattr(self, "pending_double", False):
    self.state.phase = rules.WAITING_FOR_ROLL
else:
    self.state.phase = rules.TURN_END
```

## Test it yourself
Add to `tests/test_movement.py`:
```python
from monopoly.rules import send_to_jail, find_jail_index
from monopoly.models import Space

def test_send_to_jail_moves_player_and_flags_them():
    player = Player(0, "Alice", "hat")
    spaces = [Space(0, "Go", "GO"), Space(10, "Jail", "JAIL")]
    send_to_jail(player, spaces)
    assert player.position == 10
    assert player.in_jail is True
```
Run `python -m pytest tests/test_movement.py -v`. Then play manually: roll until you get doubles and confirm you get another roll; if you're feeling patient (or temporarily rig the dice with a debug key), get three doubles in a row and confirm you land directly in jail without collecting Go money even if your position would have crossed it.

## Checkpoint
```text
git commit -m "Handle doubles: extra turns and three-in-a-row jail rule"
```
This is a rule that trips up a lot of home-made Monopoly implementations — you've got it right and tested.

## Stuck? Try this
- Extra turns never happen → confirm `pending_double` is actually being read in `update()`, and that it's stored on `self` (as `self.pending_double`), not as a local variable that disappears after `roll()` returns.
- Player collects 200 even when sent directly to jail → make sure the "three doubles" branch returns *before* reaching the normal movement/pass-Go code, not after.
