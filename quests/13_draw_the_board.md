# Quest 13: Draw the actual board

## Why this quest
Time to see all 40 spaces on screen at once, using the board data (Quest 11) and the position math (Quest 12) together. This is the first moment the project looks like Monopoly.

## Your tasks

1. In `monopoly/screens.py`, create a `GameScreen` class (similar shape to `MenuScreen`) that, in `__init__`, calls `load_board()` to get its `spaces` list and stores a `pygame.Rect` for the board area (e.g. a square in the center-left of the window).
2. Write `GameScreen.draw(self, surface)`: for every space, get its `space_rect` and draw a rectangle outline, then draw the space's name in small text inside it (shortened if it doesn't fit — you don't need every letter).
3. For `"STREET"` spaces, draw a thin colored strip along the outer edge of the rectangle using a color that matches `group` (make a small dictionary mapping group names to RGB colors).
4. Draw a large label in the center of the board (e.g. "MONOPOLY").
5. Wire "New Game" on the main menu to eventually reach `GameScreen` (for now it's fine to go there directly, skipping player setup — that's Quest 14).

## Starter code

Add to `monopoly/screens.py`:
```python
import pygame
from monopoly.models import load_board
from monopoly.board_view import space_rect

GROUP_COLORS = {
    "brown": (101, 67, 33),
    "light_blue": (135, 206, 250),
    "pink": (216, 87, 155),
    "orange": (245, 146, 40),
    "red": (220, 40, 40),
    "yellow": (245, 220, 40),
    "green": (40, 150, 60),
    "dark_blue": (20, 60, 140),
}

class GameScreen:
    def __init__(self, app):
        self.app = app
        self.spaces = load_board()
        self.board_rect = pygame.Rect(40, 40, 720, 720)

    def handle_event(self, event):
        pass  # buttons come in a later quest

    def draw(self, surface):
        for space in self.spaces:
            rect = space_rect(space.index, self.board_rect)
            pygame.draw.rect(surface, (240, 240, 230), rect)
            pygame.draw.rect(surface, (20, 20, 20), rect, width=1)

            if space.space_type == "STREET":
                color = GROUP_COLORS.get(space.group, (150, 150, 150))
                # TODO: draw a thin strip of `color` along the outer edge
                # of `rect` (a pygame.draw.rect with a small height/width,
                # positioned along whichever side faces outward)

            # TODO: render space.name in a small font and blit it inside rect,
            # shortening it (e.g. name[:10]) if it's too long to fit
```

## Test it yourself
Run `python main.py`, go to New Game (or temporarily point it straight at `GameScreen` if setup isn't built yet). Confirm: all 40 spaces are visible with no gaps or overlaps, Go is in a corner, street spaces show their group color, and resizing the window doesn't scramble the layout (it's fine if it doesn't resize gracefully yet — just don't let it crash).

## Checkpoint
```text
git commit -m "Draw board spaces from data"
```
The board is no longer an abstract list of 40 objects — it's something a player could actually look at and understand.

## Stuck? Try this
- Names overflow their rectangles → shorten with slicing, e.g. `space.name[:8]`, or reduce the font size for board text specifically (a smaller `pygame.font.SysFont(None, 16)`).
- Nothing draws at all → confirm `GameScreen.draw` is actually being called — check `App.draw` delegates to `self.screen.draw(self.window)` and that you actually switched `self.screen` to a `GameScreen`.
- Colors look wrong → print `space.group` for a few streets and compare against the exact keys in `GROUP_COLORS` — a mismatched key silently falls back to gray via `.get()`.
