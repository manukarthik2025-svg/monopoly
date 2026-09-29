# Quest 23 · Bankruptcy and winning

**Goal:** a player who can't pay goes bankrupt. When only one player is left, a winner screen!
**New file:** `ui/popups.py`, `tests/test_bankruptcy.py` **Changed:** `logic/game.py`, `ui/play_screen.py`, `ui/sidebar.py`, `ui/screens.py`

## The rules

When you go bankrupt, everything you own goes to whoever you owed:

- **You owed a player:** your buildings are sold to the bank for half price, then **all** your cash, properties and jail cards go to that player. (Mortgaged ones cost them 10% interest.)
- **You owed the bank:** buildings go back to the bank, and **every** property you had is auctioned, one after another.

Then you're out. When only one player is left, they win.

## Do it

1. In `logic/game.py`:
   - a new phase: `GAME_OVER = "GAME_OVER"`
   - in `__init__`: `self.auctions_waiting = []` and `self.winner = None`
   - `finish_move` now starts any waiting auctions first, and bankrupt players never roll again:

```python
    def finish_move(self):
        """This roll is completely sorted out. What happens next?"""
        if self.auctions_waiting:
            self.start_auction(self.auctions_waiting.pop(0))
            return
        player = self.current_player()
        if self.roll_again and not player.in_jail and not player.bankrupt:
            self.phase = ROLL
        else:
            self.phase = END_TURN
```

   - a helper after `pay_debt`, for giving a property to someone else (trading will use it too):

```python
    def hand_over(self, space, new_owner):
        """Give a property to someone else. Mortgaged ones cost the new owner 10% interest."""
        space.owner = new_owner
        if space.mortgaged:
            interest = space.mortgage_value() // 10
            self.charge(new_owner, interest, BANK, f"interest on mortgaged {space.name}")
```

   - and a whole new section before `can_manage_properties`:

```python
    # ---------- bankruptcy ----------

    def go_bankrupt(self):
        if not self.debts:
            return
        debt = self.debts[0]
        player = debt.debtor
        # Forget every debt this player owes or is owed. They're out.
        self.debts = [d for d in self.debts if d.debtor is not player and d.creditor is not player]

        if debt.creditor == BANK:
            self.bankrupt_to_bank(player)
        else:
            self.bankrupt_to_player(player, debt.creditor)
        player.bankrupt = True
        player.in_jail = False
        self.say(f"{player.name} is bankrupt!")

        survivors = self.active_players()
        if len(survivors) == 1:
            pass    # TODO: set self.winner, empty auctions_waiting, set the phase to GAME_OVER,
                    #       say who won, and return
        if player is self.current_player():
            self.roll_again = False
        self.finish_move()

    def remove_buildings(self, space):
        """Put every building on this space back in the bank's supply."""
        if space.houses == 5:
            self.hotels_left += 1
        else:
            self.houses_left += space.houses
        space.houses = 0

    def bankrupt_to_bank(self, player):
        for space in properties_of(player, self.board):
            self.remove_buildings(space)
            space.owner = None
            space.mortgaged = False
            self.auctions_waiting.append(space)
        for card in player.jail_cards:
            self.decks[card["deck"]].put_back(card)
        player.jail_cards = []
        player.cash = 0

    def bankrupt_to_player(self, player, creditor):
        # Buildings are sold back to the bank for half price first.
        for space in properties_of(player, self.board):
            if space.houses > 0:
                value = space.houses * space.house_cost // 2
                self.remove_buildings(space)
                self.transfer(BANK, player, value, f"selling buildings on {space.name}")
        self.transfer(player, creditor, player.cash, "bankruptcy")
        for space in properties_of(player, self.board):
            self.hand_over(space, creditor)
        creditor.jail_cards.extend(player.jail_cards)
        player.jail_cards = []
```

2. Create `tests/test_bankruptcy.py`:

```python
from helpers import make_game

from logic.game import AUCTION, BANK, GAME_OVER


def test_bankrupt_to_another_player():
    game = make_game(players=3)
    ann, ben, cat = game.players
    game.board[1].owner = ann
    ann.cash = 30
    game.charge(ann, 100, ben, "rent")
    game.go_bankrupt()
    assert ann.bankrupt
    assert game.board[1].owner is ben
    assert ben.cash == 1530


def test_bankrupt_to_the_bank_auctions_everything():
    game = make_game(players=3)
    ann = game.players[0]
    game.board[1].owner = ann
    game.board[1].houses = 2
    game.houses_left = 30
    ann.cash = 30
    game.charge(ann, 200, BANK, "tax")
    game.go_bankrupt()
    assert game.board[1].owner is None
    assert game.houses_left == 32
    assert game.phase == AUCTION


def test_last_player_standing_wins():
    game = make_game()
    ann, ben = game.players
    ann.cash = 0
    game.charge(ann, 100, ben, "rent")
    game.go_bankrupt()
    assert game.phase == GAME_OVER
    assert game.winner is ben
```

3. **"Are you sure?"** Going bankrupt can't be undone, so it asks first. Create `ui/popups.py`:

```python
"""Small boxes that pop up over the game."""
import pygame

from ui import theme
from ui.draw import panel, text, text_block
from ui.widgets import Button


class ConfirmPopup:
    """Asks a yes/no question. Runs on_yes only if they click Yes."""

    def __init__(self, screen, question, on_yes):
        self.screen = screen
        self.question = question
        self.on_yes = on_yes
        self.box = pygame.Rect(0, 0, 560, 250)
        self.box.center = (theme.WIDTH // 2, theme.HEIGHT // 2)
        self.yes_button = Button("Yes", self.yes, (self.box.centerx - 170, self.box.bottom - 86, 160, 56), theme.RED)
        self.no_button = Button("No", screen.close_popup, (self.box.centerx + 10, self.box.bottom - 86, 160, 56),
                                theme.GREY)

    def yes(self):
        self.screen.close_popup()
        self.on_yes()

    def handle_event(self, event):
        self.yes_button.handle_event(event)
        self.no_button.handle_event(event)

    def draw(self, surface):
        panel(surface, self.box, theme.PAPER)
        text_block(surface, self.question, self.box.centerx, self.box.y + 40, self.box.width - 80, 24, bold=True)
        self.yes_button.draw(surface)
        self.no_button.draw(surface)
```

4. In `ui/play_screen.py`, `from ui.popups import ConfirmPopup` and `from logic.game import GAME_OVER`. Then:

```python
    def confirm_bankrupt(self):
        player = self.game.acting_player()
        self.popup = ConfirmPopup(self, f"Really go bankrupt? {player.name} will be out of the game.",
                                  self.game.go_bankrupt)
```

   and at the end of `update`:

```python
        if self.game.phase == GAME_OVER:
            from ui.screens import WinnerScreen
            self.app.go_to(WinnerScreen(self.app, self.game))
```

5. In `ui/sidebar.py`:
   - `self.bankrupt_button = Button("Go bankrupt", screen.confirm_bankrupt, color=theme.RED)`
   - the debts line in `main_buttons` returns `[self.pay_debt_button, self.bankrupt_button]`
   - in `draw_players`, bankrupt players get a grey card. Put this straight after `is_current = ...`:

```python
            if player.bankrupt:
                panel(surface, card, (200, 200, 200))
                text(surface, player.name, (card.x + 20, card.centery), 20, theme.GREY, bold=True, anchor="midleft")
                text(surface, "BANKRUPT", (card.right - 20, card.centery), 18, theme.RED, bold=True, anchor="midright")
                continue
```

6. The winner screen. In `ui/screens.py`, import `from logic.board import properties_of` and add `money` to the `ui.draw` import. Add at the bottom:

```python
class WinnerScreen:
    def __init__(self, app, game):
        self.app = app
        self.game = game
        self.buttons = [
            Button("Play again", self.play_again, (MIDDLE - 330, 740, 300, 64), theme.GREEN, 24),
            Button("Main menu", self.menu, (MIDDLE + 30, 740, 300, 64), theme.BLUE, 24),
        ]

    def play_again(self):
        self.app.go_to(SetupScreen(self.app))

    def menu(self):
        self.app.go_to(MenuScreen(self.app))

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self, seconds):
        pass

    def draw(self, surface):
        background(surface)
        winner = self.game.winner
        box = panel(surface, (MIDDLE - 400, 90, 800, 610), theme.PAPER)
        token(surface, winner, (MIDDLE, box.y + 80), radius=50)
        text(surface, f"{winner.name} wins!", (MIDDLE, box.y + 140), 60, bold=True, anchor="midtop")

        y = box.y + 250
        for player in self.game.players:
            token(surface, player, (box.x + 150, y + 16), radius=16)
            text(surface, player.name, (box.x + 180, y), 26, bold=True)
            if player.bankrupt:
                result = "bankrupt"
            else:
                owned = len(properties_of(player, self.game.board))
                result = f"{money(player.cash)} and {owned} properties"
            text(surface, result, (box.right - 150, y + 2), 24, theme.GREY, anchor="topright")
            y += 54
        for button in self.buttons:
            button.draw(surface)
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Two players, one with $20 (temporarily!). Make them owe money, click Go bankrupt → Yes → the winner screen appears.
- [ ] Three players: the bankrupt one is skipped from then on

## Save

Commit message: `Quest 23: bankruptcy and a winner`

**The full game of Monopoly now works.** Everything after this makes it nicer to play.
