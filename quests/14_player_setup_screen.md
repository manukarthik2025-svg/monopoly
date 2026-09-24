# Quest 14: Player setup screen

## Why this quest
Right now there's no way to actually create the players who'll play. This quest builds the screen that turns "2 to 6 humans around a computer" into real `Player` objects, with basic mistake-proofing.

## Your tasks

1. In `monopoly/screens.py`, build out `SetupScreen` properly.
2. Let the user pick a player count from 2 to 6 (simplest approach: a `-` and `+` button next to a number).
3. For each active player slot, show a text field for their name. Pygame has no built-in text box, so track a plain string per player and append typed characters to it on `pygame.KEYDOWN` events (use `event.unicode`), handling `Backspace` (`pygame.K_BACKSPACE`) to remove the last character.
4. Let each player pick a token from a small fixed list (e.g. `["hat", "car", "dog", "ship", "boot", "iron"]`), no two players sharing one.
5. Add a "Start Game" button. Disable it (or refuse to proceed) if any name is blank, any two names match, or any two tokens match.
6. On successful start, build a list of `Player` objects and pass it into a new `GameState`, then switch to `GameScreen`.

## Starter code
```python
import pygame
from monopoly.models import Player, GameState, load_board

TOKENS = ["hat", "car", "dog", "ship", "boot", "iron"]

class SetupScreen:
    def __init__(self, app):
        self.app = app
        self.player_count = 2
        self.names = ["" for _ in range(6)]
        self.tokens = [TOKENS[i] for i in range(6)]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            active_slot = 0  # TODO: track which name field is currently being typed into
            if event.key == pygame.K_BACKSPACE:
                # TODO: remove the last character from self.names[active_slot]
                pass
            elif event.unicode.isprintable():
                # TODO: append event.unicode to self.names[active_slot]
                pass
        # TODO: handle clicks on +/- (change self.player_count, clamped 2-6),
        # clicks that select which name field is active, token pick buttons,
        # and the Start Game button

    def validation_error(self):
        active_names = self.names[:self.player_count]
        active_tokens = self.tokens[:self.player_count]
        if any(name.strip() == "" for name in active_names):
            return "Every player needs a name"
        # TODO: check for duplicate names using set(), same idea as Quest 11
        # TODO: check for duplicate tokens the same way
        return None

    def start_game(self):
        if self.validation_error():
            return
        players = []
        for i in range(self.player_count):
            # TODO: create a Player(i, self.names[i], self.tokens[i]) and append it
            pass
        from monopoly.screens import GameScreen
        state = GameState(players, load_board())
        self.app.go_to(GameScreen(self.app, state))

    def draw(self, surface):
        # TODO: draw the player count, each active name field (highlight the
        # active one), each token choice, any validation_error() message,
        # and the Start Game button
        pass
```

Note: `GameScreen` now needs to accept a `state` argument — update its `__init__(self, app, state)` and store `self.state = state` instead of building its own board.

## Test it yourself
Run the game. Try starting with only 1 player possible via count controls (should be blocked below 2, and above 6). Try leaving a name blank — you should see an error, not a crash. Try two identical names, then two identical tokens — both should be rejected with a clear message. Then fill in 3 valid distinct players and confirm Start Game reaches the board with those exact names.

## Checkpoint
```text
git commit -m "Add player setup screen with validation"
```
A real game finally starts from real human input instead of hardcoded test data.

## Stuck? Try this
- Typing does nothing → confirm you're checking `event.type == pygame.KEYDOWN` (not `MOUSEBUTTONDOWN`), and that `event.unicode` is being read, not `event.key`, for the actual character.
- Backspace deletes the wrong field → double check `active_slot` really points at the field you clicked, not always 0.
- `player_count` control breaks past 6 or below 2 → clamp it: `self.player_count = max(2, min(6, self.player_count))` after every change.
