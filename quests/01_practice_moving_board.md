# Quest 01: Move around a board (practice)

## Why this quest
This is throwaway practice code, not part of the real game yet. The goal is to prove to yourself you can model "a token moving around a loop of 40 spaces" before you do it for real. Delete this file when you're done.

## New idea(s)
**The remainder operator `%`.** `%` gives you what's left over after dividing. `7 % 3` is `1`, because 3 goes into 7 twice with 1 left over. On a board of 40 spaces numbered 0-39, if you're standing on space 38 and move 5 spaces, you don't want position 43 — you want to wrap around to position 3. `(38 + 5) % 40` gives you exactly that.

```python
for n in [5, 38, 40, 79]:
    print(n % 40)
# 5, 38, 0, 39
```

## Your tasks

1. Create a scratch file, e.g. `scratch_practice_a.py` (not inside `monopoly/`).
2. Make a variable `position` starting at `0`.
3. Write a function `roll_die()` that returns a random whole number from 1 to 6.
4. Write a function `move(position, spaces)` that returns the new position after moving `spaces` steps from `position`, wrapping around at 40 using `%`.
5. In a loop that runs 10 times: roll two dice, add them together, move, and print the roll and the new position.

## Starter code
```python
import random

def roll_die():
    # TODO: return a random integer from 1 to 6
    pass

def move(position, spaces):
    # TODO: return the new position, wrapping around at 40
    pass

position = 0
for turn in range(10):
    d1 = roll_die()
    d2 = roll_die()
    total = d1 + d2
    position = move(position, total)
    print(f"Rolled {d1} + {d2} = {total}, now on space {position}")
```

## Test it yourself
Run `python scratch_practice_a.py`. You should see 10 lines printed. Check by hand: every printed position must be between 0 and 39 inclusive, and each new position should equal the old one plus the roll, wrapped with `%`.

## Checkpoint
```text
git commit -m "Practice A: move a token around a 40-space loop"
```
You just wrote the exact math the real game will use to move players around the board.

## Stuck? Try this
- `random` not imported → add `import random` at the top.
- Position goes above 39 → you forgot the `% 40`, or applied it to the wrong number.
- `roll_die()` always returns the same number → check you used `random.randint(1, 6)`, not `random.random()`.
