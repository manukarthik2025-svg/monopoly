# Quest 34: Bankruptcy and finding a winner

## Why this quest
This is the quest that turns your project from "a thing you can play with" into "a game that actually ends." Two different bankruptcy destinations — another player, or the bank — have different rules for what happens to the loser's stuff.

## Your tasks

1. In `monopoly/rules.py`, write `declare_bankruptcy(state, debtor, creditor)`. `creditor` is either a `Player` or `"BANK"`.
2. **Bankrupt to a player:** transfer all remaining cash, all owned properties (update `.owner` on each), and all held jail cards to the creditor. Mortgaged properties transfer as-is (still mortgaged) — the creditor inherits the choice to unmortgage later, per PLAN.md's rule that mortgage interest must be resolved correctly for the receiver (reuse the same rule you chose in Quest 32's trading).
3. **Bankrupt to the bank:** return every house/hotel on the debtor's properties to the bank supply, set every one of their properties back to unowned and unmortgaged, and queue each one for a fresh auction (reuse `start_auction` from Quest 23, one at a time — you'll need a small queue on `GameState`, e.g. `state.pending_auctions`, processed one after another before the game continues). Held jail cards return to their original decks' discard piles.
4. Either way: set `debtor.bankrupt = True`, clear `state.pending_decision`, and log it clearly.
5. Write `check_for_winner(state)`: if exactly one active (`is_active()`) player remains, set `state.phase = GAME_OVER` and store the winner (e.g. `state.winner = that_player`). Call this after every bankruptcy.
6. Build a simple `WinnerScreen` showing the winner's name and a "New Game"/"Main Menu" choice.
7. Update `advance_turn` (Quest 19) — you already skip bankrupt players there, so double check it still works correctly with 3+ players when one goes bankrupt mid-game.

## Starter code
```python
def declare_bankruptcy(state, debtor, creditor):
    if creditor != "BANK":
        # TODO: give creditor all of debtor's cash, properties (update owner
        # and both .owned lists), and jail_cards
        pass
    else:
        for index in list(debtor.owned):
            space = state.spaces[index]
            state.houses_left += space.houses if space.houses < 5 else 0
            state.hotels_left += 1 if space.houses == 5 else 0
            space.houses = 0
            space.owner = None
            space.mortgaged = False
            # TODO: append space to state.pending_auctions instead of
            # starting the auction immediately (process one at a time)
        debtor.owned = []
        # TODO: return debtor.jail_cards worth of held cards to their decks'
        # discard piles (see state.held_jail_cards from Quest 28), then
        # reset debtor.jail_cards to 0

    debtor.bankrupt = True
    debtor.cash = 0
    state.pending_decision = None
    check_for_winner(state)


def check_for_winner(state):
    active = [p for p in state.players if p.is_active()]
    if len(active) == 1:
        state.winner = active[0]
        state.phase = GAME_OVER
```

Wire the "Declare Bankruptcy" button from Quest 33:
```python
def go_bankrupt(self):
    pending = self.state.pending_decision
    rules.declare_bankruptcy(self.state, pending.debtor, pending.creditor)
    if self.state.phase != rules.GAME_OVER:
        self.state.phase = rules.TURN_END
```

## Test it yourself
Add to `tests/test_bankruptcy.py` (new file):
```python
from monopoly.models import Player, GameState, Space
from monopoly.rules import declare_bankruptcy, check_for_winner

def test_bankrupt_to_player_transfers_everything():
    alice = Player(0, "Alice", "hat")
    bob = Player(1, "Bob", "car")
    space = Space(1, "A", "STREET", group="brown")
    space.owner = 0
    alice.owned = [1]
    alice.cash = 300
    state = GameState([alice, bob], [space])
    declare_bankruptcy(state, alice, bob)
    assert alice.bankrupt is True
    assert space.owner == 1
    assert bob.cash == 1800  # 1500 starting + Alice's 300

def test_bankrupt_to_bank_resets_properties():
    alice = Player(0, "Alice", "hat")
    bob = Player(1, "Bob", "car")
    space = Space(1, "A", "STREET", group="brown", house_cost=50)
    space.owner = 0
    space.houses = 2
    alice.owned = [1]
    state = GameState([alice, bob], [space])
    state.houses_left = 20
    declare_bankruptcy(state, alice, "BANK")
    assert space.owner is None
    assert space.houses == 0
    assert state.houses_left == 22

def test_last_active_player_wins():
    alice = Player(0, "Alice", "hat")
    bob = Player(1, "Bob", "car")
    state = GameState([alice, bob], [Space(0, "Go", "GO")])
    bob.bankrupt = True
    check_for_winner(state)
    assert state.phase == "GAME_OVER"
    assert state.winner is alice
```
Run `python -m pytest tests/test_bankruptcy.py -v`. Then play a full manual game to bankruptcy at least once — the real test is that the game reaches `WinnerScreen` cleanly.

## Checkpoint
```text
git commit -m "Implement bankruptcy to players and the bank, and winner detection"
```
You've now hit PLAN.md's Milestone 5 exit criterion: a full game can eliminate players and end with exactly one winner.

## Stuck? Try this
- Bankrupt-to-bank leaves properties still marked as owned → confirm you set `space.owner = None` for *every* property in `debtor.owned`, not just the first one — a `for` loop over `list(debtor.owned)` (a copy) is safer than looping over `debtor.owned` while also modifying it.
- Game never reaches `GAME_OVER` → call `check_for_winner` right after every bankruptcy, not just at the end of a turn.
