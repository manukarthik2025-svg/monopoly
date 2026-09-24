# Quest 12: Turn a space index into screen coordinates

## Why this quest
You have 40 `Space` objects but no idea where to draw them. Rather than writing 40 separate "draw space 7 at pixel (x, y)" statements, you'll write one function that calculates any space's position from its index and a bit of math — the "calculate, don't hardcode" idea PLAN.md keeps insisting on.

## Your tasks

1. In a new file `monopoly/board_view.py`, write a function `space_rect(index, board_rect)` that returns a `pygame.Rect` for where that space belongs on screen.
2. `board_rect` is the square area the whole board lives in (you'll pass this in from the game screen later).
3. The board has 11 spaces along each edge (4 corners + 9 in between), for `4 * 9 + 4 = 40` total.
4. Corners (indexes `0`, `10`, `20`, `30`) are squares at the four corners of `board_rect`.
5. Indexes `1-9` run along the bottom edge (right to left, since Go is bottom-right in real Monopoly). Indexes `11-19` run up the right edge. Indexes `21-29` run along the top edge. Indexes `31-39` run down the left edge.
6. Don't write four separate blocks of near-identical code for the four sides. Instead, figure out which "side" the index belongs to (`index // 10`) and its position along that side (`index % 10`), then compute one `x, y` from that.

## Starter code
```python
import pygame

def space_rect(index, board_rect):
    corner_size = board_rect.width // 8
    edge_length = board_rect.width - 2 * corner_size
    step = edge_length // 9

    side = index // 10        # 0 = bottom, 1 = right, 2 = top, 3 = left
    position_on_side = index % 10

    if position_on_side == 0:
        # TODO: this is a corner space. Figure out which corner from `side`
        # and return a corner_size x corner_size square in the right spot.
        pass
    else:
        # TODO: this is an edge space. Using `side` and `position_on_side`,
        # work out the x, y for a (step x corner_size) or (corner_size x step)
        # rectangle along the correct edge, moving in the right direction.
        pass

    return pygame.Rect(0, 0, corner_size, corner_size)  # placeholder, replace this
```

## Test it yourself
Write a tiny temporary script that calls `space_rect(i, pygame.Rect(0, 0, 800, 800))` for every `i` from 0 to 39 and prints each result. Check by hand:
- Index 0 and index 10 should be at opposite corners along the bottom.
- Indexes 1 through 9 should have steadily changing x (or y) values, staying on one edge, with no big jumps.
- No rectangle should have negative x or y, or extend past 800.

## Checkpoint
```text
git commit -m "Calculate board space positions from index"
```
This single function replaces what would otherwise be 40 separate hardcoded rectangles — and it'll automatically stay correct if you resize the window later.

## Stuck? Try this
- Spaces overlap or leave gaps → walk through the math for `index = 1` and `index = 9` by hand on paper first; get the numbers right before writing code.
- All spaces land in the same spot → you're probably returning the placeholder rect at the bottom instead of your calculated one — Python doesn't warn you about unreachable code paths.
- Confused about `//` vs `%` → `//` (floor division) throws away the remainder and keeps the whole number; `%` keeps only the remainder. `23 // 10 == 2` and `23 % 10 == 3`.
