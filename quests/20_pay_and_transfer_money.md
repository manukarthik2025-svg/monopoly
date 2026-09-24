# Quest 20: One function for all money movement

## Why this quest
Rent, taxes, purchases, trades, bankruptcy — every one of them moves money. PLAN.md is emphatic about this: "centralize all money and asset transfers." If every feature quietly does `player.cash -= amount` in its own way, you will eventually have a bug where money is created or destroyed and you won't know which of ten places caused it. One function, used everywhere, fixes that at the source.

## Your tasks

1. In `monopoly/rules.py`, write `pay(state, payer, receiver, amount, reason)`.
2. `payer` and `receiver` can each be a `Player` object or the string `"BANK"` (the bank has infinite money, so paying the bank just removes cash with no matching addition; receiving from the bank adds cash with no matching subtraction).
3. The function should: subtract `amount` from `payer.cash` if `payer` isn't the bank, add `amount` to `receiver.cash` if `receiver` isn't the bank, and log a clear message via `state.log(...)`.
4. It should NOT check whether the payer can afford it — that check belongs to whatever calls `pay()` (rent, tax, purchases each have different rules for what happens on insufficient funds, which you'll build in later quests). Keep this function simple and unconditional.
5. Every place in your code so far that changes `player.cash` directly (passing Go, for instance) should be rewritten to call `pay()` instead, for consistency.

## Starter code
```python
def pay(state, payer, receiver, amount, reason):
    payer_name = "the bank" if payer == "BANK" else payer.name
    receiver_name = "the bank" if receiver == "BANK" else receiver.name

    if payer != "BANK":
        # TODO: subtract amount from payer.cash
        pass
    if receiver != "BANK":
        # TODO: add amount to receiver.cash
        pass

    state.log(f"{payer_name} paid {amount} to {receiver_name} ({reason})")
```

Update the "passed Go" code from Quest 17 to use it:
```python
if passed_go:
    rules.pay(self.state, "BANK", player, 200, "passed Go")
```

## Test it yourself
Add to `tests/test_money.py` (new file):
```python
from monopoly.models import Player, GameState, Space
from monopoly.rules import pay

def make_state():
    players = [Player(0, "Alice", "hat"), Player(1, "Bob", "car")]
    return GameState(players, [Space(0, "Go", "GO")]), players

def test_pay_between_two_players():
    state, (alice, bob) = make_state()
    pay(state, alice, bob, 50, "test rent")
    assert alice.cash == 1450
    assert bob.cash == 1550

def test_pay_from_bank_only_adds_money():
    state, (alice, bob) = make_state()
    pay(state, "BANK", alice, 200, "passed Go")
    assert alice.cash == 1700

def test_pay_to_bank_only_removes_money():
    state, (alice, bob) = make_state()
    pay(state, alice, "BANK", 100, "tax")
    assert alice.cash == 1400
```
Run `python -m pytest tests/test_money.py -v`. All three should pass, and total money in the two-player tests plus/minus the bank's contribution should always make sense — nothing should vanish or double.

## Checkpoint
```text
git commit -m "Centralize money transfers through a single pay function"
```
Every rent charge, tax, purchase, and trade for the rest of the project routes through this one function — which means every one of them also gets logged automatically for free.

## Stuck? Try this
- `AttributeError: 'str' object has no attribute 'cash'` → you tried to do `payer.cash` without first checking `payer != "BANK"`.
- Cash changes on the wrong player → double check you didn't swap `payer`/`receiver` anywhere you call `pay()`.
