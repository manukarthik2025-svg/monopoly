# Quest 14 · Buying

**Goal:** land on a property nobody owns and you can buy it. Taxes cost money too.
**New file:** `ui/stage.py` **Changed:** `logic/game.py`, `ui/play_screen.py`, `ui/sidebar.py`, tests

## Idea: a phase that asks a question

Landing on an unowned property **stops** the turn and asks: buy it or not? So `land()` sets `phase = BUY` and returns. `roll()` sees the phase isn't `MOVING` any more, so it doesn't call `finish_move()`. The game waits. When the player answers, `buy()` (or `decline()`) calls `finish_move()` itself.

That's what the `if self.phase == MOVING:` line in `roll()` was for all along.

## Do it

1. In `logic/game.py`, add the phase:

```python
BUY = "BUY"                # landed on an unowned property: buy it or auction it
```

   and grow `land()`. After the `GO_TO_JAIL` part:

```python
        elif space.kind == "TAX":
            self.transfer(player, BANK, space.price, space.name)
        elif space.can_be_owned():
            if space.owner is None:
                self.phase = BUY
```

2. Add a buying section to `Game`:

```python
    # ---------- buying and auctions ----------

    def buy(self):
        player = self.current_player()
        space = self.board[player.position]
        if self.phase != BUY or player.cash < space.price:
            return
        # TODO: transfer the price from the player to the BANK, and make the player the owner
        self.finish_move()

    def decline(self):
        if self.phase != BUY:
            return
        self.say(f"{self.current_player().name} didn't buy it")    # Quest 17 turns this into an auction
        self.finish_move()
```

3. The middle of the board becomes a **stage** where questions get asked. Create `ui/stage.py`:

```python
"""The middle of the board, where deeds, cards and auctions appear."""
import pygame

from logic.game import BUY
from ui import theme
from ui.board_layout import CENTER
from ui.draw import money, text
from ui.widgets import Button


class Stage:
    def __init__(self, game):
        self.game = game
        middle = CENTER.centerx
        self.buy_button = Button("Buy", game.buy, (middle - 190, CENTER.y + 520, 180, 58), theme.GREEN, 22)
        self.auction_button = Button("Auction it", game.decline, (middle + 10, CENTER.y + 520, 180, 58),
                                     theme.ORANGE, 22)

    def buttons(self):
        if self.game.phase == BUY:
            return [self.buy_button, self.auction_button]
        return []

    def update(self):
        game = self.game
        if game.phase == BUY:
            space = game.board[game.current_player().position]
            self.buy_button.label = f"Buy {money(space.price)}"
            self.buy_button.enabled = game.current_player().cash >= space.price

    def handle_event(self, event):
        for button in self.buttons():
            if button.handle_event(event):
                return True
        return False

    def draw(self, surface):
        game = self.game
        if game.phase == BUY:
            self.cover(surface)
            space = game.board[game.current_player().position]
            text(surface, "FOR SALE", (CENTER.centerx, CENTER.y + 50), 22, theme.GREY, bold=True, anchor="midtop")
            text(surface, space.name, CENTER.center, 40, bold=True, anchor="center")
        for button in self.buttons():
            button.draw(surface)

    def cover(self, surface):
        """Fade out the logo so whatever's on the stage stands out."""
        layer = pygame.Surface(CENTER.size, pygame.SRCALPHA)
        layer.fill((*theme.BOARD_GREEN, 215))
        surface.blit(layer, CENTER)
```

4. In `ui/play_screen.py`: `from ui.stage import Stage`, then `self.stage = Stage(game)` in `__init__`, and:

```python
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.quit_to_menu()
            return
        if self.stage.handle_event(event):
            return
        self.sidebar.handle_event(event)

    def update(self, seconds):
        self.stage.update()
        self.sidebar.update()

    def draw(self, surface):
        background(surface)
        self.board_view.draw(surface)
        self.stage.draw(surface)
        self.sidebar.draw(surface)
```

5. In `ui/sidebar.py`, import `BUY`, and add to `describe`:

```python
    if game.phase == BUY:
        space = game.board[player.position]
        return f"Buy {space.name} for {money(space.price)}, or put it up for auction."
```

6. **Tests.** Create `tests/test_buying.py`:

```python
from helpers import make_game

from logic.game import BUY, END_TURN


def test_landing_on_unowned_property_asks_to_buy():
    game = make_game((1, 2))       # Baltic Avenue
    game.roll()
    assert game.phase == BUY


def test_buying_a_property():
    game = make_game((1, 2))
    ann = game.players[0]
    game.roll()
    game.buy()
    assert game.board[3].owner is ann
    assert ann.cash == 1440
    assert game.phase == END_TURN


def test_you_cant_buy_without_enough_cash():
    game = make_game((1, 2))
    ann = game.players[0]
    ann.cash = 10
    game.roll()
    game.buy()
    assert game.board[3].owner is None


def test_landing_on_your_own_property_does_nothing():
    game = make_game((1, 2))
    ann = game.players[0]
    game.board[3].owner = ann
    game.roll()
    assert ann.cash == 1500
    assert game.phase == END_TURN
```

   And in `tests/test_money.py`:

```python
def test_income_tax():
    game = make_game((1, 3))
    game.roll()
    assert game.players[0].cash == 1300
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Land on a street and the stage asks. Buy → cash goes down. Next time you land there, nothing happens.
- [ ] Land on Income Tax → $200 gone

## Save

Commit message: `Quest 14: buying property`
