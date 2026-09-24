# Quest 16: A Roll Dice button that actually rolls

## Why this quest
This is where the turn loop starts. You'll introduce the game's phase system for real and wire up the first button that changes game state, not just prints a message.

## New idea(s)
**Phases as plain strings.** A "phase" is just a string telling you what the game is currently waiting for — `state.phase` might be `"WAITING_FOR_ROLL"` or `"TURN_END"`. Instead of scattering true/false flags everywhere, one variable holds exactly one value at a time, and your code checks it with plain `if`/`elif`. Collecting the valid phase names together at the top of a file makes typos obvious (Python will complain about an undefined name) instead of silently comparing against a misspelled string.

```python
TURN_START = "TURN_START"
WAITING_FOR_ROLL = "WAITING_FOR_ROLL"

phase = TURN_START
if phase == WAITING_FOR_ROLL:
    print("waiting...")
else:
    print("not yet")
```

## Your tasks

1. At the top of `monopoly/rules.py`, define these as module-level constants: `TURN_START`, `WAITING_FOR_ROLL`, `MOVING`, `RESOLVING_SPACE`, `WAITING_FOR_DECISION`, `TURN_END`, `GAME_OVER` (each just equal to its own name as a string, like the example above).
2. When a `GameScreen` starts, set `state.phase = rules.WAITING_FOR_ROLL`.
3. Add a "Roll Dice" `Button` to `GameScreen`, enabled only when `state.phase == rules.WAITING_FOR_ROLL`.
4. On click, call `rules.roll_dice()`, store the result in `state.dice`, log it, and set `state.phase = rules.MOVING` (movement itself is next quest — for now just display the dice values).
5. Display the current dice values and the current phase name somewhere on screen — this "debug info" is genuinely useful, not just for you; keep something like it until the game explains itself well enough in the UI (Quest 36).

## Starter code

Add to `monopoly/rules.py` (above the functions from Quest 15):
```python
TURN_START = "TURN_START"
WAITING_FOR_ROLL = "WAITING_FOR_ROLL"
MOVING = "MOVING"
RESOLVING_SPACE = "RESOLVING_SPACE"
WAITING_FOR_DECISION = "WAITING_FOR_DECISION"
TURN_END = "TURN_END"
GAME_OVER = "GAME_OVER"
```

In `monopoly/screens.py`, inside `GameScreen`:
```python
from monopoly import rules

class GameScreen:
    def __init__(self, app, state):
        self.app = app
        self.state = state
        self.state.phase = rules.WAITING_FOR_ROLL
        self.roll_button = Button((800, 700, 160, 60), "Roll Dice", on_click=self.roll)

    def roll(self):
        # TODO: only do anything if self.state.phase == rules.WAITING_FOR_ROLL
        # then call rules.roll_dice(), store it in self.state.dice,
        # log it with self.state.log(...), and set phase to rules.MOVING
        pass

    def handle_event(self, event):
        self.roll_button.disabled = self.state.phase != rules.WAITING_FOR_ROLL
        self.roll_button.handle_event(event)

    def draw(self, surface):
        # ... existing board drawing from Quest 13 ...
        self.roll_button.draw(surface, self.app.font)
        # TODO: render self.state.dice and self.state.phase as text somewhere
        # visible, e.g. in the top-right corner
```

## Test it yourself
Run the game, get to `GameScreen`. Confirm the Roll Dice button is enabled, clicking it shows two numbers 1-6 and changes the displayed phase to `MOVING`, and clicking it again while in `MOVING` does nothing (since it's now disabled).

## Checkpoint
```text
git commit -m "Add phase system and working Roll Dice button"
```
The game now has a real turn structure — everything from here on is about filling in what happens during each phase.

## Stuck? Try this
- Button stays clickable in the wrong phase → confirm `self.roll_button.disabled` is being recalculated every frame in `handle_event`, not just once in `__init__`.
- Dice never change → check `self.roll()` is actually connected via `on_click=self.roll` and not `on_click=self.roll()` (calling it immediately instead of passing the function).
