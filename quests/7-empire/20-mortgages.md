# Quest 20 · Mortgages

**Goal:** a "My properties" popup where you can mortgage property for quick cash, and pay it back later.
**New files:** `logic/buildings.py`, `ui/assets_popup.py`, `tests/test_buildings.py` **Changed:** `logic/game.py`, `ui/play_screen.py`, `ui/sidebar.py`, `ui/board_view.py`

## The rules

- **Mortgage:** the bank gives you half the price. The property then charges **no rent**.
- **Unmortgage:** pay back that amount **plus 10%**.
- You can't mortgage a street while any street of its colour has buildings on it (houses come next quest).

## Idea: "why can't I?" functions

Every rule in `buildings.py` comes as a pair:

```python
why_cant_mortgage(game, space)   # returns a reason like "It's already mortgaged", or None if you can
mortgage(game, space)            # does it, but only if why_cant_mortgage said None
```

The button uses the reason as its tooltip, and is enabled when the reason is `None`. The rule is written **once**, in `logic/`, and the screen just asks it.

## Idea: `partial`

Each row of the popup needs a button that calls `mortgage(game, this_space)`. `partial(buildings.mortgage, game, space)` makes a brand-new function that calls exactly that when the button is clicked. It's like `lambda`, but clearer when there are arguments.

## Do it

1. Create `logic/buildings.py`:

```python
from logic.board import group_of
from logic.game import BANK

# Each "why_cant_..." function returns a reason (a string) if you're NOT allowed,
# or None if you are. The buttons show the reason when you hover over them.


def why_cant_mortgage(game, space):
    if space.mortgaged:
        return "It's already mortgaged"
    if any(other.houses > 0 for other in group_of(space, game.board)):
        return "Sell the buildings in this colour first"
    return None


def mortgage(game, space):
    if why_cant_mortgage(game, space):
        return
    game.transfer(BANK, space.owner, space.mortgage_value(), f"mortgaging {space.name}")
    space.mortgaged = True


def unmortgage_cost(space):
    return space.mortgage_value() + space.mortgage_value() // 10     # plus 10% interest


def why_cant_unmortgage(game, space):
    pass    # TODO: "It isn't mortgaged" / "Not enough cash" / None


def unmortgage(game, space):
    if why_cant_unmortgage(game, space):
        return
    # TODO: the owner pays unmortgage_cost(space) to the BANK, and it's not mortgaged any more
```

2. Create `tests/test_buildings.py`:

```python
from helpers import make_game

from logic.buildings import mortgage, unmortgage, unmortgage_cost


def browns_for_ann():
    game = make_game()
    ann = game.players[0]
    game.board[1].owner = ann
    game.board[3].owner = ann
    return game, ann, game.board[1], game.board[3]


def test_mortgage_and_unmortgage():
    game, ann, med, baltic = browns_for_ann()
    mortgage(game, med)
    assert med.mortgaged
    assert ann.cash == 1530
    assert unmortgage_cost(med) == 33
    unmortgage(game, med)
    assert not med.mortgaged
    assert ann.cash == 1497
```

3. In `logic/game.py`, add at the end of the class:

```python
    # ---------- what's allowed right now ----------

    def can_manage_properties(self):
        return self.phase in (ROLL, JAIL, BUY, END_TURN)
```

   (Not in the middle of an auction, for example.)

4. Create `ui/assets_popup.py`. Next quest adds Build and Sell buttons to each row.

```python
"""The "My properties" popup: build, sell, mortgage and unmortgage."""
from functools import partial

import pygame

from logic import buildings
from logic.board import properties_of
from logic.rent import rent_for
from ui import theme
from ui.draw import money, panel, text
from ui.widgets import Button

BOX = pygame.Rect(40, 36, 1520, 828)
ROW_HEIGHT = 46


class AssetsPopup:
    def __init__(self, screen, player):
        self.screen = screen
        self.game = screen.game
        self.player = player
        self.rows = []
        for i, space in enumerate(properties_of(player, self.game.board)):
            x = BOX.x + 30 + (i // 14) * 750
            y = BOX.y + 110 + (i % 14) * ROW_HEIGHT
            # partial(f, a, b) makes a new function that calls f(a, b) later, when the button is clicked.
            row = {
                "space": space,
                "y": y,
                "x": x,
                "mortgage": Button("", partial(buildings.mortgage, self.game, space), (x + 558, y, 150, 38),
                                   theme.BLUE, 15),
                "unmortgage": Button("", partial(buildings.unmortgage, self.game, space), (x + 558, y, 150, 38),
                                     theme.PURPLE, 15),
            }
            self.rows.append(row)
        self.done_button = Button("Done", screen.close_popup, (BOX.right - 190, BOX.y + 24, 160, 52), theme.GREY)

    def row_buttons(self, row):
        if row["space"].mortgaged:
            return [row["unmortgage"]]
        return [row["mortgage"]]

    def update_buttons(self):
        for row in self.rows:
            space = row["space"]
            row["mortgage"].label = "Mortgage +" + money(space.mortgage_value())
            row["mortgage"].reason = buildings.why_cant_mortgage(self.game, space)
            row["unmortgage"].label = "Unmortgage " + money(buildings.unmortgage_cost(space))
            row["unmortgage"].reason = buildings.why_cant_unmortgage(self.game, space)
            for button in self.row_buttons(row):
                button.enabled = button.reason is None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.screen.close_popup()
            return
        self.update_buttons()
        self.done_button.handle_event(event)
        for row in self.rows:
            for button in self.row_buttons(row):
                button.handle_event(event)

    def draw(self, surface):
        self.update_buttons()
        panel(surface, BOX, theme.PAPER)
        text(surface, f"{self.player.name}'s properties", (BOX.x + 30, BOX.y + 22), 34, bold=True)
        text(surface, f"Cash: {money(self.player.cash)}", (BOX.x + 32, BOX.y + 68), 18, theme.GREY)
        self.done_button.draw(surface)

        if not self.rows:
            text(surface, "You don't own anything yet. Land on a property and buy it!", BOX.center, 24,
                 theme.GREY, anchor="center")

        for row in self.rows:
            space = row["space"]
            x, y = row["x"], row["y"]
            chip = pygame.Rect(x, y + 3, 14, 32)
            pygame.draw.rect(surface, theme.GROUP_COLORS[space.group], chip, border_radius=3)
            text(surface, space.name, (x + 24, y + 1), 18, bold=True)
            text(surface, self.status(space), (x + 24, y + 22), 14, theme.GREY)
            for button in self.row_buttons(row):
                button.draw(surface)

    def status(self, space):
        if space.mortgaged:
            return "Mortgaged - no rent"
        if space.houses == 5:
            buildings_text = "hotel"
        elif space.houses > 0:
            buildings_text = f"{space.houses} house" + ("s" if space.houses > 1 else "")
        else:
            buildings_text = "no buildings"
        rent = rent_for(space, self.game.board, 7)
        if space.kind == "UTILITY":
            return f"Rent: {rent // 7} x dice roll"
        return f"{buildings_text}, rent {money(rent)}"
```

5. **Popups in the play screen.** A popup sits on top of everything, and while it's open it gets **all** the clicks. In `ui/play_screen.py`:
   - `from ui.assets_popup import AssetsPopup`, and add `dim` to the `ui.draw` import
   - in `__init__`: `self.popup = None`
   - add:

```python
    def open_properties(self):
        self.popup = AssetsPopup(self, self.game.current_player())

    def close_popup(self):
        self.popup = None
```

   - at the very start of `handle_event`:

```python
        if self.popup is not None:
            self.popup.handle_event(event)
            return
```

   - in `draw`, don't show hover deeds under a popup, and draw the popup last:

```python
        hovered = self.board_view.space_under_mouse() if self.popup is None else None
        self.stage.draw(surface, hovered)
        self.sidebar.draw(surface)
        if self.popup is not None:
            dim(surface)
            self.popup.draw(surface)
```

6. **A button to open it.** In `ui/sidebar.py`:

```python
        self.properties_button = Button("My properties", screen.open_properties, color=theme.PURPLE, size=18)
```

   Put it in the toolbar row with Menu. Replace the `self.menu_button.rect = ...` line with:

```python
        for i, button in enumerate([self.properties_button, None, self.menu_button]):
            if button:
                button.rect = pygame.Rect(LEFT + i * 230, toolbar_y, 218, 50)
```

   (The `None` saves a gap for the Trade button in Quest 25.) Add it to `all_buttons`: `self.main_buttons() + [self.properties_button, self.menu_button]`, and in `update`:

```python
        self.properties_button.enabled = self.game.can_manage_properties()
        self.properties_button.reason = "Not right now"
```

   Mortgaged property chips should look grey. In `draw_players`, change the chip colour line to:

```python
                color = theme.LIGHT_GREY if space.mortgaged else theme.GROUP_COLORS[space.group]
                pygame.draw.rect(surface, color, chip, border_radius=2)
```

7. **Show mortgages on the board.** In `ui/board_view.py`, in the `for space in self.game.board:` loop in `draw`:

```python
            if space.mortgaged:
                self.draw_mortgaged(surface, space)
```

```python
    def draw_mortgaged(self, surface, space):
        rect = space_rect(space.index)
        cover = pygame.Surface(rect.size, pygame.SRCALPHA)
        cover.fill((40, 40, 40, 120))
        surface.blit(cover, rect)
        words = theme.font(10, True).render("MORTGAGED", True, theme.WHITE)
        banner = pygame.Surface((words.get_width() + 10, words.get_height() + 2))
        banner.fill(theme.RED)
        banner.blit(words, (5, 1))
        if rect.width < rect.height:          # tall, thin space: run the banner up the middle
            banner = pygame.transform.rotate(banner, 90)
        surface.blit(banner, banner.get_rect(center=rect.center))
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Buy something, open My properties, mortgage it → +cash, a red banner on the board, and a grey chip
- [ ] Someone lands on it → "no rent" in the log
- [ ] Unmortgage costs 10% more than you got

## Save

Commit message: `Quest 20: mortgages`
