# Quest 22 · Debt

**Goal:** if you owe more than you have, the game **stops** and makes you raise the money (sell houses, mortgage) before anything else can happen.
**Changed:** `logic/game.py`, `ui/sidebar.py`, `ui/play_screen.py`, `ui/stage.py`, `tests/test_money.py`

## The bug we're fixing

Right now, rent you can't afford just makes your cash go negative. That isn't allowed in Monopoly.

## Idea: a debt is a note that says "you still owe this"

`charge()` is like `transfer()`, but careful: if you can afford it, it pays. If you can't, it writes a `Debt` into the list `game.debts` instead. While that list isn't empty:
- nobody can roll or end their turn
- the player in debt (maybe **not** the current player, think of the birthday card!) gets **Pay** and property buttons

`transfer()` stays for money that must always move (like the bank paying you). `charge()` is for money someone might not have.

## Do it

1. In `logic/game.py`, add a class above `Game`:

```python
class Debt:
    """Money someone has to pay but can't afford yet."""

    def __init__(self, debtor, creditor, amount, reason):
        self.debtor = debtor        # a Player
        self.creditor = creditor    # a Player, or BANK
        self.amount = amount
        self.reason = reason
```

   In `__init__`: `self.debts = []`

   After `transfer`, add:

```python
    def charge(self, payer, amount, receiver, reason):
        """Like transfer, but if the payer can't afford it, it becomes a debt."""
        if payer.cash >= amount:
            self.transfer(payer, receiver, amount, reason)
        else:
            self.debts.append(Debt(payer, receiver, amount, reason))
            self.say(f"{payer.name} owes ${amount} but only has ${payer.cash}!")

    def pay_debt(self):
        if not self.debts:
            return
        debt = self.debts[0]
        # TODO: if the debtor still can't afford it, return
        self.debts.pop(0)
        self.transfer(debt.debtor, debt.creditor, debt.amount, debt.reason)
```

   And after `current_player`:

```python
    def acting_player(self):
        """Who is making decisions right now: someone in debt, or whoever's turn it is."""
        if self.debts:
            return self.debts[0].debtor
        return self.current_player()
```

2. Nobody moves on while there's a debt. Change the first lines of `roll` and `end_turn`:

```python
        if self.phase != ROLL or self.debts:
```

```python
        if self.phase != END_TURN or self.debts:
```

3. Now go hunting. Change `transfer` to `charge` **everywhere a player might not have the money.** Careful: the order of the arguments is different! `charge(payer, amount, receiver, reason)`. There are 6 places:
   - `land()`: tax
   - `pay_rent()`: rent
   - `roll_in_jail()`: the bail after the third failed try
   - `draw_card()`: `MONEY` cards that cost money, both halves of `EACH_PLAYER`, and `REPAIRS`

   For example, tax becomes:

```python
            self.charge(player, space.price, BANK, space.name)
```

4. **Tests.** Add to `tests/test_money.py`:

```python
def test_charge_you_cant_afford_becomes_a_debt():
    game = make_game()
    ann, ben = game.players
    ann.cash = 50
    game.charge(ann, 100, ben, "rent")
    assert ann.cash == 50
    assert len(game.debts) == 1


def test_paying_a_debt_after_raising_money():
    game = make_game()
    ann, ben = game.players
    ann.cash = 50
    game.charge(ann, 100, ben, "rent")
    ann.cash = 150
    game.pay_debt()
    assert ann.cash == 50
    assert ben.cash == 1600
    assert game.debts == []


def test_cant_end_turn_while_in_debt():
    game = make_game((1, 3))
    game.players[0].cash = 100
    game.roll()                       # Income Tax: $200
    game.end_turn()
    assert game.current_player().name == "Ann"
```

5. **Sidebar.** In `ui/sidebar.py`, import `name_of` from `logic.game` as well.
   - a new button: `self.pay_debt_button = Button("Pay debt", game.pay_debt, color=theme.GREEN)`
   - debts come **first** in `main_buttons`:

```python
        if self.game.debts:
            return [self.pay_debt_button]
```

   - in `update`:

```python
        if self.game.debts:
            debt = self.game.debts[0]
            self.pay_debt_button.label = f"Pay {money(debt.amount)}"
            self.pay_debt_button.enabled = debt.debtor.cash >= debt.amount
            self.pay_debt_button.reason = "Not enough cash yet"
```

   - first thing in `describe`, after `player = ...`:

```python
    if game.debts:
        debt = game.debts[0]
        return (f"{debt.debtor.name} owes {money(debt.amount)} to {name_of(debt.creditor)}. "
                "Sell or mortgage something to raise the cash, or go bankrupt.")
```

   - in `draw_turn_panel`, show the person in debt instead:

```python
        player = self.game.acting_player()
        token(surface, player, (self.turn_panel.x + 42, self.turn_panel.y + 44), radius=22)
        text(surface, f"{player.name}'s turn" if not self.game.debts else f"{player.name} is in debt",
             (self.turn_panel.x + 76, self.turn_panel.y + 22), 30, bold=True)
```

6. The popup should open for whoever has to act. In `ui/play_screen.py`, `open_properties` uses `self.game.acting_player()`.

7. In `ui/stage.py`, you can't buy while someone owes money. Add `and not game.debts` to the end of the Buy button's `enabled` line.

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Temporarily start a player with $20 (in `logic/player.py`) and land on tax → the sidebar says they owe money, and Pay stays grey until they mortgage something
- [ ] Put the $1500 back!

## Save

Commit message: `Quest 22: debts`
