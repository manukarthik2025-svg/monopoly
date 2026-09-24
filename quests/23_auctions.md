# Quest 23: Auction a declined property

## Why this quest
Standard Monopoly rules require every unwanted property to go to auction, open to all players including the one who declined it. This is one of the rules people often get wrong when building Monopoly from scratch — you're going to get it right.

## Your tasks

1. In `monopoly/models.py`, add an `AuctionState` class: `space`, `bidders` (list of active player_ids still in the auction), `current_bid` (starts at `0`), `leader` (starts `None`).
2. In `monopoly/rules.py`, write `start_auction(state, space)`: create an `AuctionState` with every active player as a bidder, store it on `state.pending_decision`, set `state.phase = AUCTION`.
3. Write `place_bid(state, player, amount)`: only valid if `amount > auction.current_bid` and `player.cash >= amount`; update `current_bid` and `leader`.
4. Write `pass_auction(state, player)`: remove `player.player_id` from `bidders`.
5. Write `auction_is_over(auction)`: `True` if only one bidder remains, or zero bidders remain and no bid was ever placed.
6. Write `finish_auction(state)`: if there's a `leader`, they pay the bank `current_bid` and receive the property (reuse `buy_property`'s ownership-transfer logic, but for the winning bid amount, not the listed price); if nobody ever bid, the property stays with the bank. Either way, clear `pending_decision` and set `state.phase = TURN_END`.
7. Build a simple auction dialog UI: current highest bid and leader, a "Bid" button that raises the bid by a fixed increment (e.g. 10) for the *current player only* keeping it simple for a first version — a full any-player-can-bid-anytime UI is a stretch goal — and a "Pass" button. After each bid/pass, check `auction_is_over` and call `finish_auction` if so.

## Starter code

Add to `monopoly/models.py`:
```python
class AuctionState:
    def __init__(self, space, bidders):
        self.space = space
        self.bidders = bidders  # list of player_id
        self.current_bid = 0
        self.leader = None
```

Add to `monopoly/rules.py`:
```python
AUCTION = "AUCTION"  # add to your phase constants if not already there

def start_auction(state, space):
    bidder_ids = [p.player_id for p in state.players if p.is_active()]
    state.pending_decision = AuctionState(space, bidder_ids)
    state.phase = AUCTION
    state.log(f"Auction started for {space.name}")


def place_bid(state, player, amount):
    auction = state.pending_decision
    if amount <= auction.current_bid or amount > player.cash:
        return False
    # TODO: set auction.current_bid = amount, auction.leader = player.player_id,
    # log it, return True
    pass


def pass_auction(state, player):
    auction = state.pending_decision
    if player.player_id in auction.bidders:
        auction.bidders.remove(player.player_id)
        state.log(f"{player.name} passes on the auction")


def auction_is_over(auction):
    if auction.leader is not None and len(auction.bidders) <= 1:
        return True
    # TODO: also return True if bidders is empty and no bid was ever placed
    return False


def finish_auction(state):
    auction = state.pending_decision
    if auction.leader is not None:
        winner = next(p for p in state.players if p.player_id == auction.leader)
        pay(state, winner, "BANK", auction.current_bid, f"won auction for {auction.space.name}")
        auction.space.owner = winner.player_id
        winner.owned.append(auction.space.index)
        state.log(f"{winner.name} wins {auction.space.name} for {auction.current_bid}")
    else:
        state.log(f"No bids — {auction.space.name} stays with the bank")
    state.pending_decision = None
    state.phase = TURN_END
```

Make sure `GameScreen.decline()` (Quest 22) now calls `rules.start_auction(self.state, self.current_space())` instead of just setting the phase directly.

## Test it yourself
Add to `tests/test_auctions.py`:
```python
from monopoly.models import Player, GameState, Space
from monopoly.rules import start_auction, place_bid, pass_auction, auction_is_over, finish_auction

def test_auction_with_no_bids_stays_with_bank():
    players = [Player(0, "Alice", "hat"), Player(1, "Bob", "car")]
    space = Space(1, "Baltic Avenue", "STREET", price=60)
    state = GameState(players, [space])
    start_auction(state, space)
    pass_auction(state, players[0])
    pass_auction(state, players[1])
    assert auction_is_over(state.pending_decision)
    finish_auction(state)
    assert space.owner is None

def test_auction_winner_pays_bid_not_list_price():
    players = [Player(0, "Alice", "hat"), Player(1, "Bob", "car")]
    space = Space(1, "Baltic Avenue", "STREET", price=60)
    state = GameState(players, [space])
    start_auction(state, space)
    place_bid(state, players[0], 10)
    pass_auction(state, players[1])
    assert auction_is_over(state.pending_decision)
    finish_auction(state)
    assert space.owner == 0
    assert players[0].cash == 1490
```
Run `python -m pytest tests/test_auctions.py -v`. Then play manually and confirm declining a purchase always ends in either a sale or the property staying with the bank — never a stuck game.

## Checkpoint
```text
git commit -m "Add property auctions"
```
Declining a property is no longer a dead end — it's a real, testable rule.

## Stuck? Try this
- Auction never ends → double check `auction_is_over` handles both endings: someone leading with everyone else passed, *and* everyone passing with nobody ever bidding.
- Winner charged the listed price instead of their bid → check `finish_auction` uses `auction.current_bid`, not `auction.space.price`.
