# Quest 19 · Cards that move you

**Goal:** every card works: advance to a space, go to the nearest railroad or utility, go back 3, and pay for repairs.
**Changed:** `logic/game.py`, `tests/test_cards.py`

## The tricky rules

- **Advance to X**: always moves *forward*, so if that means passing Go, you collect $200. Then you land on X as normal (so you might buy it, or pay rent).
- **Nearest railroad**: if someone owns it, you pay them **double** rent.
- **Nearest utility**: if someone owns it, you roll the dice and pay them **10 ×** the roll.
- **Go back 3**: backwards, so you never pass Go.
- **Repairs**: pay for every house and hotel you own.

## Idea: an optional extra argument

`land()` needs to know when it's been called because of a "nearest" card, so that rent works differently. Instead of writing a second `land`, it gets an extra argument with a default, `card_rule=None`. Normal landings don't mention it, and the card passes `card_rule="RAILROAD"` or `"UTILITY"`.

## Do it

1. In `logic/game.py`, import `properties_of` from `logic.board` as well. Add two movement helpers after `move_forward`:

```python
    def move_to(self, player, target):
        """Move forward (never backward) until you reach `target`."""
        steps = (target - player.position) % 40
        self.move_forward(player, steps)

    def nearest(self, start, kind):
        """The index of the next space of this kind, going forward from `start`."""
        for steps in range(1, 41):
            index = (start + steps) % 40
            if self.board[index].kind == kind:
                return index
```

> Why `% 40` in `move_to`? From space 36 to space 5: `(5 - 36) % 40` is `9`. Nine steps forward, past Go.

2. Change the first line of `land` to `def land(self, player, card_rule=None):`, and pass it on: `self.pay_rent(player, space, card_rule)`.

   Replace `pay_rent`:

```python
    def pay_rent(self, player, space, card_rule=None):
        if space.mortgaged:
            self.say(f"{space.name} is mortgaged, so there's no rent")
            return
        rent = rent_for(space, self.board, sum(self.dice))
        if card_rule == "RAILROAD":
            rent = rent * 2
        if card_rule == "UTILITY":
            die1, die2 = self.roll_dice()
            self.say(f"{player.name} rolled {die1} and {die2} for the utility")
            rent = (die1 + die2) * 10
        self.transfer(player, space.owner, rent, f"rent on {space.name}")
```

3. In `draw_card`, add the remaining actions before `GO_TO_JAIL`:

```python
        elif action == "MOVE_TO":
            self.move_to(player, card["target"])
            self.land(player)

        elif action == "NEAREST":
            self.move_to(player, self.nearest(player.position, card["kind"]))
            self.land(player, card_rule=card["kind"])

        elif action == "BACK":
            player.position = (player.position - card["steps"]) % 40
            self.land(player)
```

   and one after it:

```python
        elif action == "REPAIRS":
            houses = 0
            hotels = 0
            for space in properties_of(player, self.board):
                pass    # TODO: count it. houses == 5 means one hotel, otherwise add its houses
            cost = houses * card["house"] + hotels * card["hotel"]
            self.transfer(player, BANK, cost, "repairs")
```

4. **Tests.** Add to `tests/test_cards.py`:

```python
def test_advance_to_go():
    game = make_game()
    ann = game.players[0]
    ann.position = 7
    put_card_on_top(game, "Chance", "Advance to Go")
    game.draw_card(ann, game.decks["Chance"])
    assert ann.position == 0
    assert ann.cash == 1700


def test_go_back_three_spaces():
    game = make_game()
    land_on_chance(game, "Go back 3")
    ann = game.players[0]
    assert ann.position == 4
    assert ann.cash == 1300              # landed on Income Tax


def test_nearest_railroad_pays_double():
    game = make_game()
    ann, ben = game.players
    game.board[15].owner = ben
    land_on_chance(game, "nearest Railroad")
    assert ann.position == 15
    assert ben.cash == 1550              # 2 x $25


def test_repairs():
    game = make_game()
    ann = game.players[0]
    game.board[1].owner = ann
    game.board[1].houses = 2
    game.board[3].owner = ann
    game.board[3].houses = 5
    land_on_chance(game, "general repairs")
    assert ann.cash == 1500 - (2 * 25 + 100)
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Play until you draw a card that moves you. The token jumps and the log shows what happened on the new space.

## Save

Commit message: `Quest 19: every card works`
