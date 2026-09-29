# Quest 25 · The trade screen

**Goal:** a Trade popup. Pick who to trade with, click properties and cash onto each side, then the other player gets to Accept or Reject.
**New file:** `ui/trade_popup.py` **Changed:** `ui/sidebar.py`, `ui/play_screen.py`

## How it works

One screen, two people. You build the offer, click **Offer trade**, then pass the mouse to the other player. They see *"Ben, do you accept this trade?"* and click Accept or Reject.

Everything it needs already exists: `Trade`, `why_cant_trade` and `do_trade` from last quest. The popup just lets you fill in a `Trade` by clicking.

## Do it

1. Create `ui/trade_popup.py`:

```python
"""The Trade popup: build an offer, then the other player accepts or rejects it."""
from functools import partial

import pygame

from logic.board import properties_of
from logic.trade import Trade, do_trade, why_cant_trade
from ui import theme
from ui.draw import money, panel, text, token
from ui.widgets import Button

BOX = pygame.Rect(40, 36, 1520, 828)
SIDE_WIDTH = 720
CHIP_SIZE = (230, 34)


class TradePopup:
    def __init__(self, screen, player):
        self.screen = screen
        self.game = screen.game
        self.me = player
        self.answering = False            # False while building the offer, True while the partner decides
        others = [other for other in self.game.active_players() if other is not player]
        self.partner_buttons = []
        for i, other in enumerate(others):
            spot = (BOX.x + 260 + i * 160, BOX.y + 24, 150, 46)
            self.partner_buttons.append(Button(other.name, partial(self.choose, other), spot, other.color, 18))
        self.cancel_button = Button("Cancel", screen.close_popup, (BOX.right - 180, BOX.y + 24, 150, 46), theme.GREY)
        self.offer_button = Button("Offer trade", self.offer, (BOX.centerx - 130, BOX.bottom - 84, 260, 58),
                                   theme.GREEN, 22)
        self.accept_button = Button("Accept", self.accept, (BOX.centerx - 230, BOX.bottom - 84, 220, 58), theme.GREEN, 22)
        self.reject_button = Button("Reject", self.reject, (BOX.centerx + 10, BOX.bottom - 84, 220, 58), theme.RED, 22)
        self.choose(others[0])

    def choose(self, partner):
        """Start a fresh offer with this partner."""
        self.trade = Trade(self.me, partner)
        self.chips = []                   # (space, offer, rect) for every clickable property
        self.side_buttons = []
        for column, offer in enumerate((self.trade.a, self.trade.b)):
            left = BOX.x + 30 + column * (SIDE_WIDTH + 40)
            for i, space in enumerate(properties_of(offer.player, self.game.board)):
                rect = pygame.Rect(left + (i % 3) * 240, BOX.y + 250 + (i // 3) * 42, *CHIP_SIZE)
                self.chips.append((space, offer, rect))
            for i, amount in enumerate((-100, -10, 10, 100)):
                label = f"+{amount}" if amount > 0 else str(amount)
                spot = (left + 240 + i * 80, BOX.y + 150, 72, 42)
                self.side_buttons.append(Button(label, partial(self.change_cash, offer, amount), spot, theme.BLUE, 16))
            if offer.player.jail_cards:
                spot = (left + 560, BOX.y + 196, 150, 38)
                self.side_buttons.append(Button("Jail card", partial(self.toggle_jail_card, offer), spot, theme.PURPLE, 15))

    def change_cash(self, offer, amount):
        offer.cash = max(0, min(offer.player.cash, offer.cash + amount))

    def toggle_jail_card(self, offer):
        offer.jail_cards = 0 if offer.jail_cards else 1

    def offer(self):
        self.answering = True

    def accept(self):
        do_trade(self.game, self.trade)
        self.screen.close_popup()

    def reject(self):
        self.game.say(f"{self.trade.b.player.name} said no to the trade")
        self.screen.close_popup()

    def buttons(self):
        if self.answering:
            return [self.accept_button, self.reject_button]
        return self.partner_buttons + self.side_buttons + [self.cancel_button, self.offer_button]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.screen.close_popup()
            return
        for button in self.buttons():
            if button.handle_event(event):
                return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.answering:
            for space, offer, rect in self.chips:
                if rect.collidepoint(event.pos):
                    pass    # TODO: if space is already in offer.properties, remove it; otherwise add it

    def draw(self, surface):
        problem = why_cant_trade(self.game, self.trade)
        self.offer_button.enabled = problem is None
        self.offer_button.reason = problem

        panel(surface, BOX, theme.PAPER)
        text(surface, "Trade with", (BOX.x + 30, BOX.y + 30), 30, bold=True)
        for button in self.buttons():
            button.draw(surface)

        for column, offer in enumerate((self.trade.a, self.trade.b)):
            left = BOX.x + 30 + column * (SIDE_WIDTH + 40)
            token(surface, offer.player, (left + 20, BOX.y + 112), radius=18)
            text(surface, f"{offer.player.name} gives", (left + 48, BOX.y + 96), 26, bold=True)
            text(surface, f"Cash: {money(offer.cash)}", (left, BOX.y + 158), 24, theme.GREEN, bold=True)
            text(surface, f"(has {money(offer.player.cash)})", (left, BOX.y + 190), 15, theme.GREY)
            if offer.jail_cards:
                text(surface, "+ a Get Out of Jail Free card", (left + 240, BOX.y + 204), 17, theme.PURPLE, bold=True)
            text(surface, "Click properties to add them:", (left, BOX.y + 222), 15, theme.GREY)
        pygame.draw.line(surface, theme.LIGHT_GREY, (BOX.centerx, BOX.y + 90), (BOX.centerx, BOX.bottom - 110), 2)

        for space, offer, rect in self.chips:
            picked = space in offer.properties
            pygame.draw.rect(surface, (220, 235, 255) if picked else theme.WHITE, rect, border_radius=6)
            pygame.draw.rect(surface, theme.BLUE if picked else theme.LIGHT_GREY, rect, 3 if picked else 1,
                             border_radius=6)
            pygame.draw.rect(surface, theme.GROUP_COLORS[space.group], (rect.x + 6, rect.y + 6, 10, rect.height - 12))
            name = space.name + (" (M)" if space.mortgaged else "")
            text(surface, name, (rect.x + 24, rect.centery), 15, bold=picked, anchor="midleft")

        if self.answering:
            partner = self.trade.b.player
            text(surface, f"{partner.name}, do you accept this trade?", (BOX.centerx, BOX.bottom - 130), 26,
                 theme.INK, bold=True, anchor="center")
        elif problem:
            text(surface, problem, (BOX.centerx, BOX.bottom - 110), 18, theme.RED, anchor="center")
```

2. In `ui/play_screen.py`, `from ui.trade_popup import TradePopup` and:

```python
    def open_trade(self):
        self.popup = TradePopup(self, self.game.acting_player())
```

3. In `ui/sidebar.py`:
   - `self.trade_button = Button("Trade", screen.open_trade, color=theme.ORANGE, size=18)`
   - the toolbar loop gets its third button, so the `None` goes:

```python
        for i, button in enumerate([self.properties_button, self.trade_button, self.menu_button]):
            button.rect = pygame.Rect(LEFT + i * 230, toolbar_y, 218, 50)
```

   - `all_buttons` returns `self.main_buttons() + [self.properties_button, self.trade_button, self.menu_button]`
   - in `update`:

```python
        self.trade_button.enabled = self.game.can_manage_properties()
        self.trade_button.reason = "Not right now"
```

## Check it

- [ ] Trade → swap a street for $100 → Offer → Accept. The owner strip on the board changes colour.
- [ ] Try something impossible (a street with houses on its colour). The Offer button explains why not.
- [ ] Reject → nothing changes

## Save

Commit message: `Quest 25: the trade screen`
