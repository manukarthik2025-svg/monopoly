# Quest 05 · Screens

**Goal:** a proper main menu and a Rules screen, and a way to switch between them.
**New file:** `ui/screens.py` **Changed:** `ui/app.py`, `ui/draw.py`

## Idea: same methods, different objects

The game will have a menu, a setup screen, a rules screen, the game itself and a winner screen. Each one is a class with the **same three methods**:

```python
def handle_event(self, event): ...   # a click or a key press
def update(self, seconds): ...       # change things (seconds = time since the last frame)
def draw(self, surface): ...         # paint yourself
```

`App` keeps whichever screen is showing in `self.screen` and calls those three methods, without caring **which** screen it is. To switch screens: `self.app.go_to(OtherScreen(...))`.

## Do it

1. Add two text helpers to `ui/draw.py`:

```python
def wrap(words, size, max_width, bold=False):
    """Split words into lines that each fit inside max_width pixels."""
    lines = []
    line = ""
    for word in str(words).split():
        attempt = word if line == "" else line + " " + word
        if theme.font(size, bold).size(attempt)[0] <= max_width:
            line = attempt
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def paragraph(surface, words, x, y, max_width, size=18, color=theme.INK):
    """Draw wrapped, left-aligned lines of text. Returns the y just below the last line."""
    for line in wrap(words, size, max_width):
        text(surface, line, (x, y), size, color)
        y += size + size // 3
    return y
```

2. Create `ui/screens.py`. The menu is the buttons from Quest 04, moved into their own class.

```python
"""The screens that aren't the main game: menu, setup, rules and the winner."""
import math

import pygame

from ui import theme
from ui.draw import background, make_logo, panel, paragraph, text
from ui.widgets import Button

MIDDLE = theme.WIDTH // 2


class MenuScreen:
    def __init__(self, app):
        self.app = app
        x = MIDDLE - 150
        self.continue_button = Button("Continue", self.continue_game, (x, 520, 300, 62), theme.BLUE, 24)
        self.continue_button.enabled = False      # Quest 26 makes saved games work
        self.buttons = [
            Button("New game", self.new_game, (x, 440, 300, 62), theme.GREEN, 24),
            self.continue_button,
            Button("Rules", self.show_rules, (x, 600, 300, 62), theme.PURPLE, 24),
            Button("Quit", self.quit, (x, 680, 300, 62), theme.RED, 24),
        ]
        self.logo = make_logo(640)
        self.time = 0

    def new_game(self):
        print("New game! (Quest 08 makes this do something)")

    def continue_game(self):
        pass

    def show_rules(self):
        self.app.go_to(RulesScreen(self.app, back_to=self))

    def quit(self):
        self.app.running = False

    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return

    def update(self, seconds):
        self.time += seconds

    def draw(self, surface):
        background(surface)
        wobble = math.sin(self.time * 1.5) * 2      # the logo gently tilts back and forth
        logo = pygame.transform.rotozoom(self.logo, wobble, 1)
        surface.blit(logo, logo.get_rect(center=(MIDDLE, 250)))
        text(surface, "a game by Manu", (MIDDLE, 350), 26, theme.WHITE, anchor="center")
        for button in self.buttons:
            button.draw(surface)
        text(surface, "F11: full screen", (MIDDLE, theme.HEIGHT - 30), 16, theme.LIGHT_GREY, anchor="center")


RULES = [
    ("The goal", "Be the last player who isn't bankrupt."),
    ("Your turn", "Roll the dice and move. Doubles means roll again, but three doubles in a row sends you to jail."),
    ("Go", "Collect $200 every time you pass Go."),
    ("Buying", "Land on an unowned property to buy it. If you don't, everyone bids for it in an auction."),
    ("Rent", "Land on someone else's property and you pay them rent. Owning a whole colour doubles the rent."),
    ("Houses", "Own every street of a colour to build houses. Build evenly. After 4 houses you can build a hotel."),
    ("Mortgages", "Mortgage a property to get half its price from the bank. It earns no rent until you pay it back plus 10%."),
    ("Jail", "In jail you can pay $50, use a Get Out of Jail Free card, or try for doubles. After 3 tries you must pay."),
    ("Cards", "Chance and Community Chest cards can move you, pay you or make you pay."),
    ("Debt", "If you can't pay, sell houses or mortgage property. If that's still not enough, you're bankrupt."),
    ("Trading", "Swap properties, cash and jail cards with other players at any time on your turn."),
    ("Free Parking", "Nothing happens on Free Parking. It's just a rest!"),
]


class RulesScreen:
    def __init__(self, app, back_to):
        self.app = app
        self.back_to = back_to          # the screen to return to
        self.back_button = Button("Back", self.back, (30, 30, 120, 50), theme.GREY)

    def back(self):
        pass    # TODO: go back to self.back_to

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.back()
            return
        self.back_button.handle_event(event)

    def update(self, seconds):
        pass

    def draw(self, surface):
        background(surface)
        box = panel(surface, (180, 40, 1240, 820), theme.PAPER)
        text(surface, "How to play", (box.centerx, box.y + 26), 40, bold=True, anchor="midtop")
        for i, (title, words) in enumerate(RULES):
            x = box.x + 50 + (i % 2) * 590
            y = box.y + 110 + (i // 2) * 116
            text(surface, title, (x, y), 22, theme.RED, bold=True)
            paragraph(surface, words, x, y + 32, 540)
        self.back_button.draw(surface)
```

3. Make `App` hand everything to `self.screen`. In `ui/app.py`:
   - add `from ui.screens import MenuScreen`
   - remove the logo, the buttons, `new_game` and `quit` from `App` (they live in `MenuScreen` now)
   - delete the imports `App` doesn't use any more. VS Code shows them greyed out.
   - at the end of `__init__`: `self.screen = MenuScreen(self)`
   - add the method:

```python
    def go_to(self, screen):
        self.screen = screen
```

   - make `run()` look like this:

```python
    def run(self):
        while self.running:
            seconds = self.clock.tick(60) / 1000     # time since the last frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                else:
                    self.screen.handle_event(event)

            self.screen.update(seconds)
            self.screen.draw(self.window)
            pygame.display.flip()

        pygame.quit()
```

## Check it

- [ ] The logo gently rocks from side to side
- [ ] Rules → the rules screen. Back (or `Esc`) → the menu again.
- [ ] Quit still works

## Save

Commit message: `Quest 05: menu and rules screens`

⭐ **Extra:** add your own house rule to `RULES`.
