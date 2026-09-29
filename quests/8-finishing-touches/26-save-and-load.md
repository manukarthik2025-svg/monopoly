# Quest 26 · Save and load

**Goal:** the game saves itself after every turn. **Continue** on the menu picks up where you left off. Esc opens a pause menu.
**New files:** `logic/save.py`, `tests/test_save.py` **Changed:** `logic/game.py`, `ui/popups.py`, `ui/play_screen.py`, `ui/sidebar.py`, `ui/screens.py`

## Idea: turning objects into plain data

JSON can store numbers, strings, lists and dictionaries, but **not** a `Player` object. So saving means turning the whole game into plain data (`game_to_dict`), and loading means building real objects back from it (`dict_to_game`).

The one tricky bit: a `Space` remembers its owner as a `Player` object. We save the player's **number** in the players list instead, and turn it back into the real `Player` when loading.

## Idea: `try` / `except`

A save file might be missing or broken. Instead of crashing the whole game:

```python
try:
    ...something that might fail...
except (OSError, ValueError):
    return None       # "couldn't load it" instead of a crash
```

## Do it

1. Create `logic/save.py`:

```python
import json
from pathlib import Path

from logic.cards import Deck
from logic.game import Game
from logic.player import Player

SAVE_FILE = Path(__file__).parent.parent / "saves" / "savegame.json"


def game_to_dict(game):
    """Turn a Game into plain lists and dictionaries that JSON can store."""

    def player_number(player):
        # JSON can't store a Player object, so we store their position in the list.
        if player is None:
            return None
        return game.players.index(player)

    return {
        "players": [
            {
                "name": player.name,
                "color": list(player.color),
                "cash": player.cash,
                "position": player.position,
                "in_jail": player.in_jail,
                "jail_turns": player.jail_turns,
                "jail_cards": player.jail_cards,
                "bankrupt": player.bankrupt,
            }
            for player in game.players
        ],
        "spaces": [
            {"owner": player_number(space.owner), "houses": space.houses, "mortgaged": space.mortgaged}
            for space in game.board
        ],
        "decks": {name: deck.cards for name, deck in game.decks.items()},
        "turn": game.turn,
        "phase": game.phase,
        "dice": list(game.dice),
        "doubles_in_a_row": game.doubles_in_a_row,
        "roll_again": game.roll_again,
        "houses_left": game.houses_left,
        "hotels_left": game.hotels_left,
        "log": game.log[-30:],
    }


def dict_to_game(data):
    """The opposite of game_to_dict: rebuild a real Game from saved data."""
    players = []
    for saved in data["players"]:
        player = Player(saved["name"], tuple(saved["color"]))
        player.cash = saved["cash"]
        player.position = saved["position"]
        player.in_jail = saved["in_jail"]
        player.jail_turns = saved["jail_turns"]
        player.jail_cards = saved["jail_cards"]
        player.bankrupt = saved["bankrupt"]
        players.append(player)

    game = Game(players)
    for space, saved in zip(game.board, data["spaces"]):
        pass    # TODO: set owner (careful: saved["owner"] is a number or None), houses, mortgaged

    for name, cards in data["decks"].items():
        game.decks[name] = Deck(name, cards, shuffle=False)

    game.turn = data["turn"]
    game.phase = data["phase"]
    game.dice = tuple(data["dice"])
    game.doubles_in_a_row = data["doubles_in_a_row"]
    game.roll_again = data["roll_again"]
    game.houses_left = data["houses_left"]
    game.hotels_left = data["hotels_left"]
    game.log = data["log"] + ["Game loaded. Welcome back!"]
    return game


def save_game(game):
    SAVE_FILE.parent.mkdir(exist_ok=True)
    with open(SAVE_FILE, "w") as file:
        json.dump(game_to_dict(game), file, indent=1)


def load_game():
    """Returns the saved Game, or None if there's no save (or it's broken)."""
    try:
        with open(SAVE_FILE) as file:
            return dict_to_game(json.load(file))
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        return None


def has_save():
    return SAVE_FILE.exists()


def delete_save():
    SAVE_FILE.unlink(missing_ok=True)
```

2. Create `tests/test_save.py`:

```python
from helpers import make_game

from logic.save import dict_to_game, game_to_dict


def test_saving_and_loading_keeps_everything():
    game = make_game((1, 2))
    ann, ben = game.players
    game.roll()
    game.buy()
    game.board[3].houses = 2

    copy = dict_to_game(game_to_dict(game))

    assert copy.players[0].name == "Ann"
    assert copy.players[0].cash == ann.cash
    assert copy.players[0].position == 3
    assert copy.board[3].owner is copy.players[0]
    assert copy.board[3].houses == 2
    assert copy.phase == game.phase
    assert copy.decks["Chance"].cards == game.decks["Chance"].cards
```

3. Saving in the middle of an auction or a debt gets complicated, so we only allow it at calm moments. Add to `Game` in `logic/game.py`:

```python
    def can_save(self):
        return self.phase in (ROLL, JAIL, END_TURN) and not self.debts
```

4. **Pause menu.** Add to `ui/popups.py`:

```python
class PausePopup:
    def __init__(self, screen):
        self.screen = screen
        self.box = pygame.Rect(0, 0, 420, 450)
        self.box.center = (theme.WIDTH // 2, theme.HEIGHT // 2)
        x = self.box.centerx - 140
        self.save_button = Button("Save game", self.save, (x, self.box.y + 170, 280, 56), theme.GREEN)
        self.buttons = [
            Button("Keep playing", screen.close_popup, (x, self.box.y + 100, 280, 56), theme.BLUE),
            self.save_button,
            Button("Rules", screen.open_rules, (x, self.box.y + 240, 280, 56), theme.PURPLE),
            Button("Quit to menu", screen.quit_to_menu, (x, self.box.y + 310, 280, 56), theme.RED),
        ]
        self.message = "Press F11 for full screen"

    def save(self):
        self.screen.save()
        self.message = "Saved!"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.screen.close_popup()
            return
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, surface):
        game = self.screen.game
        self.save_button.enabled = game.can_save()
        self.save_button.reason = "You can save at the start or end of a turn"
        panel(surface, self.box, theme.PAPER)
        text(surface, "Paused", (self.box.centerx, self.box.y + 30), 36, bold=True, anchor="midtop")
        for button in self.buttons:
            button.draw(surface)
        text(surface, self.message, (self.box.centerx, self.box.bottom - 40), 17, theme.GREY, anchor="center")
```

5. In `ui/play_screen.py`:
   - `from logic.save import delete_save, save_game` and add `PausePopup` to the popups import
   - `end_turn` autosaves:

```python
    def end_turn(self):
        self.game.end_turn()
        save_game(self.game)       # autosave after every turn
```

   - new methods:

```python
    def save(self):
        save_game(self.game)
        self.game.say("Game saved.")

    def open_pause(self):
        self.popup = PausePopup(self)

    def open_rules(self):
        from ui.screens import RulesScreen
        self.app.go_to(RulesScreen(self.app, back_to=self))
```

   - `Esc` opens the pause menu instead of quitting: in `handle_event`, `self.quit_to_menu()` becomes `self.open_pause()`
   - a finished game shouldn't be continued. Where `update` goes to the `WinnerScreen`, call `delete_save()` first.

6. In `ui/sidebar.py`, the Menu button opens the pause menu: `Button("Menu", screen.open_pause, ...)`

7. In `ui/screens.py`, import `from logic.save import has_save, load_game`. In `MenuScreen.__init__`, `self.continue_button.enabled = has_save()`, and:

```python
    def continue_game(self):
        game = load_game()
        if game is None:
            self.continue_button.enabled = False
            self.continue_button.reason = "That save file is broken, sorry!"
            return
        self.app.go_to(PlayScreen(self.app, game))
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Play a few turns, Esc → Quit to menu → Continue: the same game, same cash, same houses
- [ ] Open `saves/savegame.json` in VS Code and have a look. That's your whole game as text!

## Save

Commit message: `Quest 26: save and load`
