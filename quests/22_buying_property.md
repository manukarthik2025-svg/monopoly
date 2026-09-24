# Quest 22: Buy or decline a property

## Why this quest
`AWAITING_PURCHASE` currently leads nowhere. This quest adds the Buy/Auction choice — the real decision point that makes Monopoly a game instead of a dice-rolling simulator.

## Your tasks

1. In `GameScreen`, add two buttons visible only during `AWAITING_PURCHASE`: "Buy" and "Auction".
2. Disable "Buy" if the current player can't afford the space's `price`.
3. In `monopoly/rules.py`, write `buy_property(state, player, space)`: pay the bank the price, set `space.owner = player.player_id`, add `space.index` to `player.owned`, log it, set phase to `TURN_END`.
4. Wire the "Auction" button (and automatic redirect if the player can't afford it) to set `state.phase = AUCTION` — the actual auction is built in Quest 23, so for now just leave a `# TODO` marking where it plugs in.
5. In `resolve_space`, if the player literally cannot afford the property (`player.cash < space.price`), skip the Buy/Auction choice entirely and go straight to `AUCTION` — a player is never offered a purchase they can't make.

## Starter code

Add to `monopoly/rules.py`:
```python
def buy_property(state, player, space):
    pay(state, player, "BANK", space.price, f"bought {space.name}")
    # TODO: set space.owner to player.player_id, append space.index to
    # player.owned, log it, and set state.phase to TURN_END
```

In `resolve_space`, replace the `if space.owner is None:` branch:
```python
if space.owner is None:
    if player.cash < space.price:
        state.log(f"{player.name} cannot afford {space.name}; going to auction")
        state.phase = AUCTION
    else:
        state.phase = AWAITING_PURCHASE
    return
```

In `monopoly/screens.py`, inside `GameScreen`:
```python
self.buy_button = Button((800, 620, 160, 60), "Buy", on_click=self.buy)
self.auction_button = Button((800, 690, 160, 60), "Auction", on_click=self.decline)

def current_space(self):
    player = self.state.current_player()
    return self.state.spaces[player.position]

def buy(self):
    if self.state.phase != rules.AWAITING_PURCHASE:
        return
    rules.buy_property(self.state, self.state.current_player(), self.current_space())

def decline(self):
    if self.state.phase != rules.AWAITING_PURCHASE:
        return
    self.state.log(f"{self.state.current_player().name} declined to buy {self.current_space().name}")
    self.state.phase = rules.AUCTION  # Quest 23 builds what happens next

def handle_event(self, event):
    # ... existing button handling ...
    awaiting_purchase = self.state.phase == rules.AWAITING_PURCHASE
    self.buy_button.disabled = not awaiting_purchase or self.state.current_player().cash < self.current_space().price
    self.auction_button.disabled = not awaiting_purchase
    self.buy_button.handle_event(event)
    self.auction_button.handle_event(event)
```

## Test it yourself
Add to `tests/test_spaces.py`:
```python
from monopoly.rules import buy_property
from monopoly.models import Player, GameState, Space

def test_buy_property_transfers_ownership_and_cash():
    player = Player(0, "Alice", "hat")
    space = Space(1, "Baltic Avenue", "STREET", price=60)
    state = GameState([player], [space])
    buy_property(state, player, space)
    assert space.owner == 0
    assert 1 in player.owned
    assert player.cash == 1440
```
Run `python -m pytest tests/test_spaces.py -v`. Then play manually: land on an unowned property with enough cash, click Buy, confirm cash drops and the space now shows as owned (you may need a small visual marker — even just a colored border matching the owner's token color is enough for now). Land on it again as the same player and confirm nothing happens (no re-purchase, no rent to yourself).

## Checkpoint
```text
git commit -m "Add property purchase and auction handoff"
```
Property ownership is real now — this unlocks rent, monopolies, and everything built on top of them.

## Stuck? Try this
- Buy button stays enabled when the player can't afford it → check the disabled check compares `cash` against `self.current_space().price`, called fresh every frame, not a stale value from when the phase started.
- Buying twice doesn't get blocked → confirm `resolve_space` only reaches the `space.owner is None` branch when there really is no owner yet; check `buy_property` actually sets `space.owner`.
