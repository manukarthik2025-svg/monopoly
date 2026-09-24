# Quest 17: Move the token and pass Go

## Why this quest
Rolling dice should actually move the player's token and pay them for passing Go — the core loop finally does something visible on the board.

## Your tasks

1. In `monopoly/rules.py`, write `move_player(player, spaces_to_move, board_size=40)` that updates `player.position` by `spaces_to_move`, wrapping with `%` (same idea as Practice A), and returns `True` if the player passed or landed on Go (position 0) as a result of this move, `False` otherwise.
2. Write `move_player` so it can tell "passed Go" apart from "started on Go": compare the position *before* and *after* the move.
3. In `GameScreen`, when phase is `MOVING`, call `move_player` with the sum of `state.dice`, and if it returns `True`, add 200 to the current player's cash and log it.
4. After moving, set `state.phase = rules.RESOLVING_SPACE` (what happens on each space type comes in Quest 21 — for now just log the space name landed on and set phase to `TURN_END`).
5. Update `GameScreen.draw` to draw each player's token (a small colored circle or square) at their current space's position, offsetting tokens slightly if multiple players share a space so both are visible.

## Starter code

Add to `monopoly/rules.py`:
```python
def move_player(player, spaces_to_move, board_size=40):
    old_position = player.position
    new_position = (old_position + spaces_to_move) % board_size
    player.position = new_position
    # TODO: return True if this move passed or landed on Go (index 0).
    # Careful: a player already on Go who doesn't move shouldn't count,
    # but wrapping around past space (board_size - 1) back to 0 should.
    pass
```

In `GameScreen`, replace the placeholder from Quest 16's `roll()`/next update with something like:
```python
def update(self):
    if self.state.phase == rules.MOVING:
        player = self.state.current_player()
        total = sum(self.state.dice)
        passed_go = rules.move_player(player, total)
        if passed_go:
            player.cash += 200
            self.state.log(f"{player.name} passed Go and collected 200")
        space = self.state.spaces[player.position]
        self.state.log(f"{player.name} landed on {space.name}")
        self.state.phase = rules.TURN_END
```
(Call `self.screen.update()` each frame from `App.run` if you haven't already wired that up since Quest 04.)

For drawing tokens, in `GameScreen.draw`, after drawing all spaces:
```python
TOKEN_COLORS = [(220, 50, 50), (50, 120, 220), (50, 180, 80),
                (230, 190, 40), (180, 60, 200), (240, 140, 40)]

for i, player in enumerate(self.state.players):
    rect = space_rect(player.position, self.board_rect)
    # TODO: draw a small circle for this player inside `rect`, using
    # TOKEN_COLORS[i], offsetting by a few pixels per player index so
    # tokens sharing a space don't perfectly overlap
```

## Test it yourself
Write `tests/test_movement.py`:
```python
from monopoly.models import Player
from monopoly.rules import move_player

def test_simple_move():
    player = Player(0, "Alice", "hat")
    move_player(player, 7)
    assert player.position == 7

def test_wraps_around_and_passes_go():
    player = Player(0, "Alice", "hat")
    player.position = 38
    passed_go = move_player(player, 5)
    assert player.position == 3
    assert passed_go is True

def test_no_pass_go_without_wrapping():
    player = Player(0, "Alice", "hat")
    player.position = 3
    passed_go = move_player(player, 4)
    assert passed_go is False
```
Run `python -m pytest tests/test_movement.py -v` — all three should pass. Then run the game itself and confirm tokens visibly move around the board each roll, and cash increases by 200 exactly when a token passes Go.

## Checkpoint
```text
git commit -m "Implement movement and passing Go"
```
This is the heartbeat of the whole game — every future space interaction happens right after this step.

## Stuck? Try this
- Passing Go pays 200 every single move, even without wrapping → your comparison is probably checking `new_position == 0` alone, without checking it against `old_position` and whether wrapping actually occurred.
- Token drawn in the wrong place → confirm you're using the *current* `player.position`, not the value from before this turn's move.
