# Quest 19: End Turn and advance to the next player

## Why this quest
Right now the game reaches `TURN_END` and just... stops. This quest closes the loop: an End Turn button that moves to the next active player and starts their turn, skipping anyone bankrupt.

## Your tasks

1. Add an "End Turn" `Button` to `GameScreen`, enabled only when `state.phase == rules.TURN_END`.
2. Write `rules.advance_turn(state)`: increment `current_player_index` by 1, wrapping around with `%` to the number of players, skipping any player whose `bankrupt` is `True` (there are no bankrupt players yet, but write it correctly now — Quest 34 will need it).
3. After advancing, reset `state.doubles_count = 0` and set `state.phase = rules.WAITING_FOR_ROLL`.
4. Guard against a subtle bug: a player should never be able to click End Turn while a required action (like an unresolved purchase decision) is pending. For now this just means "only enabled during `TURN_END`" — later quests will add more phases this button must respect.
5. Log whose turn it now is.

## Starter code

Add to `monopoly/rules.py`:
```python
def advance_turn(state):
    n = len(state.players)
    next_index = state.current_player_index
    for _ in range(n):
        next_index = (next_index + 1) % n
        if state.players[next_index].is_active():
            break
    state.current_player_index = next_index
    # TODO: reset state.doubles_count to 0 and set state.phase to WAITING_FOR_ROLL
```

In `monopoly/screens.py`:
```python
self.end_turn_button = Button((800, 780, 160, 60), "End Turn", on_click=self.end_turn)

def end_turn(self):
    if self.state.phase != rules.TURN_END:
        return
    rules.advance_turn(self.state)
    self.state.log(f"It's now {self.state.current_player().name}'s turn")
```
Remember to call `self.end_turn_button.handle_event(event)` and update its `.disabled` flag in `handle_event`, and draw it in `draw`, the same pattern as the Roll Dice button.

## Test it yourself
Add to `tests/test_movement.py`:
```python
from monopoly.rules import advance_turn
from monopoly.models import GameState, Space

def test_advance_turn_moves_to_next_player():
    players = [Player(0, "Alice", "hat"), Player(1, "Bob", "car")]
    state = GameState(players, [Space(0, "Go", "GO")])
    advance_turn(state)
    assert state.current_player_index == 1

def test_advance_turn_skips_bankrupt_players():
    players = [Player(0, "Alice", "hat"), Player(1, "Bob", "car"), Player(2, "Cara", "dog")]
    players[1].bankrupt = True
    state = GameState(players, [Space(0, "Go", "GO")])
    advance_turn(state)
    assert state.current_player_index == 2
```
Run `python -m pytest tests/test_movement.py -v`. Then play manually with 3 players and confirm turns cycle in order and the End Turn button is disabled at every phase except `TURN_END`.

## Checkpoint
```text
git commit -m "Implement ending a turn and advancing to the next player"
```
You now have a complete, playable (if bare) turn loop: roll, move, resolve, end turn, repeat — this is Milestone 2's exit criterion from PLAN.md.

## Stuck? Try this
- Turn order skips more players than expected → walk through `advance_turn` on paper with a 2-player game where player 1 is bankrupt; the `for` loop with `break` should stop at the first active player it finds, not keep going.
- Same player goes twice in a row unexpectedly → that's actually correct if they rolled doubles (Quest 18) — check `state.phase` was really `TURN_END` and not still `WAITING_FOR_ROLL` from a double.
