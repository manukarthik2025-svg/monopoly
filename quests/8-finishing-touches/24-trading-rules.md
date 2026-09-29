# Quest 24 · Trading rules

**Goal:** the rules for swapping properties, cash and jail cards between two players, tested before there's any screen for it.
**New files:** `logic/trade.py`, `tests/test_trade.py`

## The rules

- Each side can offer cash, properties and Get Out of Jail Free cards.
- You can only offer what you actually have.
- You can't trade a street if **any** street of its colour has buildings. Sell them first.
- Getting a mortgaged property costs you 10% interest straight away (that's `hand_over` from Quest 23).

## Idea: check everything first, then do everything

A trade must happen **completely or not at all**. If it failed halfway (Ann's street moved but Ben's cash didn't), money would vanish. So `why_cant_trade` checks every single thing first, and `do_trade` only runs once there's nothing left that could go wrong.

## Do it

1. Create `logic/trade.py`:

```python
from logic.board import group_of


class Offer:
    """What one player puts on the table in a trade."""

    def __init__(self, player):
        self.player = player
        self.cash = 0
        self.properties = []
        self.jail_cards = 0

    def is_empty(self):
        return self.cash == 0 and not self.properties and self.jail_cards == 0


class Trade:
    def __init__(self, player_a, player_b):
        self.a = Offer(player_a)
        self.b = Offer(player_b)


def why_cant_trade(game, trade):
    if trade.a.is_empty() and trade.b.is_empty():
        return "Nothing is being traded yet"
    for offer in (trade.a, trade.b):
        player = offer.player
        if offer.cash > player.cash:
            return f"{player.name} doesn't have ${offer.cash}"
        if offer.jail_cards > len(player.jail_cards):
            return f"{player.name} doesn't have that many jail cards"
        for space in offer.properties:
            # TODO: if player doesn't own this space, return f"{player.name} doesn't own {space.name}"
            if any(other.houses > 0 for other in group_of(space, game.board)):
                return f"Sell the buildings on {space.name}'s colour first"
    return None


def do_trade(game, trade):
    if why_cant_trade(game, trade):
        return False
    a = trade.a.player
    b = trade.b.player
    # Cash first, so nobody spends money on mortgage interest that they just traded away.
    game.transfer(a, b, trade.a.cash, "a trade")
    game.transfer(b, a, trade.b.cash, "a trade")
    for space in trade.a.properties:
        game.hand_over(space, b)
    for space in trade.b.properties:
        game.hand_over(space, a)
    for _ in range(trade.a.jail_cards):
        b.jail_cards.append(a.jail_cards.pop())
    for _ in range(trade.b.jail_cards):
        a.jail_cards.append(b.jail_cards.pop())
    game.say(f"{a.name} and {b.name} made a trade")
    return True
```

2. Create `tests/test_trade.py`, then run it. One test fails until you finish the TODO.

```python
from helpers import make_game

from logic.trade import Trade, do_trade, why_cant_trade


def test_swap_a_street_for_cash():
    game = make_game()
    ann, ben = game.players
    game.board[1].owner = ann
    trade = Trade(ann, ben)
    trade.a.properties.append(game.board[1])
    trade.b.cash = 100
    assert do_trade(game, trade)
    assert game.board[1].owner is ben
    assert ann.cash == 1600
    assert ben.cash == 1400


def test_cant_trade_what_you_dont_own():
    game = make_game()
    ann, ben = game.players
    trade = Trade(ann, ben)
    trade.a.properties.append(game.board[1])
    assert why_cant_trade(game, trade) is not None


def test_cant_trade_streets_with_buildings():
    game = make_game()
    ann, ben = game.players
    game.board[1].owner = ann
    game.board[3].owner = ann
    game.board[3].houses = 1
    trade = Trade(ann, ben)
    trade.a.properties.append(game.board[1])
    assert why_cant_trade(game, trade) is not None


def test_mortgaged_property_costs_ten_percent():
    game = make_game()
    ann, ben = game.players
    game.board[39].owner = ann
    game.board[39].mortgaged = True
    trade = Trade(ann, ben)
    trade.a.properties.append(game.board[39])
    do_trade(game, trade)
    assert ben.cash == 1480      # 10% of the $200 mortgage value
```

## Check it

- [ ] `python -m pytest`: all passed

## Save

Commit message: `Quest 24: trading rules`
