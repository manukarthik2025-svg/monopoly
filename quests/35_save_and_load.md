# Quest 35: Save and load a game

## Why this quest
A real game can take an hour. Nobody wants to lose all progress by closing the window. This quest teaches you to turn your whole `GameState` into plain data and back — the same JSON skill from Quest 10, applied to something that changes constantly instead of something fixed.

## Your tasks

1. Create `monopoly/persistence.py`.
2. Write `state_to_dict(state)`: convert every important piece of `GameState` (players, spaces including their mutable owner/mortgaged/houses fields, current_player_index, phase, dice, doubles_count, houses_left, hotels_left, history, deck orders and discard piles, held jail cards, pending_decision if any) into plain dictionaries and lists — no `Player`/`Space` objects, no Pygame objects, ever.
3. Write `dict_to_state(data)`: the reverse — rebuild real `Player`, `Space`, and `GameState` objects from the dictionary.
4. Include a `"save_version": 1` field. Before loading, check it matches what your code expects; if not (or if the file is corrupt/missing keys), show a friendly in-game message instead of crashing.
5. Write `save_game(state, path)` using an atomic pattern: write to a temporary file first (e.g. `path + ".tmp"`), then rename it over the real path only once the write succeeded — this way a crash mid-save can never corrupt your only copy.
6. Write `load_game(path)` that calls `dict_to_state` and returns `None` (with a logged error) rather than crashing on a bad file.
7. Wire a "Save" button (writes to `saves/quicksave.json`) and a "Load Game" menu option into the UI. Add an autosave call at the end of `advance_turn` (Quest 19).

## Starter code
```python
import json
import os
from monopoly.models import Player, Space, GameState

SAVE_VERSION = 1

def state_to_dict(state):
    return {
        "save_version": SAVE_VERSION,
        "players": [player_to_dict(p) for p in state.players],
        "spaces": [space_to_dict(s) for s in state.spaces],
        "current_player_index": state.current_player_index,
        "phase": state.phase,
        "dice": list(state.dice),
        "doubles_count": state.doubles_count,
        "houses_left": state.houses_left,
        "hotels_left": state.hotels_left,
        "history": state.history,
        # TODO: also include chance/chest deck and discard contents,
        # and held_jail_cards, once those exist in your GameState
    }


def player_to_dict(player):
    # TODO: return a plain dict with every field from Player.__init__,
    # plus owned, in_jail, jail_turns, jail_cards, bankrupt
    pass


def space_to_dict(space):
    # TODO: return a plain dict with every field from Space.__init__,
    # including the mutable owner/mortgaged/houses values
    pass


def save_game(state, path):
    data = state_to_dict(state)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)  # atomic on both Windows and other platforms


def load_game(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    if data.get("save_version") != SAVE_VERSION:
        return None
    return dict_to_state(data)


def dict_to_state(data):
    players = [dict_to_player(pd) for pd in data["players"]]
    spaces = [dict_to_space(sd) for sd in data["spaces"]]
    state = GameState(players, spaces)
    state.current_player_index = data["current_player_index"]
    state.phase = data["phase"]
    state.dice = tuple(data["dice"])
    state.doubles_count = data["doubles_count"]
    state.houses_left = data["houses_left"]
    state.hotels_left = data["hotels_left"]
    state.history = data["history"]
    return state


def dict_to_player(d):
    # TODO: build a Player from d, then overwrite every field (cash,
    # position, owned, in_jail, jail_turns, jail_cards, bankrupt) with the
    # saved values instead of the fresh __init__ defaults
    pass


def dict_to_space(d):
    # TODO: same idea as dict_to_player, but for Space
    pass
```

## Test it yourself
Add to `tests/test_persistence.py` (new file):
```python
from monopoly.models import Player, Space, GameState
from monopoly.persistence import save_game, load_game

def test_round_trip_preserves_key_values(tmp_path):
    player = Player(0, "Alice", "hat")
    player.cash = 1234
    space = Space(1, "A", "STREET", group="brown")
    space.owner = 0
    state = GameState([player], [space])
    state.phase = "TURN_END"

    save_path = str(tmp_path / "test_save.json")
    save_game(state, save_path)
    loaded = load_game(save_path)

    assert loaded is not None
    assert loaded.players[0].cash == 1234
    assert loaded.spaces[0].owner == 0
    assert loaded.phase == "TURN_END"

def test_loading_a_missing_file_returns_none():
    assert load_game("saves/does_not_exist.json") is None
```
`tmp_path` is a built-in pytest tool that hands you a fresh temporary folder per test — no manual cleanup needed. Run `python -m pytest tests/test_persistence.py -v`.

## Checkpoint
```text
git commit -m "Add save/load with atomic writes and validation"
```
You can now close the game mid-match and pick up exactly where you left off — including mid-auction or mid-payment, once you extend `state_to_dict`/`dict_to_state` to cover `pending_decision` too.

## Stuck? Try this
- Loaded game is missing owned properties or wrong houses → confirm `space_to_dict`/`dict_to_space` include the mutable fields (`owner`, `mortgaged`, `houses`), not just the static ones from the original JSON board data.
- Crash on load after a bad edit to a save file → that's exactly what the `save_version` check and the `try/except` around `json.load` are for; confirm they're really catching it instead of letting the exception propagate.
