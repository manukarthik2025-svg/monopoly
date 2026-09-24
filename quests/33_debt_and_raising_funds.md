# Quest 33: Owing more than you have

## Why this quest
Right now, if `pay()` is called and the payer can't afford it, cash silently goes negative. Real Monopoly has a whole process for this: pause the game, let the player sell/mortgage/trade to raise funds, and only then either finish the payment or declare bankruptcy.

## Your tasks

1. Add a new phase `PAYMENT_REQUIRED`.
2. In `monopoly/models.py`, add a `PendingPayment` class: `debtor`, `creditor` (a `Player` or `"BANK"`), `amount`, `reason`.
3. Write `rules.require_payment(state, debtor, creditor, amount, reason)`: if `debtor.cash >= amount`, just call `pay()` immediately as before — no need to interrupt the game for a debt the player can already cover. Otherwise, store a `PendingPayment` on `state.pending_decision` and set `state.phase = PAYMENT_REQUIRED`.
4. Every place that currently calls `pay()` directly for rent, tax, or forced bail should switch to `require_payment` instead — check `resolve_space`, `apply_card`, and jail handling from earlier quests.
5. While `state.phase == PAYMENT_REQUIRED`, allow the debtor to use the Asset Manager (mortgage/sell buildings) and propose trades, same as any other time — nothing about those screens needs to change, since they already just check ownership.
6. Add a "Pay Now" button, enabled once `debtor.cash >= pending.amount`, and a "Declare Bankruptcy" button, always enabled during this phase. "Pay Now" calls `pay()` with the stored details and returns to `TURN_END`. Bankruptcy is Quest 34.

## Starter code
```python
class PendingPayment:
    def __init__(self, debtor, creditor, amount, reason):
        self.debtor = debtor
        self.creditor = creditor
        self.amount = amount
        self.reason = reason
```

```python
PAYMENT_REQUIRED = "PAYMENT_REQUIRED"

def require_payment(state, debtor, creditor, amount, reason):
    if debtor.cash >= amount:
        pay(state, debtor, creditor, amount, reason)
        return
    # TODO: create a PendingPayment, store it on state.pending_decision,
    # set state.phase to PAYMENT_REQUIRED, and log that a payment is required
```

```python
def resolve_pending_payment(state):
    pending = state.pending_decision
    if state.current_player().cash < pending.amount:
        return False  # not enough yet — caller should keep them in PAYMENT_REQUIRED
    pay(state, pending.debtor, pending.creditor, pending.amount, pending.reason)
    state.pending_decision = None
    state.phase = TURN_END
    return True
```

## Test it yourself
Add to `tests/test_payments.py` (new file):
```python
from monopoly.models import Player, GameState, Space
from monopoly.rules import require_payment, resolve_pending_payment, PAYMENT_REQUIRED

def test_affordable_payment_happens_immediately():
    player = Player(0, "Alice", "hat")
    other = Player(1, "Bob", "car")
    state = GameState([player, other], [Space(0, "Go", "GO")])
    require_payment(state, player, other, 100, "rent")
    assert player.cash == 1400
    assert state.phase != PAYMENT_REQUIRED

def test_unaffordable_payment_pauses_the_game():
    player = Player(0, "Alice", "hat")
    player.cash = 50
    other = Player(1, "Bob", "car")
    state = GameState([player, other], [Space(0, "Go", "GO")])
    require_payment(state, player, other, 100, "rent")
    assert state.phase == PAYMENT_REQUIRED
    assert player.cash == 50  # unchanged until they can actually pay

def test_resolving_after_raising_funds():
    player = Player(0, "Alice", "hat")
    player.cash = 50
    other = Player(1, "Bob", "car")
    state = GameState([player, other], [Space(0, "Go", "GO")])
    require_payment(state, player, other, 100, "rent")
    player.cash = 200  # pretend they mortgaged something
    assert resolve_pending_payment(state) is True
    assert player.cash == 100
```
Run `python -m pytest tests/test_payments.py -v`.

## Checkpoint
```text
git commit -m "Add mandatory-payment mode and fund-raising flow"
```
No player can ever have their cash silently go negative from here on — this is the safety net that makes bankruptcy (next quest) a deliberate, correct event instead of a symptom of a bug.

## Stuck? Try this
- Rent/tax immediately triggers bankruptcy even when the player could raise funds → confirm you're calling `require_payment`, not `pay`, everywhere debt might occur, and that the game genuinely waits in `PAYMENT_REQUIRED` rather than auto-resolving.
- "Pay Now" is clickable when it shouldn't be → its `disabled` check must compare *current* cash, recalculated every frame, against `pending.amount` — not a value cached from when the debt started.
