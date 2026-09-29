# Quest 03 · Colours and a logo

**Goal:** a real Monopoly logo on a smooth green background (or your picture from Quest 01).
**New files:** `ui/theme.py`, `ui/draw.py` **Changed:** `ui/app.py`

## Idea: one place for every colour

If every file typed its own `(22, 84, 62)`, changing the green would mean hunting through 20 files. Instead `theme.py` names every colour once, and everything else says `theme.FELT`. Change it there and the whole game changes.

## Idea: remembering things in a dictionary

Making a font is slow, and we'll ask for fonts thousands of times a second. So `font()` keeps every font it makes in a dictionary called `_fonts`. The first time you ask for size 20 it makes one. After that it hands back the one it already made.

## Do it

1. Create `ui/theme.py`:

```python
import pygame

# The game is always drawn at this size. pygame stretches it to fit the window.
WIDTH = 1600
HEIGHT = 900

# Colours are (red, green, blue), each from 0 to 255.
FELT = (22, 84, 62)            # the "table" behind the board
FELT_DARK = (11, 46, 34)
BOARD_GREEN = (206, 230, 208)  # the classic Monopoly board colour
TILE = (250, 248, 240)
INK = (28, 28, 30)
WHITE = (255, 255, 255)
PAPER = (252, 251, 247)
GREY = (125, 125, 130)
LIGHT_GREY = (225, 225, 228)
DISABLED = (180, 180, 186)

RED = (214, 40, 40)
GREEN = (38, 160, 90)
BLUE = (45, 110, 205)
ORANGE = (240, 140, 20)
PURPLE = (130, 80, 190)
GOLD = (245, 190, 50)
CHANCE_ORANGE = (247, 148, 29)
CHEST_BLUE = (0, 150, 214)

GROUP_COLORS = {
    "brown": (141, 85, 54),
    "light_blue": (170, 224, 250),
    "pink": (217, 58, 150),
    "orange": (247, 148, 29),
    "red": (237, 28, 36),
    "yellow": (254, 230, 0),
    "green": (31, 178, 90),
    "dark_blue": (0, 114, 187),
    "railroad": (60, 60, 60),
    "utility": (150, 150, 150),
}

TOKEN_COLORS = [
    (231, 76, 60),     # red
    (52, 152, 219),    # blue
    (46, 204, 113),    # green
    (241, 196, 15),    # yellow
    (155, 89, 182),    # purple
    (230, 126, 34),    # orange
]

# Fonts are slow to create, so we make each size once and remember it.
_fonts = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        if bold:
            _fonts[key] = pygame.font.SysFont("segoeuisemibold", size)
        else:
            _fonts[key] = pygame.font.SysFont("segoeui", size)
    return _fonts[key]


def title_font(size):
    key = (size, "title")
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont("segoeuiblack", size)
    return _fonts[key]
```

2. Create `ui/draw.py`. More helpers get added to this file in later quests.

```python
"""Small drawing helpers that every other ui file uses."""
from pathlib import Path

import pygame

from ui import theme

ASSETS_FOLDER = Path(__file__).parent.parent / "assets"


def text(surface, words, position, size=20, color=theme.INK, bold=False, anchor="topleft"):
    """Draw words on the screen. `anchor` says which point of the text sits at `position`:
    "topleft", "center", "midtop", "topright", "midleft", ...  Returns the text's Rect."""
    image = theme.font(size, bold).render(str(words), True, color)
    rect = image.get_rect(**{anchor: position})
    surface.blit(image, rect)
    return rect


def dim(surface, alpha=150):
    """Darken everything already drawn (used behind popups)."""
    layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    layer.fill((0, 0, 0, alpha))
    surface.blit(layer, (0, 0))


def make_logo(width):
    """The red MONOPOLY banner, as its own picture so it can be rotated."""
    height = width // 4
    logo = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(logo, theme.RED, logo.get_rect(), border_radius=6)
    pygame.draw.rect(logo, theme.WHITE, logo.get_rect().inflate(-10, -10), width=3, border_radius=4)
    words = theme.title_font(int(height * 0.62)).render("MONOPOLY", True, theme.WHITE)
    outline = theme.title_font(int(height * 0.62)).render("MONOPOLY", True, theme.INK)
    spot = words.get_rect(center=logo.get_rect().center)
    logo.blit(outline, spot.move(3, 3))
    logo.blit(words, spot)
    return logo


_background = None


def background(surface):
    """The green felt table. If assets/background.png exists, that's used instead."""
    global _background
    if _background is None:
        picture_file = ASSETS_FOLDER / "background.png"
        if picture_file.exists():
            picture = pygame.image.load(picture_file).convert()
            _background = pygame.transform.smoothscale(picture, surface.get_size())
            dim(_background, 90)
        else:
            _background = pygame.Surface(surface.get_size())
            for y in range(theme.HEIGHT):
                mix = y / theme.HEIGHT      # 0.0 at the top, 1.0 at the bottom
                # TODO: make `color` fade from theme.FELT at the top to theme.FELT_DARK at the bottom
                color = theme.FELT
                pygame.draw.line(_background, color, (0, y), (theme.WIDTH, y))
    surface.blit(_background, (0, 0))
```

> **Hint for the TODO:** for each of red, green and blue: `top + (bottom - top) * mix`. `zip(theme.FELT, theme.FELT_DARK)` pairs them up for you.

> **What's `**{anchor: position}`?** When `anchor` is `"center"`, it becomes `get_rect(center=position)`. It lets one function place text by any corner.

3. In `ui/app.py`:
   - add `from ui import theme` and `from ui.draw import background, make_logo, text` at the top
   - use `(theme.WIDTH, theme.HEIGHT)` instead of `(1600, 900)`
   - replace the `self.font = ...` line with `self.logo = make_logo(640)`
   - replace the fill and "Monopoly" lines in `run()` with:

```python
            background(self.window)
            self.window.blit(self.logo, self.logo.get_rect(center=(800, 250)))
            text(self.window, "a game by Manu", (800, 350), 26, theme.WHITE, anchor="center")
```

## Check it

- [ ] Red MONOPOLY logo near the top
- [ ] Background fades from green to dark green. Rename `assets/background.png` for a moment to see it, because if your picture is there, it's used instead.

## Save

Commit message: `Quest 03: theme colours and the logo`

⭐ **Extra:** make the six `TOKEN_COLORS` your favourite colours.
