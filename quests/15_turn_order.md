# Quest 15: Decide turn order

## Why this quest
Real Monopoly decides who goes first with a dice roll, not just "player 1." This is a small, self-contained rule that's a good warm-up before the bigger turn-loop quest next.

## Your tasks

1. In `monopoly/rules.py` (new file), write `roll_dice()` returning a tuple of two random ints from 1 to 6.
2. Write `decide_turn_order(players)`: roll dice for each active player, find the highest total, and if there's a tie, re-roll only among the tied players, repeating until there's a single winner. Return a new list of players in turn order starting from the winner.
3. Call this once when `GameScreen` is created (right after setup), store the result back into `state.players`, and log each roll to `state.history` via `state.log(...)`.

## Starter code

`monopoly/rules.py`:
```python
import random

def roll_dice():
    return (random.randint(1, 6), random.randint(1, 6))


def decide_turn_order(players, log=None):
    remaining = list(players)
    rolls = {}
    for player in remaining:
        d1, d2 = roll_dice()
        rolls[player.player_id] = d1 + d2
        if log:
            log(f"{player.name} rolled {d1} + {d2} = {d1 + d2} for turn order")

    highest = max(rolls.values())
    tied = [p for p in remaining if rolls[p.player_id] == highest]

    if len(tied) > 1:
        if log:
            log("Tie! Re-rolling among tied players.")
        # TODO: recursively call decide_turn_order(tied, log) to break the tie,
        # then figure out how to combine that result with the non-tied players
        # (hint: the winner of the tie-break becomes first; everyone else keeps
        # their original relative order starting after the winner)
        pass

    winner = tied[0]
    start_index = players.index(winner)
    # TODO: return players reordered so winner is first, preserving the
    # original relative order of everyone else (hint: slicing with [:] and
    # concatenation, e.g. players[start_index:] + players[:start_index])
```

## Test it yourself
Write a temporary test in `tests/test_turn_order.py`:
```python
from monopoly.rules import decide_turn_order
from monopoly.models import Player

def test_turn_order_returns_all_players():
    players = [Player(0, "Alice", "hat"), Player(1, "Bob", "car")]
    order = decide_turn_order(players)
    assert len(order) == 2
    assert set(p.player_id for p in order) == {0, 1}
```
Run `python -m pytest tests/test_turn_order.py -v` — this doesn't check *who* goes first (that's random) but confirms the function doesn't lose or duplicate a player. Run it several times (`python -m pytest tests/test_turn_order.py --count=20` if you have `pytest-repeat`, or just run it 20 times manually) since randomness means a single pass can hide a bug.

## Checkpoint
```text
git commit -m "Decide turn order with dice, rerolling ties"
```
This is a real Monopoly rule, fully working and tested, independent of any graphics.

## Stuck? Try this
- Infinite loop or crash on a tie → make sure your recursive call only includes the `tied` list, not all `players`, or it can tie against itself forever with only one player.
- Winner isn't actually first in the returned list → print `[p.name for p in order]` and compare against who actually had the highest roll from your printed logs.
