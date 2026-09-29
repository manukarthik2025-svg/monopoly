# Quest 12 · The sidebar

**Goal:** the right side of the screen shows every player's cash, whose turn it is, the dice, the right buttons, and a log of what's happening.
**New file:** `ui/sidebar.py` **Changed:** `ui/play_screen.py`

## Idea: the screen *asks* the game

The sidebar never decides anything. Every frame it asks the game: whose turn is it? What phase? What are the dice? Then it draws the answers. Buttons just call a rule, like `game.roll()`, and the rule decides whether anything happens.

So the rules stay in `logic/`, and the screen just shows them.

## Do it

1. Create `ui/sidebar.py`:

```python
"""The right-hand side of the play screen: players, dice, buttons and the log."""
import pygame

from logic.game import END_TURN, ROLL
from ui import theme
from ui.draw import money, panel, paragraph, text, token
from ui.widgets import Button

LEFT = 900
WIDTH = 678

PIPS = {
    1: [(0, 0)],
    2: [(-1, -1), (1, 1)],
    3: [(-1, -1), (0, 0), (1, 1)],
    4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
    5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],
    6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)],
}


def draw_die(surface, value, rect):
    panel(surface, rect, theme.WHITE, radius=12)
    pygame.draw.rect(surface, theme.LIGHT_GREY, rect, 2, border_radius=12)
    spacing = rect.width // 4
    for dx, dy in PIPS.get(value, []):
        center = (rect.centerx + dx * spacing, rect.centery + dy * spacing)
        pygame.draw.circle(surface, theme.INK, center, rect.width // 11)


def describe(game):
    """One sentence telling the players what to do right now."""
    if game.phase == ROLL:
        return "Roll the dice!"
    if game.phase == END_TURN:
        return "All done. Click End turn."
    return ""


class Sidebar:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen      # the PlayScreen, for things like opening popups
        self.roll_button = Button("Roll dice", screen.roll, color=theme.GREEN, size=22)
        self.end_button = Button("End turn", screen.end_turn, color=theme.BLUE, size=22)
        self.menu_button = Button("Menu", screen.quit_to_menu, color=theme.GREY, size=18)

        # Stack the panels under the player cards (2 players per row).
        rows = (len(game.players) + 1) // 2
        self.turn_panel = pygame.Rect(LEFT, 22 + rows * 96 + 8, WIDTH, 268)
        toolbar_y = self.turn_panel.bottom + 16
        self.menu_button.rect = pygame.Rect(LEFT + 460, toolbar_y, 218, 50)
        log_top = toolbar_y + 70
        self.log_panel = pygame.Rect(LEFT, log_top, WIDTH, 878 - log_top)

    def main_buttons(self):
        """The big buttons, which change depending on what's happening."""
        if self.game.phase == ROLL:
            return [self.roll_button]
        if self.game.phase == END_TURN:
            return [self.end_button]
        return []

    def all_buttons(self):
        return self.main_buttons() + [self.menu_button]

    def update(self):
        """Work out where the big buttons go."""
        x = self.turn_panel.x + 24
        for button in self.main_buttons():
            button.rect = pygame.Rect(x, self.turn_panel.bottom - 80, 200, 58)
            x += 214

    def handle_event(self, event):
        # Space bar clicks the first big button.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            buttons = self.main_buttons()
            if buttons and buttons[0].enabled:
                buttons[0].on_click()
            return
        for button in self.all_buttons():
            if button.handle_event(event):
                return

    def draw(self, surface):
        self.draw_players(surface)
        self.draw_turn_panel(surface)
        for button in self.all_buttons():
            button.draw(surface)
        self.draw_log(surface)

    def draw_players(self, surface):
        for i, player in enumerate(self.game.players):
            column = i % 2
            row = i // 2
            card = pygame.Rect(LEFT + column * 347, 22 + row * 96, 331, 82)
            is_current = player is self.game.current_player()

            panel(surface, card, theme.WHITE, border=player.color if is_current else None)
            token(surface, player, (card.x + 32, card.y + 30), radius=18)
            text(surface, player.name, (card.x + 60, card.y + 12), 21, bold=True)
            text(surface, money(player.cash), (card.right - 16, card.y + 10), 24, theme.GREEN, bold=True,
                 anchor="topright")

    def draw_turn_panel(self, surface):
        panel(surface, self.turn_panel, theme.PAPER)
        player = self.game.current_player()
        token(surface, player, (self.turn_panel.x + 42, self.turn_panel.y + 44), radius=22)
        text(surface, f"{player.name}'s turn", (self.turn_panel.x + 76, self.turn_panel.y + 22), 30, bold=True)
        paragraph(surface, describe(self.game), self.turn_panel.x + 26, self.turn_panel.y + 84, 420, 20, theme.GREY)

        dice = self.game.dice
        for i, value in enumerate(dice):
            draw_die(surface, value, pygame.Rect(self.turn_panel.right - 190 + i * 88, self.turn_panel.y + 26, 74, 74))

    def draw_log(self, surface):
        panel(surface, self.log_panel, (245, 244, 238))
        text(surface, "WHAT'S HAPPENING", (self.log_panel.x + 22, self.log_panel.y + 14), 15, theme.GREY, bold=True)
        room = (self.log_panel.height - 50) // 21      # how many lines fit
        lines = self.game.log[-room:]
        y = self.log_panel.y + 42
        for i, line in enumerate(lines):
            newest = i == len(lines) - 1
            color = theme.INK if newest else (95, 95, 100)
            shown = line if len(line) < 78 else line[:75] + "..."
            text(surface, shown, (self.log_panel.x + 22, y), 17, color, bold=newest)
            y += 21
```

2. Update `ui/play_screen.py`:
   - `from ui.sidebar import Sidebar`
   - in `__init__`: `self.sidebar = Sidebar(game, self)`
   - **delete** the temporary R and E keys from Quest 11
   - add two methods the buttons call:

```python
    def roll(self):
        self.game.roll()

    def end_turn(self):
        self.game.end_turn()
```

   - and hand events, updates and drawing on to the sidebar:

```python
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.quit_to_menu()
            return
        self.sidebar.handle_event(event)

    def update(self, seconds):
        self.sidebar.update()

    def draw(self, surface):
        background(surface)
        self.board_view.draw(surface)
        self.sidebar.draw(surface)
```

## Check it

- [ ] Roll dice → dice show the roll, the token moves, and the log says where it landed
- [ ] The button changes to End turn. Click it and the next player's card lights up.
- [ ] `Space` does the same as clicking the big button
- [ ] Pass Go: cash goes up by $200

## Save

Commit message: `Quest 12: the sidebar`

⭐ **Extra:** the log only shows the newest lines. Could you make the mouse wheel (`pygame.MOUSEWHEEL`) scroll back through older ones?
