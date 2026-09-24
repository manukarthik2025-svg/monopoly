# Quest 09: The GameState class

## Why this quest
Right now "players" and "the board" are separate things floating around. The real game needs one object that holds *everything about the current match* — whose turn it is, what phase the game is in, the dice, the history log. This is the object every rule function from here on will read from and change.

## Your tasks

1. In `monopoly/models.py`, add a `GameState` class below `Space`.
2. Store: `players` (a list of `Player` objects), `spaces` (a list of 40 `Space` objects), `current_player_index` (starts at `0`), `phase` (starts at the string `"TURN_START"`), `dice` (starts at `(0, 0)`), `doubles_count` (starts at `0`), `houses_left` (starts at `32`), `hotels_left` (starts at `12`), `history` (an empty list of message strings), `pending_decision` (starts at `None`).
3. Add a method `current_player(self)` that returns the `Player` object whose turn it is right now.
4. Add a method `log(self, message)` that appends `message` to `self.history`.

## Starter code
```python
class GameState:
    def __init__(self, players, spaces):
        self.players = players
        self.spaces = spaces
        self.current_player_index = 0
        self.phase = "TURN_START"
        self.dice = (0, 0)
        self.doubles_count = 0
        self.houses_left = 32
        self.hotels_left = 12
        self.history = []
        self.pending_decision = None

    def current_player(self):
        # TODO: return self.players at self.current_player_index
        pass

    def log(self, message):
        # TODO: append message to self.history
        pass
```

## Test it yourself
Temporarily add and run:
```python
players = [Player(0, "Alice", "hat"), Player(1, "Bob", "car")]
spaces = [Space(0, "Go", "GO")]
state = GameState(players, spaces)
print(state.current_player().name)   # Alice
state.log("Game started")
print(state.history)                  # ['Game started']
```
Remove this test code afterward.

## Checkpoint
```text
git commit -m "Add GameState class to hold the whole match"
```
This one object is the "save file in memory" — everything about a running game lives inside it, which is exactly what makes Quest 35 (save/load) possible later.

## Stuck? Try this
- `IndexError: list index out of range` on `current_player()` → check `current_player_index` isn't larger than the number of players you created.
- Forgot why `phase` is a plain string like `"TURN_START"` instead of a number → strings are self-explanatory when you print them for debugging (`"TURN_START"` tells you something immediately; `0` doesn't). Later you'll see all the phase names collected together in `rules.py`.
