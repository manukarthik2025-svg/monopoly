# Quest 27 · Juice

**Goal:** the game *feels* good. The dice tumble, tokens hop space by space, and confetti falls on the winner.
**Changed:** `ui/play_screen.py`, `ui/board_view.py`, `ui/sidebar.py`, `ui/stage.py`, `ui/screens.py`

## Idea: the rules decide, the screen catches up

When you click Roll, the **rules** move your token instantly, since `player.position` changes straight away. The **screen** keeps its own `shown_positions`, which hop one space at a time towards the real position. While anything is still moving, the game is **busy**: the buttons wait, and the stage hides the deed so you don't see where you'll land before you get there.

The animation never changes the game, it only shows it. That's why it can't break any rule.

## Do it

1. In `ui/play_screen.py`, under the imports:

```python
DICE_SPIN = 0.5       # seconds the dice tumble for
HOP_TIME = 0.13       # seconds per space when a token moves
```

   In `__init__`:

```python
        self.dice_timer = 0
        self.hop_timer = 0
        # Where each token is DRAWN. It hops towards the real position a space at a time.
        self.shown_positions = {player: player.position for player in game.players}
```

   Start the dice spinning when anyone rolls:

```python
    def roll(self):
        self.game.roll()
        self.dice_timer = DICE_SPIN

    def roll_in_jail(self):
        self.game.roll_in_jail()
        self.dice_timer = DICE_SPIN
```

   Add:

```python
    def is_busy(self):
        """True while the dice are spinning or a token is still hopping."""
        if self.dice_timer > 0:
            return True
        return any(self.shown_positions[p] != p.position for p in self.game.players if not p.bankrupt)
```

```python
    def move_tokens(self, seconds):
        self.hop_timer -= seconds
        if self.hop_timer > 0:
            return
        self.hop_timer = HOP_TIME
        for player in self.game.players:
            shown = self.shown_positions[player]
            steps = (player.position - shown) % 40
            if steps == 0:
                continue
            if player.in_jail or steps > 20:
                # Jumps (to jail, or backwards) happen instantly instead of hopping.
                self.shown_positions[player] = player.position
            else:
                self.shown_positions[player] = (shown + 1) % 40
```

   And replace `update` and `draw`:

```python
    def update(self, seconds):
        self.dice_timer = max(0, self.dice_timer - seconds)
        if self.dice_timer == 0:
            self.move_tokens(seconds)
        self.stage.update(self.is_busy())
        self.sidebar.update()

        if self.game.phase == GAME_OVER and not self.is_busy():
            from ui.screens import WinnerScreen
            delete_save()
            self.app.go_to(WinnerScreen(self.app, self.game))

    def draw(self, surface):
        background(surface)
        self.board_view.draw(surface, self.shown_positions)
        hovered = self.board_view.space_under_mouse() if self.popup is None else None
        self.stage.draw(surface, hovered, self.is_busy())
        self.sidebar.draw(surface)
        if self.popup is not None:
            dim(surface)
            self.popup.draw(surface)
```

   > What's `(player.position - shown) % 40` for? It's how many steps forward the token still has to go, even past Go. If it's more than 20, the player must have jumped (to jail, or back 3), so we don't hop the long way round.

2. In `ui/board_view.py`, `draw` and `draw_tokens` take the shown positions: `def draw(self, surface, shown_positions):`, `self.draw_tokens(surface, shown_positions)`, `def draw_tokens(self, surface, shown_positions):`, and in the crowds loop use `shown_positions[player]` instead of `player.position`.

3. In `ui/sidebar.py`, `import random` at the top. Replace `update`, so nothing can be clicked while the game is busy:

```python
    def update(self):
        """Work out which buttons can be clicked right now, and where the big ones go."""
        game = self.game
        player = game.current_player()
        ready = not self.screen.is_busy()     # not while dice spin or a token hops

        self.roll_button.enabled = ready
        self.end_button.enabled = ready
        self.jail_roll_button.enabled = ready
        self.bankrupt_button.enabled = ready
        self.bail_button.enabled = ready and player.cash >= BAIL
        self.bail_button.reason = "Not enough cash"
        self.card_button.enabled = ready and len(player.jail_cards) > 0
        self.card_button.reason = "You don't have a Get Out of Jail Free card"
        if game.debts:
            debt = game.debts[0]
            self.pay_debt_button.label = f"Pay {money(debt.amount)}"
            self.pay_debt_button.enabled = ready and debt.debtor.cash >= debt.amount
            self.pay_debt_button.reason = "Not enough cash yet"
        self.properties_button.enabled = ready and game.can_manage_properties()
        self.properties_button.reason = "Not right now"
        self.trade_button.enabled = ready and game.can_manage_properties()
        self.trade_button.reason = "Not right now"

        x = self.turn_panel.x + 24
        for button in self.main_buttons():
            button.rect = pygame.Rect(x, self.turn_panel.bottom - 80, 200, 58)
            x += 214
```

   and in `draw_turn_panel`, make the dice tumble:

```python
        dice = self.game.dice
        if self.screen.dice_timer > 0:
            dice = (random.randint(1, 6), random.randint(1, 6))
```

4. In `ui/stage.py`, replace `update` and `draw` so they know when the game is busy:

```python
    def update(self, busy):
        game = self.game
        ready = not busy
        if game.phase == BUY:
            space = game.board[game.current_player().position]
            self.buy_button.label = f"Buy {money(space.price)}"
            self.buy_button.enabled = ready and game.current_player().cash >= space.price and not game.debts
            self.buy_button.reason = "Not enough cash. Mortgage something, or auction it."
            self.auction_button.enabled = ready
        if game.phase == AUCTION:
            for button, extra in zip(self.bid_buttons, (1, 10, 100)):
                button.enabled = ready and game.auction.can_raise(extra)
                button.reason = "Not enough cash"
            self.drop_out_button.enabled = ready

    def draw(self, surface, hovered_space, busy):
        game = self.game
        if game.phase == AUCTION:
            self.cover(surface)
            self.draw_auction(surface)
        elif game.phase == BUY and not busy:
            self.cover(surface)
            space = game.board[game.current_player().position]
            draw_deed(surface, space, (CENTER.centerx, CENTER.y + 250))
            text(surface, "FOR SALE", (CENTER.centerx, CENTER.y + 50), 22, theme.GREY, bold=True, anchor="midtop")
        elif game.last_card is not None and not busy:
            self.cover(surface)
            draw_card(surface, game.last_card, CENTER.center)
        elif hovered_space is not None and hovered_space.can_be_owned():
            self.cover(surface)
            draw_deed(surface, hovered_space, (CENTER.centerx, CENTER.centery - 20))
            owner = hovered_space.owner
            words = f"Owned by {owner.name}" if owner else f"For sale: {money(hovered_space.price)}"
            text(surface, words, (CENTER.centerx, CENTER.centery + 160), 22, theme.INK, bold=True, anchor="midtop")

        for button in self.buttons():
            if game.phase == BUY and busy:
                continue
            button.draw(surface)
```

5. **Confetti!** In `ui/screens.py`, `WinnerScreen` gets 160 falling paper pieces. Each one is a list: `[x, y, speed, colour]`.

```python
    def __init__(self, app, game):
        self.app = app
        self.game = game
        self.confetti = []
        for _ in range(160):
            self.confetti.append([random.uniform(0, theme.WIDTH), random.uniform(-theme.HEIGHT, 0),
                                  random.uniform(60, 160), random.choice(theme.TOKEN_COLORS)])
        self.buttons = [
            Button("Play again", self.play_again, (MIDDLE - 330, 740, 300, 64), theme.GREEN, 24),
            Button("Main menu", self.menu, (MIDDLE + 30, 740, 300, 64), theme.BLUE, 24),
        ]
```

```python
    def update(self, seconds):
        for piece in self.confetti:
            piece[1] += piece[2] * seconds       # fall down
            if piece[1] > theme.HEIGHT:
                piece[1] = -10
```

   and in `draw`, straight after `background(surface)`:

```python
        for x, y, speed, color in self.confetti:
            wiggle = math.sin(y / 30) * 6
            pygame.draw.rect(surface, color, (x + wiggle, y, 8, 14))
```

## Check it

- [ ] Roll → the dice tumble for half a second, then the token hops space by space
- [ ] Buttons wait until it lands. Going to jail is instant.
- [ ] Win a game → confetti

## Save

Commit message: `Quest 27: juice`

⭐ **Extra:** sound! `pygame.mixer.Sound("assets/dice.wav").play()` in `PlayScreen.roll`. Find a free dice sound online, or record your own.
