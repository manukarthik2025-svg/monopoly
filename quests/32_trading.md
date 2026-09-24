# Quest 32: Trading between players

## Why this quest
Trading is what makes Monopoly a negotiation game, not just a dice-rolling one. The core coding challenge here isn't the UI — it's making sure a trade either completes entirely or not at all, never halfway.

## Your tasks

1. In `monopoly/models.py`, add a `TradeOffer` class: `from_player`, `to_player`, `from_cash`, `to_cash`, `from_properties` (list of space indexes), `to_properties`, `from_jail_cards`, `to_jail_cards`.
2. In `monopoly/rules.py`, write `validate_trade(state, trade)` returning `None` if legal or a reason string. Checks: both players can afford the cash they're offering; every offered property is actually owned by the offering player; no offered property has `houses > 0` anywhere in its color group (properties with buildings can't be traded — the group's buildings must be sold first); jail card counts offered don't exceed what each player actually holds.
3. Write `execute_trade(state, trade)`: only call this after `validate_trade` returns `None`. Move all cash, properties (update `.owner` and both players' `.owned` lists), and jail cards in one pass — since you validated first, nothing here should ever fail partway through.
4. Note the mortgaged-property interest rule: if a mortgaged property changes hands, PLAN.md requires presenting and resolving the interest obligation to the receiver — a reasonable simplified rule for your first version is that the receiving player must immediately pay the bank the same 10% interest fee as an unmortgage would cost, or the property arrives still mortgaged and rent-free until they choose to unmortgage it normally. Pick one, document your choice as a comment in `execute_trade`, and be consistent.
5. Build a simple `TradeScreen`: pick another active player, add properties/cash/cards to each side with +/- controls, show a live summary, and Accept/Reject buttons for the other player to respond to (since this is a shared-screen game, "the other player" just means handing over the keyboard/mouse and clicking their own Accept button).

## Starter code
```python
class TradeOffer:
    def __init__(self, from_player, to_player):
        self.from_player = from_player
        self.to_player = to_player
        self.from_cash = 0
        self.to_cash = 0
        self.from_properties = []
        self.to_properties = []
        self.from_jail_cards = 0
        self.to_jail_cards = 0
```

```python
def validate_trade(state, trade):
    if trade.from_player.cash < trade.from_cash:
        return f"{trade.from_player.name} can't afford {trade.from_cash}"
    if trade.to_player.cash < trade.to_cash:
        return f"{trade.to_player.name} can't afford {trade.to_cash}"
    for index in trade.from_properties:
        space = state.spaces[index]
        if space.owner != trade.from_player.player_id:
            return f"{trade.from_player.name} doesn't own {space.name}"
        # TODO: check no property in this space's group has houses
    # TODO: repeat the ownership + no-houses checks for trade.to_properties
    # TODO: check trade.from_jail_cards <= trade.from_player.jail_cards, and
    # the same for to_jail_cards
    return None


def execute_trade(state, trade):
    pay(state, trade.from_player, trade.to_player, trade.from_cash, "trade")
    pay(state, trade.to_player, trade.from_player, trade.to_cash, "trade")
    for index in trade.from_properties:
        # TODO: transfer ownership of state.spaces[index] from from_player to to_player
        # (update space.owner, remove index from from_player.owned, add to to_player.owned)
        pass
    # TODO: repeat for trade.to_properties in the opposite direction
    # TODO: move jail cards similarly
```

## Test it yourself
Add to `tests/test_trades.py` (new file):
```python
from monopoly.models import Player, GameState, Space, TradeOffer
from monopoly.rules import validate_trade, execute_trade

def test_valid_trade_moves_everything():
    alice = Player(0, "Alice", "hat")
    bob = Player(1, "Bob", "car")
    space = Space(1, "A", "STREET", group="brown")
    space.owner = 0
    alice.owned = [1]
    state = GameState([alice, bob], [space])

    trade = TradeOffer(alice, bob)
    trade.from_properties = [1]
    trade.to_cash = 100

    assert validate_trade(state, trade) is None
    execute_trade(state, trade)
    assert space.owner == 1
    assert 1 in bob.owned
    assert 1 not in alice.owned
    assert alice.cash == 1600
    assert bob.cash == 1400

def test_cannot_trade_property_you_dont_own():
    alice = Player(0, "Alice", "hat")
    bob = Player(1, "Bob", "car")
    space = Space(1, "A", "STREET", group="brown")
    space.owner = 1  # Bob owns it, not Alice
    state = GameState([alice, bob], [space])
    trade = TradeOffer(alice, bob)
    trade.from_properties = [1]
    assert validate_trade(state, trade) is not None
```
Run `python -m pytest tests/test_trades.py -v`.

## Checkpoint
```text
git commit -m "Add trade validation and execution"
```
Validate-then-execute is a pattern worth remembering beyond this project: never make a change you might have to partially undo.

## Stuck? Try this
- A trade partially completes then errors → that means you're not fully validating first; move any check you find yourself wanting mid-`execute_trade` back into `validate_trade`.
- Properties end up owned by nobody → double check you update `space.owner` to the *new* owner's `player_id`, not just remove it from the old owner's list.
