# Quest 09 · Paint the board

**Goal:** a proper Monopoly board with colour bars, names, prices, little pictures, and the logo in the middle.
**New file:** `ui/board_art.py` **Changed:** `ui/board_view.py`, `ui/draw.py`

## Idea: paint once, reuse forever

The board has 40 spaces with 100+ bits of text. Painting all of that 60 times a second would be slow. The board never changes, so we paint it **once** onto its own picture (a `Surface`) and just stick that picture on the screen each frame. Owners, houses and tokens get drawn on top later.

## Idea: draw it standing up, then turn it

Every ordinary space is drawn the same way: standing upright, with its colour bar at the top. Then it gets **rotated** so the bar faces the middle of the board:

```text
bottom row:   don't turn
left column:  turn a quarter
top row:      turn upside down
right column: turn a quarter the other way
```

## Do it

1. Add two more helpers to `ui/draw.py`:

```python
def text_block(surface, words, center_x, top, max_width, size=18, color=theme.INK, bold=False):
    """Draw wrapped, centred lines of text. Returns the y just below the last line."""
    y = top
    for line in wrap(words, size, max_width, bold):
        rect = text(surface, line, (center_x, y), size, color, bold, anchor="midtop")
        y = rect.bottom - size // 8
    return y


def money(amount):
    return f"${amount:,}"
```

(`{amount:,}` puts commas in big numbers: `$1,500`.)

2. Create `ui/board_art.py`. It's long, so paste it, then read through `draw_tile` and `draw_board_picture` together.

```python
"""Paints the board picture once, at the start. Nothing here changes during a game."""
import pygame

from ui import theme
from ui.board_layout import BOARD, CENTER, CORNER, TILE, side_of, space_rect
from ui.draw import darker, make_logo, money, text, text_block

# ---------- little pictures ----------


def draw_train(surface, center):
    x, y = center
    pygame.draw.rect(surface, theme.INK, (x - 20, y - 8, 30, 14), border_radius=2)      # body
    pygame.draw.rect(surface, theme.INK, (x + 6, y - 16, 12, 22), border_radius=2)      # cab
    pygame.draw.rect(surface, theme.INK, (x - 16, y - 16, 6, 8))                        # chimney
    for wheel_x in (x - 14, x - 2, x + 12):
        pygame.draw.circle(surface, theme.INK, (wheel_x, y + 9), 5)
        pygame.draw.circle(surface, theme.TILE, (wheel_x, y + 9), 2)


def draw_bulb(surface, center):
    x, y = center
    pygame.draw.circle(surface, theme.GOLD, (x, y - 6), 13)
    pygame.draw.circle(surface, theme.INK, (x, y - 6), 13, 2)
    pygame.draw.rect(surface, theme.GREY, (x - 6, y + 6, 12, 10), border_radius=2)
    pygame.draw.line(surface, theme.INK, (x - 4, y - 4), (x, y - 12), 2)
    pygame.draw.line(surface, theme.INK, (x, y - 12), (x + 4, y - 4), 2)


def draw_tap(surface, center):
    x, y = center
    pygame.draw.rect(surface, theme.GREY, (x - 18, y - 12, 26, 9), border_radius=3)
    pygame.draw.rect(surface, theme.GREY, (x + 2, y - 12, 9, 16), border_radius=3)
    pygame.draw.rect(surface, theme.INK, (x - 10, y - 19, 4, 8))
    pygame.draw.polygon(surface, theme.CHEST_BLUE, [(x + 6, y + 6), (x + 1, y + 15), (x + 11, y + 15)])
    pygame.draw.circle(surface, theme.CHEST_BLUE, (x + 6, y + 16), 5)


def draw_chest(surface, center):
    x, y = center
    brown = (150, 95, 45)
    pygame.draw.rect(surface, brown, (x - 20, y - 8, 40, 22), border_radius=3)
    pygame.draw.rect(surface, darker(brown), (x - 20, y - 18, 40, 12),
                     border_top_left_radius=8, border_top_right_radius=8)
    pygame.draw.rect(surface, theme.INK, (x - 20, y - 18, 40, 32), 2, border_radius=4)
    pygame.draw.rect(surface, theme.GOLD, (x - 4, y - 8, 8, 9))


def draw_car(surface, center):
    x, y = center
    pygame.draw.rect(surface, theme.RED, (x - 26, y - 4, 52, 14), border_radius=5)
    pygame.draw.rect(surface, theme.RED, (x - 14, y - 16, 28, 14), border_radius=6)
    pygame.draw.rect(surface, (190, 225, 250), (x - 10, y - 13, 20, 8), border_radius=3)
    for wheel_x in (x - 15, x + 15):
        pygame.draw.circle(surface, theme.INK, (wheel_x, y + 10), 7)
        pygame.draw.circle(surface, theme.LIGHT_GREY, (wheel_x, y + 10), 3)


def draw_padlock(surface, center):
    x, y = center
    pygame.draw.arc(surface, theme.INK, (x - 13, y - 26, 26, 30), 0, 3.15, 5)
    pygame.draw.rect(surface, theme.GOLD, (x - 18, y - 10, 36, 28), border_radius=5)
    pygame.draw.rect(surface, theme.INK, (x - 18, y - 10, 36, 28), 2, border_radius=5)
    pygame.draw.circle(surface, theme.INK, (x, y + 2), 4)


def draw_diamond(surface, center):
    x, y = center
    points = [(x, y - 16), (x + 16, y), (x, y + 16), (x - 16, y)]
    pygame.draw.polygon(surface, (120, 170, 220), points)
    pygame.draw.polygon(surface, theme.INK, points, 2)


def draw_icon(surface, space, center):
    """The little picture for railroads, utilities, cards and taxes."""
    if space.kind == "RAILROAD":
        draw_train(surface, center)
    elif space.name == "Electric Company":
        draw_bulb(surface, center)
    elif space.name == "Water Works":
        draw_tap(surface, center)
    elif space.name == "Community Chest":
        draw_chest(surface, center)
    elif space.name == "Chance":
        text(surface, "?", center, 58, theme.CHANCE_ORANGE, bold=True, anchor="center")
    elif space.kind == "TAX":
        draw_diamond(surface, center)


# ---------- the spaces ----------


def space_name(surface, name, top, width):
    """The name in capitals, shrunk until every word fits."""
    words = name.upper()
    size = 11
    while size > 7 and any(theme.font(size, True).size(word)[0] > width for word in words.split()):
        size -= 1
    return text_block(surface, words, surface.get_width() // 2, top, width, size, bold=True)


def draw_tile(space):
    """One ordinary space, drawn standing up with its top facing the middle of the board."""
    tile = pygame.Surface((TILE, CORNER))
    tile.fill(theme.TILE)
    middle = TILE // 2

    if space.kind == "STREET":
        pygame.draw.rect(tile, theme.GROUP_COLORS[space.group], (0, 0, TILE, 24))
        pygame.draw.line(tile, theme.INK, (0, 24), (TILE, 24))
        space_name(tile, space.name, 28, TILE - 6)
    else:
        space_name(tile, space.name, 5, TILE - 6)
        draw_icon(tile, space, (middle, 64))

    if space.kind == "TAX":
        text(tile, f"PAY {money(space.price)}", (middle, CORNER - 6), 11, bold=True, anchor="midbottom")
    elif space.price:
        text(tile, money(space.price), (middle, CORNER - 6), 12, anchor="midbottom")
    return tile


def draw_corner(space):
    corner = pygame.Surface((CORNER, CORNER))
    corner.fill(theme.TILE)
    middle = CORNER // 2

    if space.kind == "GO":
        text(corner, "COLLECT $200", (middle, 10), 11, bold=True, anchor="midtop")
        text(corner, "AS YOU PASS", (middle, 24), 10, anchor="midtop")
        go = theme.title_font(44).render("GO", True, theme.RED)
        corner.blit(go, go.get_rect(center=(middle, 60)))
        arrow = [(14, 96), (34, 84), (34, 91), (98, 91), (98, 101), (34, 101), (34, 108)]
        pygame.draw.polygon(corner, theme.RED, arrow)

    elif space.kind == "JAIL":
        cell = pygame.Rect(CORNER - 80, 0, 80, 80)
        pygame.draw.rect(corner, theme.CHANCE_ORANGE, cell)
        window = cell.inflate(-24, -24)
        pygame.draw.rect(corner, theme.WHITE, window)
        for bar_x in range(window.x + 8, window.right, 10):
            pygame.draw.line(corner, theme.INK, (bar_x, window.y), (bar_x, window.bottom), 3)
        pygame.draw.rect(corner, theme.INK, window, 2)
        pygame.draw.rect(corner, theme.INK, cell, 1)
        text(corner, "IN JAIL", (cell.centerx, cell.bottom - 2), 11, bold=True, anchor="midbottom")
        visiting = pygame.transform.rotate(theme.font(11, True).render("JUST VISITING", True, theme.INK), 90)
        corner.blit(visiting, visiting.get_rect(center=(16, 40)))

    elif space.kind == "FREE_PARKING":
        text(corner, "FREE", (middle, 12), 15, theme.RED, bold=True, anchor="midtop")
        draw_car(corner, (middle, 60))
        text(corner, "PARKING", (middle, CORNER - 12), 15, theme.RED, bold=True, anchor="midbottom")

    elif space.kind == "GO_TO_JAIL":
        text(corner, "GO TO", (middle, 12), 15, theme.BLUE, bold=True, anchor="midtop")
        draw_padlock(corner, (middle, 62))
        text(corner, "JAIL", (middle, CORNER - 12), 15, theme.BLUE, bold=True, anchor="midbottom")

    return corner


def draw_card_pile(label, color, angle):
    pile = pygame.Surface((170, 100), pygame.SRCALPHA)
    pygame.draw.rect(pile, (*color, 60), pile.get_rect(), border_radius=10)
    pygame.draw.rect(pile, color, pile.get_rect(), width=3, border_radius=10)
    text(pile, label, (85, 50), 17, darker(color, 40), bold=True, anchor="center")
    return pygame.transform.rotate(pile, angle)


def draw_board_picture(board):
    """Paint the whole board onto one picture that's reused every frame."""
    picture = pygame.Surface(BOARD.size)
    picture.fill(theme.BOARD_GREEN)

    # The middle: logo and the two card piles.
    middle = (CENTER.centerx - BOARD.x, CENTER.centery - BOARD.y)
    logo = pygame.transform.rotate(make_logo(460), 40)
    picture.blit(logo, logo.get_rect(center=middle))
    chest_pile = draw_card_pile("COMMUNITY CHEST", theme.CHEST_BLUE, 40)
    picture.blit(chest_pile, chest_pile.get_rect(center=(middle[0] - 165, middle[1] - 165)))
    chance_pile = draw_card_pile("CHANCE", theme.CHANCE_ORANGE, 40)
    picture.blit(chance_pile, chance_pile.get_rect(center=(middle[0] + 165, middle[1] + 165)))

    # The 40 spaces around the edge.
    for space in board:
        rect = space_rect(space.index).move(-BOARD.x, -BOARD.y)
        if space.index % 10 == 0:
            art = draw_corner(space)
        else:
            turn = [0, 0, 0, 0][side_of(space.index)]    # TODO: the right angle for each side
            art = pygame.transform.rotate(draw_tile(space), turn)
        picture.blit(art, rect)
        pygame.draw.rect(picture, theme.INK, rect, 1)

    pygame.draw.rect(picture, theme.INK, picture.get_rect(), 3)
    pygame.draw.rect(picture, theme.INK, CENTER.move(-BOARD.x, -BOARD.y), 2)
    return picture
```

3. Make `BoardView` use the picture. Replace `ui/board_view.py` with:

```python
from ui.board_art import draw_board_picture
from ui.board_layout import BOARD
from ui.draw import shadow


class BoardView:
    def __init__(self, board):
        self.board = board
        self.picture = draw_board_picture(board)

    def draw(self, surface):
        shadow(surface, BOARD, radius=4, offset=8, alpha=90)
        surface.blit(self.picture, BOARD.topleft)
```

4. **The TODO.** `pygame.transform.rotate` takes an angle in degrees, and positive means anticlockwise. Run the game and look at it. Try `90`, `-90` and `180` for each side until every colour bar faces the middle.

## Check it

- [ ] Every colour bar faces the middle of the board
- [ ] Go is bottom-right, Boardwalk is next to it on the right side
- [ ] The logo sits diagonally in the middle

## Save

Commit message: `Quest 09: paint the board`

⭐ **Extra:** redesign one of the little pictures. Maybe give the Free Parking car a spoiler?
