# Quest 26: Getting out of jail

## Why this quest
Being in jail needs its own mini turn: pay bail, use a card, or try for doubles — each with different consequences. This is a genuinely fiddly rule; take it slowly and lean on the tests.

## Your tasks

1. Add a new phase `IN_JAIL_DECISION`.
2. At the start of a turn (in your Roll-Dice-enabling logic), if `state.current_player().in_jail` is `True`, set phase to `IN_JAIL_DECISION` instead of `WAITING_FOR_ROLL`, and show three buttons: "Pay 50", "Use Card" (disabled if `jail_cards == 0`), "Roll for Doubles".
3. "Pay 50": `pay(state, player, "BANK", 50, "bail")`, set `in_jail = False`, then go straight to `WAITING_FOR_ROLL` (they still get to roll and move normally this turn).
4. "Use Card": decrement `jail_cards`, set `in_jail = False`, same as above (the physical card returns to its deck — you'll wire that up properly once decks exist in Quest 27).
5. "Roll for Doubles": roll the dice. If doubles, set `in_jail = False` and move normally using this roll (no extra turn for the doubles, since getting out of jail already used it). If not doubles, increment `jail_turns`; if `jail_turns < 3`, end the turn with no movement; if `jail_turns == 3`, force `pay(state, player, "BANK", 50, "forced bail")`, set `in_jail = False`, and move using this roll.
6. Write `attempt_jail_roll(state, player)` in `rules.py` containing this logic so it's testable without clicking buttons.

## Starter code
```python
IN_JAIL_DECISION = "IN_JAIL_DECISION"

def attempt_jail_roll(state, player):
    dice = roll_dice()
    state.dice = dice
    is_double = dice[0] == dice[1]

    if is_double:
        player.in_jail = False
        state.log(f"{player.name} rolled doubles and leaves jail")
        return dice  # caller should now move the player using sum(dice)

    player.jail_turns += 1
    if player.jail_turns >= 3:
        # TODO: pay 50 to the bank as forced bail, set in_jail = False,
        # log it, and return dice so the caller moves the player
        pass

    state.log(f"{player.name} failed to roll doubles in jail ({player.jail_turns}/3)")
    return None  # caller should end the turn without moving
```

In `GameScreen`, the roll button's behavior needs to branch:
```python
def roll(self):
    player = self.state.current_player()
    if self.state.phase == rules.IN_JAIL_DECISION:
        dice = rules.attempt_jail_roll(self.state, player)
        if dice is None:
            self.state.phase = rules.TURN_END
        else:
            self.state.phase = rules.MOVING
        return
    # ... existing WAITING_FOR_ROLL logic from Quest 16/18 ...
```
Add `pay_bail` and `use_jail_card` functions in `rules.py` following the same shape, each setting `in_jail = False` and transitioning phase to `WAITING_FOR_ROLL`.

## Test it yourself
Add to `tests/test_jail.py`:
```python
from monopoly.rules import attempt_jail_roll
from monopoly.models import GameState, Space

def test_third_failed_attempt_forces_bail():
    player = Player(0, "Alice", "hat")
    player.in_jail = True
    player.jail_turns = 2
    state = GameState([player], [Space(0, "Go", "GO")])
    # Run attempt_jail_roll enough times (mock or just check the counting logic
    # directly by calling it and inspecting jail_turns and in_jail after forcing
    # jail_turns to 2 beforehand, since real dice are random)
    result = attempt_jail_roll(state, player)
    # Because dice are random, only assert what must always be true regardless
    # of the roll: either doubles freed them, or jail_turns went to 3 and bail
    # was forced, or jail_turns is 3 with in_jail still True if your forced-bail
    # branch has a bug. Assert player.in_jail is False after this call.
    assert player.in_jail is False
```
Run this test multiple times in a row (`python -m pytest tests/test_jail.py -v` repeatedly) since it depends on random dice — it should pass every time regardless of the roll, because either doubles or forced bail always frees the player on the third attempt.

## Checkpoint
```text
git commit -m "Implement jail turn choices: bail, card, and doubles"
```
Jail is one of the fiddliest rules in Monopoly — you've now covered every legal way in and out.

## Stuck? Try this
- Player stuck in jail forever → check `jail_turns >= 3` really does force bail rather than just logging a failed attempt again.
- Rolling doubles to leave jail also gives an extra turn → re-read the rule: doubles that free you from jail move you once, normally, with no bonus roll — this is different from ordinary doubles during a normal turn.
