# Quest 10 · Who's playing?

**Goal:** type in 2 to 6 names, click Start, and see everyone's token sitting on Go.
**New file:** `logic/game.py` **Changed:** `ui/widgets.py`, `ui/draw.py`, `ui/screens.py`, `ui/play_screen.py`, `ui/board_view.py`

## Idea: one object that holds the whole game

`Game` will hold **everything** about a game: the players, the board, whose turn it is, and a log of what happened. It will also hold every rule. It starts tiny today and grows in almost every quest after this.

## Do it

1. Create `logic/game.py`:

```python
from logic.board import load_board


class Game:
    """Everything about one game of Monopoly, and every rule for changing it."""

    def __init__(self, players):
        self.players = players
        self.board = load_board()
        self.turn = 0                # index into self.players
        self.log = []
        self.say(f"{self.current_player().name} goes first!")

    def current_player(self):
        return self.players[self.turn]

    def active_players(self):
        return [player for player in self.players if not player.bankrupt]

    def say(self, message):
        self.log.append(message)
```

2. Add a `TextBox` to the bottom of `ui/widgets.py`:

```python
class TextBox:
    """A box you can click on and type into."""

    def __init__(self, rect, words=""):
        self.rect = pygame.Rect(rect)
        self.words = words
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.words = self.words[:-1]
            elif event.unicode.isprintable() and len(self.words) < 12:
                self.words += event.unicode

    def draw(self, surface):
        border = theme.BLUE if self.active else theme.LIGHT_GREY
        pygame.draw.rect(surface, theme.WHITE, self.rect, border_radius=8)
        pygame.draw.rect(surface, border, self.rect, width=3, border_radius=8)
        rect = text(surface, self.words, (self.rect.x + 14, self.rect.centery), 22, anchor="midleft")
        blink_on = pygame.time.get_ticks() // 500 % 2 == 0
        if self.active and blink_on:
            pygame.draw.line(surface, theme.INK, (rect.right + 2, rect.top + 4), (rect.right + 2, rect.bottom - 4), 2)
```

3. Add a `token` helper to `ui/draw.py`:

```python
def token(surface, player, center, radius=14):
    """A player's round playing piece with their first letter on it."""
    x, y = center
    pygame.draw.circle(surface, (0, 0, 0), (x + 1, y + 3), radius)
    pygame.draw.circle(surface, theme.WHITE, (x, y), radius)
    pygame.draw.circle(surface, player.color, (x, y), radius - 3)
    letter = player.name[:1].upper()
    text(surface, letter, (x, y), int(radius * 1.1), text_color_for(player.color), bold=True, anchor="center")
```

4. In `ui/screens.py`, add these imports (and remove `load_board`, which isn't needed here any more):

```python
import random

from logic.game import Game
from logic.player import Player
from ui.widgets import Button, TextBox
```

   Add `token` to the `from ui.draw import ...` line. Make New game open the setup screen:

```python
    def new_game(self):
        self.app.go_to(SetupScreen(self.app))
```

   Then add this class under `MenuScreen`:

```python
class SetupScreen:
    def __init__(self, app):
        self.app = app
        self.box = pygame.Rect(MIDDLE - 360, 70, 720, 760)
        self.name_boxes = []
        for i in range(6):
            self.name_boxes.append(TextBox((self.box.x + 110, self.box.y + 120 + i * 76, 400, 58), f"Player {i + 1}"))
        self.count = 2
        self.add_button = Button("+ Add", self.add_player, (self.box.x + 530, 0, 150, 52), theme.BLUE)
        self.remove_button = Button("Remove", self.remove_player, (self.box.x + 530, 0, 150, 52), theme.GREY)
        self.start_button = Button("Start game!", self.start, (MIDDLE - 160, self.box.bottom - 96, 320, 66),
                                   theme.GREEN, 26)
        self.back_button = Button("Back", self.back, (30, 30, 120, 50), theme.GREY)

    def add_player(self):
        self.count = min(6, self.count + 1)

    def remove_player(self):
        pass    # TODO: one fewer player, but never fewer than 2

    def names(self):
        return [box.words.strip() for box in self.name_boxes[:self.count]]

    def problem(self):
        """What's stopping the game from starting, or None if it's ready."""
        names = self.names()
        if "" in names:
            return "Every player needs a name"
        # TODO: if two names are the same, return "Two players have the same name"
        #       (hint: a set() has no repeats. Compare its length to the list's length.)
        return None

    def start(self):
        players = []
        for i, name in enumerate(self.names()):
            players.append(Player(name, theme.TOKEN_COLORS[i]))
        random.shuffle(players)          # a random player goes first
        self.app.go_to(PlayScreen(self.app, Game(players)))

    def back(self):
        self.app.go_to(MenuScreen(self.app))

    def buttons(self):
        row_y = self.box.y + 120 + (self.count - 1) * 76 + 3
        self.remove_button.rect.y = row_y
        self.add_button.rect.y = row_y + 76
        buttons = [self.start_button, self.back_button]
        if self.count > 2:
            buttons.append(self.remove_button)
        if self.count < 6:
            buttons.append(self.add_button)
        return buttons

    def handle_event(self, event):
        for box in self.name_boxes[:self.count]:
            box.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.problem() is None:
            self.start()
            return
        for button in self.buttons():
            if button.handle_event(event):
                return

    def update(self, seconds):
        self.start_button.enabled = self.problem() is None

    def draw(self, surface):
        background(surface)
        panel(surface, self.box, theme.PAPER)
        text(surface, "Who's playing?", (MIDDLE, self.box.y + 34), 40, bold=True, anchor="midtop")
        for i, box in enumerate(self.name_boxes[:self.count]):
            dummy = Player(box.words or "?", theme.TOKEN_COLORS[i])
            token(surface, dummy, (self.box.x + 66, box.rect.centery), radius=22)
            box.draw(surface)
        for button in self.buttons():
            button.draw(surface)
```

5. `PlayScreen` now gets a whole `Game` instead of just a board. In `ui/play_screen.py`:

```python
    def __init__(self, app, game):
        self.app = app
        self.game = game
        self.board_view = BoardView(game)
```

6. Replace `ui/board_view.py`. It now draws the tokens as well:

```python
import math

import pygame

from ui import theme
from ui.board_art import draw_board_picture
from ui.board_layout import BOARD, space_rect
from ui.draw import shadow, token


def spots_in(rect, count, gap=27):
    """Where to put `count` tokens inside `rect` so they don't sit on top of each other."""
    columns = 1 if count == 1 else (2 if rect.width < rect.height else 3)
    rows = math.ceil(count / columns)
    spots = []
    for i in range(count):
        column = i % columns
        row = i // columns
        x = rect.centerx + (column - (columns - 1) / 2) * gap
        y = rect.centery + (row - (rows - 1) / 2) * gap
        spots.append((int(x), int(y)))
    return spots


class BoardView:
    def __init__(self, game):
        self.game = game
        self.picture = draw_board_picture(game.board)

    def draw(self, surface):
        shadow(surface, BOARD, radius=4, offset=8, alpha=90)
        surface.blit(self.picture, BOARD.topleft)
        self.draw_tokens(surface)

    def draw_tokens(self, surface):
        # Group players by the space they're on: {0: [ann, ben], 7: [cat]}
        crowds = {}
        for player in self.game.players:
            if not player.bankrupt:
                crowds.setdefault(player.position, []).append(player)

        pulse = 3 + 2 * math.sin(pygame.time.get_ticks() / 150)
        current = self.game.current_player()

        for index, players in crowds.items():
            rect = space_rect(index)
            for player, spot in zip(players, spots_in(rect, len(players))):
                if player is current:
                    pygame.draw.circle(surface, theme.WHITE, spot, 16 + pulse, 2)
                token(surface, player, spot)
```

> `crowds.setdefault(key, [])` means: give me the list for this key, and if there isn't one yet, make an empty one first.
> `zip(a, b)` walks through two lists side by side: the 1st player with the 1st spot, the 2nd with the 2nd, and so on.

## Check it

- [ ] "+ Add" goes up to 6 players and "Remove" goes down to 2
- [ ] Start is grey if a name is empty, or two names are the same
- [ ] Start shows everyone's token on Go, and one of them has a pulsing ring (it's their turn)
- [ ] Try it with 6 players. Do they all fit on Go?

## Save

Commit message: `Quest 10: setup screen and tokens`
