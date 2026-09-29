# Quest 17 · Auctions

**Goal:** if you don't buy a property, **everyone** gets to bid on it (including you). The last bidder left wins.
**New files:** `logic/auction.py`, `tests/test_auction.py` **Changed:** `logic/game.py`, `ui/stage.py`, `ui/sidebar.py`, `tests/test_buying.py`

## How our auction works

Players take turns. On your turn you either **raise** the bid (+$1, +$10 or +$100) or **drop out**. Once you drop out you're out. It ends when only the top bidder is left, or when everyone has dropped out and nobody bid (then the bank keeps it).

## Idea: a small class for a small job

The auction has its own state: who's still in, whose turn it is, the highest bid. That lives in its own `Auction` class, in its own file, with its own tests. `Game` just holds one while it's running.

## Do it

1. Create `logic/auction.py`:

```python
class Auction:
    """Players take turns raising the bid or dropping out. Last one in wins."""

    def __init__(self, space, bidders):
        self.space = space
        self.bidders = list(bidders)    # players still in, in turn order
        self.turn = 0                   # index into bidders
        self.high_bid = 0
        self.high_bidder = None

    def whose_turn(self):
        return self.bidders[self.turn]

    def can_raise(self, extra):
        return self.whose_turn().cash >= self.high_bid + extra

    def raise_bid(self, extra):
        if not self.can_raise(extra):
            return
        self.high_bid += extra
        self.high_bidder = self.whose_turn()
        self.turn = (self.turn + 1) % len(self.bidders)

    def drop_out(self):
        self.bidders.pop(self.turn)
        if self.bidders:
            self.turn = self.turn % len(self.bidders)

    def is_over(self):
        pass    # TODO: True if nobody is left, OR one bidder is left and they're the high bidder
```

> Why doesn't `drop_out` move `self.turn` on? Popping someone out of the list slides everyone after them one place left, so the **next** bidder is already sitting at `self.turn`.

2. Create `tests/test_auction.py`:

```python
from helpers import make_game

from logic.auction import Auction
from logic.game import END_TURN
from logic.player import Player


def test_last_bidder_standing_wins():
    ann, ben, cat = Player("Ann"), Player("Ben"), Player("Cat")
    auction = Auction("a street", [ann, ben, cat])
    auction.raise_bid(10)      # Ann bids $10
    auction.drop_out()         # Ben drops out
    auction.raise_bid(50)      # Cat bids $60
    assert not auction.is_over()
    auction.drop_out()         # Ann drops out
    assert auction.is_over()
    assert auction.high_bidder is cat
    assert auction.high_bid == 60


def test_you_cant_bid_more_than_your_cash():
    ann, ben = Player("Ann"), Player("Ben")
    ann.cash = 5
    auction = Auction("a street", [ann, ben])
    auction.raise_bid(10)
    assert auction.high_bid == 0


def test_nobody_bids():
    ann, ben = Player("Ann"), Player("Ben")
    auction = Auction("a street", [ann, ben])
    auction.drop_out()
    assert not auction.is_over()      # Ben could still bid
    auction.drop_out()
    assert auction.is_over()
    assert auction.high_bidder is None


def test_auction_in_a_real_game():
    game = make_game((1, 2))
    ann, ben = game.players
    game.roll()
    game.decline()
    game.bid(1)          # Ann: $1
    game.bid(10)         # Ben: $11
    game.drop_out()      # Ann is out
    assert game.board[3].owner is ben
    assert ben.cash == 1489
    assert game.phase == END_TURN
```

   And add to `tests/test_buying.py` (import `AUCTION` as well):

```python
def test_declining_starts_an_auction():
    game = make_game((1, 2))
    game.roll()
    game.decline()
    assert game.phase == AUCTION
```

3. In `logic/game.py`:
   - `from logic.auction import Auction`
   - a new phase: `AUCTION = "AUCTION"        # an auction is running`
   - in `__init__`: `self.auction = None`
   - replace `decline`, and add the auction rules after it:

```python
    def decline(self):
        if self.phase != BUY:
            return
        player = self.current_player()
        self.say(f"{player.name} didn't buy it, so it goes up for auction")
        self.start_auction(self.board[player.position])

    def start_auction(self, space):
        # Everyone still playing can bid, starting with whoever's turn it is.
        players = self.active_players()
        first = players.index(self.current_player()) if self.current_player() in players else 0
        bidders = players[first:] + players[:first]
        self.auction = Auction(space, bidders)
        self.phase = AUCTION
        self.say(f"Auction for {space.name}!")

    def bid(self, extra):
        if self.auction is None or not self.auction.can_raise(extra):
            return
        bidder = self.auction.whose_turn()
        self.auction.raise_bid(extra)
        self.say(f"{bidder.name} bid ${self.auction.high_bid}")
        self.check_auction()

    def drop_out(self):
        if self.auction is None:
            return
        self.say(f"{self.auction.whose_turn().name} dropped out")
        self.auction.drop_out()
        self.check_auction()

    def check_auction(self):
        auction = self.auction
        if not auction.is_over():
            return
        self.auction = None
        winner = auction.high_bidder
        if winner is None:
            self.say(f"Nobody bid, so the bank keeps {auction.space.name}")
        else:
            pass    # TODO: the winner pays their bid to the BANK, becomes the owner, and say() so
        self.finish_move()
```

4. **The auction on the stage.** In `ui/stage.py`, import `AUCTION`, and `panel` and `token` from `ui.draw`.
   - In `__init__`, add the bidding buttons:

```python
        right = CENTER.x + 330
        self.bid_buttons = [
            Button("+$1", lambda: game.bid(1), (right, CENTER.y + 446, 86, 52), theme.GREEN),
            Button("+$10", lambda: game.bid(10), (right + 94, CENTER.y + 446, 86, 52), theme.GREEN),
            Button("+$100", lambda: game.bid(100), (right + 188, CENTER.y + 446, 86, 52), theme.GREEN),
        ]
        self.drop_out_button = Button("Drop out", game.drop_out, (right, CENTER.y + 506, 274, 52), theme.RED)
```

   (`lambda: game.bid(10)` is a tiny function that calls `game.bid(10)` **later**, when the button is clicked.)

   - In `buttons()`: `if self.game.phase == AUCTION: return self.bid_buttons + [self.drop_out_button]`
   - In `update()`:

```python
        if game.phase == AUCTION:
            for button, extra in zip(self.bid_buttons, (1, 10, 100)):
                button.enabled = game.auction.can_raise(extra)
                button.reason = "Not enough cash"
```

   - In `draw()`, make the auction the **first** thing it checks (the old `if game.phase == BUY:` becomes `elif`):

```python
        if game.phase == AUCTION:
            self.cover(surface)
            self.draw_auction(surface)
```

   - And add:

```python
    def draw_auction(self, surface):
        auction = self.game.auction
        draw_deed(surface, auction.space, (CENTER.x + 160, CENTER.centery))
        box = panel(surface, (CENTER.x + 310, CENTER.y + 30, 314, 570), theme.WHITE)
        text(surface, "AUCTION", (box.centerx, box.y + 16), 28, theme.ORANGE, bold=True, anchor="midtop")
        text(surface, "Highest bid", (box.centerx, box.y + 62), 17, theme.GREY, anchor="midtop")
        text(surface, money(auction.high_bid), (box.centerx, box.y + 82), 44, theme.GREEN, bold=True, anchor="midtop")
        leader = auction.high_bidder.name if auction.high_bidder else "nobody yet"
        text(surface, f"by {leader}", (box.centerx, box.y + 140), 18, theme.GREY, anchor="midtop")

        y = box.y + 180
        for bidder in auction.bidders:
            is_turn = bidder is auction.whose_turn()
            if is_turn:
                pygame.draw.rect(surface, (255, 243, 205), (box.x + 12, y - 4, box.width - 24, 34), border_radius=8)
            token(surface, bidder, (box.x + 34, y + 13), radius=12)
            text(surface, bidder.name, (box.x + 56, y + 2), 19, bold=is_turn)
            text(surface, money(bidder.cash), (box.right - 22, y + 2), 17, theme.GREY, anchor="topright")
            y += 36
```

5. In `ui/sidebar.py`, import `AUCTION`, and add to `describe`:

```python
    if game.phase == AUCTION:
        return f"Auction! {game.auction.whose_turn().name}, raise the bid or drop out."
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Click "Auction it" → the auction panel appears. Take turns bidding and dropping out. The winner pays and owns it.
- [ ] Everyone drops out → the bank keeps it

## Save

Commit message: `Quest 17: auctions`
