# Quest 08 · Board maths

**Goal:** 40 numbered boxes in the right places around the board. **New game** takes you there.
**New files:** `ui/board_layout.py`, `ui/board_view.py`, `ui/play_screen.py`, `tests/test_layout.py` **Changed:** `ui/screens.py`

## Idea: work it out with `//` and `%`

The board is a square: 4 corners, with 9 spaces along each side between them.

- `index // 10` is the **side**: 0 = bottom, 1 = left, 2 = top, 3 = right
- `index % 10` is the **step** along that side: 0 means it's a corner

Space 23: `23 // 10 = 2` (top row), `23 % 10 = 3` (the 3rd space along).

Sizes: corners are 113 px square, and the other spaces are 70 px wide. `113 + 9×70 + 113 = 856`, the whole board.

**Grab paper first.** Draw the square, put Go in the bottom-right corner, and number spaces 0, 1, 9, 10, 11, 20, 21, 30, 31 and 39. Which way does each side go?

## Do it

1. Create `ui/board_layout.py`. Two sides are yours to finish:

```python
"""Where every space goes on the screen. Just maths, no drawing."""
import pygame

CORNER = 113                  # corner squares are CORNER x CORNER pixels
TILE = 70                     # the other spaces are TILE pixels wide
SIZE = 2 * CORNER + 9 * TILE  # 856: the whole board
BOARD = pygame.Rect(22, 22, SIZE, SIZE)
FAR = SIZE - CORNER           # distance from the board's edge to the far corners
CENTER = pygame.Rect(BOARD.x + CORNER, BOARD.y + CORNER, 9 * TILE, 9 * TILE)


def side_of(index):
    """0 = bottom row, 1 = left column, 2 = top row, 3 = right column."""
    return index // 10


def space_rect(index):
    """The rectangle on screen for space number `index` (0 to 39)."""
    side = side_of(index)
    step = index % 10        # how far along its side the space is

    if step == 0:
        # Corners: Go (bottom right), Jail (bottom left), Free Parking (top left), Go To Jail (top right)
        x, y = [(FAR, FAR), (0, FAR), (0, 0), (FAR, 0)][side]
        return pygame.Rect(BOARD.x + x, BOARD.y + y, CORNER, CORNER)

    if side == 0:    # bottom row, going right to left
        return pygame.Rect(BOARD.x + FAR - step * TILE, BOARD.y + FAR, TILE, CORNER)
    if side == 1:    # left column, going upwards
        return pygame.Rect(BOARD.x, BOARD.y + FAR - step * TILE, CORNER, TILE)
    if side == 2:    # top row, going left to right
        pass    # TODO
    # right column, going downwards
    pass    # TODO


def inner_strip(index, thickness):
    """The edge of a space that faces the middle of the board (where the colour bar is)."""
    rect = space_rect(index)
    side = side_of(index)
    if side == 0:
        return pygame.Rect(rect.x, rect.y, rect.width, thickness)
    if side == 1:
        return pygame.Rect(rect.right - thickness, rect.y, thickness, rect.height)
    if side == 2:
        return pygame.Rect(rect.x, rect.bottom - thickness, rect.width, thickness)
    return pygame.Rect(rect.x, rect.y, thickness, rect.height)


def outer_strip(index, thickness):
    """The edge of a space that faces out, away from the middle."""
    rect = space_rect(index)
    side = side_of(index)
    if side == 0:
        return pygame.Rect(rect.x, rect.bottom - thickness, rect.width, thickness)
    if side == 1:
        return pygame.Rect(rect.x, rect.y, thickness, rect.height)
    if side == 2:
        return pygame.Rect(rect.x, rect.y, rect.width, thickness)
    return pygame.Rect(rect.right - thickness, rect.y, thickness, rect.height)
```

(You'll use `inner_strip` and `outer_strip` later, for houses and owner colours.)

2. Create `tests/test_layout.py`. Yes, you can test screen maths without opening a window:

```python
from ui.board_layout import BOARD, space_rect


def test_go_is_bottom_right():
    assert space_rect(0).bottomright == BOARD.bottomright


def test_jail_is_bottom_left():
    assert space_rect(10).bottomleft == BOARD.bottomleft


def test_free_parking_is_top_left():
    assert space_rect(20).topleft == BOARD.topleft


def test_every_space_is_on_the_board():
    for index in range(40):
        assert BOARD.contains(space_rect(index)), index


def test_no_spaces_overlap():
    for a in range(40):
        for b in range(a + 1, 40):
            assert not space_rect(a).colliderect(space_rect(b)), (a, b)
```

Fill in the TODOs until `python -m pytest` passes.

3. Create `ui/board_view.py`. For now it draws plain numbered boxes:

```python
import pygame

from ui import theme
from ui.board_layout import space_rect
from ui.draw import text


class BoardView:
    def __init__(self, board):
        self.board = board

    def draw(self, surface):
        for space in self.board:
            rect = space_rect(space.index)
            pygame.draw.rect(surface, theme.TILE, rect)
            pygame.draw.rect(surface, theme.INK, rect, 1)
            text(surface, space.index, rect.center, 20, anchor="center")
```

4. Create `ui/play_screen.py`, the screen where the game happens:

```python
import pygame

from ui.board_view import BoardView
from ui.draw import background


class PlayScreen:
    def __init__(self, app, board):
        self.app = app
        self.board_view = BoardView(board)

    # MenuScreen is imported here instead of at the top because screens.py
    # imports this file too. Two files importing each other at the top = crash.
    def quit_to_menu(self):
        from ui.screens import MenuScreen
        self.app.go_to(MenuScreen(self.app))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.quit_to_menu()

    def update(self, seconds):
        pass

    def draw(self, surface):
        background(surface)
        self.board_view.draw(surface)
```

5. In `ui/screens.py`, add the imports `from logic.board import load_board` and `from ui.play_screen import PlayScreen`, then make **New game** go there:

```python
    def new_game(self):
        self.app.go_to(PlayScreen(self.app, load_board()))
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] New game shows 0 in the bottom-right corner, counting up clockwise all the way to 39
- [ ] `Esc` goes back to the menu

## Save

Commit message: `Quest 08: where every space goes`
