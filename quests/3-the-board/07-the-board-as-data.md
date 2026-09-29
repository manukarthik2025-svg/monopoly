# Quest 07 · The board as data

**Goal:** all 40 spaces loaded from a data file, and checked by tests.
**New file:** `data/board.json` **Changed:** `logic/board.py`, `tests/test_board.py`

## Idea: facts go in data files

Prices and names are **facts**, not code. They go in a JSON file, which looks almost exactly like Python lists and dictionaries:

```json
{"name": "Baltic Avenue", "kind": "STREET", "price": 60}
```

The only differences: JSON uses `true`, `false` and `null` (Python's `True`, `False`, `None`), and it's very picky about commas. One missing comma and nothing loads.

Want a Monopoly with your town's streets on it? Change the JSON. No code changes needed.

## Do it

1. Create the folder `data/` and inside it `board.json`. Copy this in exactly:

```json
[
  {"name": "Go", "kind": "GO"},
  {"name": "Mediterranean Avenue", "kind": "STREET", "group": "brown", "price": 60, "house_cost": 50, "rent": [2, 10, 30, 90, 160, 250]},
  {"name": "Community Chest", "kind": "CARD"},
  {"name": "Baltic Avenue", "kind": "STREET", "group": "brown", "price": 60, "house_cost": 50, "rent": [4, 20, 60, 180, 320, 450]},
  {"name": "Income Tax", "kind": "TAX", "price": 200},
  {"name": "Reading Railroad", "kind": "RAILROAD", "group": "railroad", "price": 200},
  {"name": "Oriental Avenue", "kind": "STREET", "group": "light_blue", "price": 100, "house_cost": 50, "rent": [6, 30, 90, 270, 400, 550]},
  {"name": "Chance", "kind": "CARD"},
  {"name": "Vermont Avenue", "kind": "STREET", "group": "light_blue", "price": 100, "house_cost": 50, "rent": [6, 30, 90, 270, 400, 550]},
  {"name": "Connecticut Avenue", "kind": "STREET", "group": "light_blue", "price": 120, "house_cost": 50, "rent": [8, 40, 100, 300, 450, 600]},
  {"name": "Jail", "kind": "JAIL"},
  {"name": "St. Charles Place", "kind": "STREET", "group": "pink", "price": 140, "house_cost": 100, "rent": [10, 50, 150, 450, 625, 750]},
  {"name": "Electric Company", "kind": "UTILITY", "group": "utility", "price": 150},
  {"name": "States Avenue", "kind": "STREET", "group": "pink", "price": 140, "house_cost": 100, "rent": [10, 50, 150, 450, 625, 750]},
  {"name": "Virginia Avenue", "kind": "STREET", "group": "pink", "price": 160, "house_cost": 100, "rent": [12, 60, 180, 500, 700, 900]},
  {"name": "Pennsylvania Railroad", "kind": "RAILROAD", "group": "railroad", "price": 200},
  {"name": "St. James Place", "kind": "STREET", "group": "orange", "price": 180, "house_cost": 100, "rent": [14, 70, 200, 550, 750, 950]},
  {"name": "Community Chest", "kind": "CARD"},
  {"name": "Tennessee Avenue", "kind": "STREET", "group": "orange", "price": 180, "house_cost": 100, "rent": [14, 70, 200, 550, 750, 950]},
  {"name": "New York Avenue", "kind": "STREET", "group": "orange", "price": 200, "house_cost": 100, "rent": [16, 80, 220, 600, 800, 1000]},
  {"name": "Free Parking", "kind": "FREE_PARKING"},
  {"name": "Kentucky Avenue", "kind": "STREET", "group": "red", "price": 220, "house_cost": 150, "rent": [18, 90, 250, 700, 875, 1050]},
  {"name": "Chance", "kind": "CARD"},
  {"name": "Indiana Avenue", "kind": "STREET", "group": "red", "price": 220, "house_cost": 150, "rent": [18, 90, 250, 700, 875, 1050]},
  {"name": "Illinois Avenue", "kind": "STREET", "group": "red", "price": 240, "house_cost": 150, "rent": [20, 100, 300, 750, 925, 1100]},
  {"name": "B. & O. Railroad", "kind": "RAILROAD", "group": "railroad", "price": 200},
  {"name": "Atlantic Avenue", "kind": "STREET", "group": "yellow", "price": 260, "house_cost": 150, "rent": [22, 110, 330, 800, 975, 1150]},
  {"name": "Ventnor Avenue", "kind": "STREET", "group": "yellow", "price": 260, "house_cost": 150, "rent": [22, 110, 330, 800, 975, 1150]},
  {"name": "Water Works", "kind": "UTILITY", "group": "utility", "price": 150},
  {"name": "Marvin Gardens", "kind": "STREET", "group": "yellow", "price": 280, "house_cost": 150, "rent": [24, 120, 360, 850, 1025, 1200]},
  {"name": "Go To Jail", "kind": "GO_TO_JAIL"},
  {"name": "Pacific Avenue", "kind": "STREET", "group": "green", "price": 300, "house_cost": 200, "rent": [26, 130, 390, 900, 1100, 1275]},
  {"name": "North Carolina Avenue", "kind": "STREET", "group": "green", "price": 300, "house_cost": 200, "rent": [26, 130, 390, 900, 1100, 1275]},
  {"name": "Community Chest", "kind": "CARD"},
  {"name": "Pennsylvania Avenue", "kind": "STREET", "group": "green", "price": 320, "house_cost": 200, "rent": [28, 150, 450, 1000, 1200, 1400]},
  {"name": "Short Line", "kind": "RAILROAD", "group": "railroad", "price": 200},
  {"name": "Chance", "kind": "CARD"},
  {"name": "Park Place", "kind": "STREET", "group": "dark_blue", "price": 350, "house_cost": 200, "rent": [35, 175, 500, 1100, 1300, 1500]},
  {"name": "Luxury Tax", "kind": "TAX", "price": 100},
  {"name": "Boardwalk", "kind": "STREET", "group": "dark_blue", "price": 400, "house_cost": 200, "rent": [50, 200, 600, 1400, 1700, 2000]}
]
```

2. At the **top** of `logic/board.py`, add:

```python
import json
from pathlib import Path

# The data/ folder. Found from this file's location, so it works no matter
# which folder you run the game from.
DATA_FOLDER = Path(__file__).parent.parent / "data"
```

`Path(__file__)` is this file (`logic/board.py`). `.parent` is `logic/`, `.parent.parent` is the top folder, and `/ "data"` adds `data/` on the end.

3. At the **bottom** of `logic/board.py`, add:

```python
def load_board():
    """Read data/board.json and turn every entry into a Space."""
    with open(DATA_FOLDER / "board.json") as file:
        entries = json.load(file)

    board = []
    for index, entry in enumerate(entries):
        space = Space(
            index,
            entry["name"],
            entry["kind"],
            price=entry.get("price", 0),
            group=entry.get("group"),
            house_cost=entry.get("house_cost", 0),
            rent=entry.get("rent"),
        )
        # TODO: add space to the board list
    return board


def group_of(space, board):
    """Every space in the same group as `space`, including itself."""
    return [other for other in board if other.group is not None and other.group == space.group]


def owns_whole_group(player, space, board):
    return all(other.owner is player for other in group_of(space, board))


def properties_of(player, board):
    return [space for space in board if space.owner is player]
```

`entry.get("price", 0)` means: the price if this entry has one, otherwise 0. Go doesn't have a price.

4. Add these tests to `tests/test_board.py`, and change the import line to `from logic.board import Space, group_of, load_board`:

```python
def test_board_has_40_spaces():
    assert len(load_board()) == 40


def test_corners_are_in_the_right_place():
    board = load_board()
    assert board[0].kind == "GO"
    assert board[10].kind == "JAIL"
    assert board[20].kind == "FREE_PARKING"
    assert board[30].kind == "GO_TO_JAIL"


def test_every_street_has_six_rents():
    for space in load_board():
        if space.kind == "STREET":
            assert len(space.rent) == 6, space.name


def test_everything_you_can_buy_has_a_price():
    for space in load_board():
        if space.can_be_owned():
            assert space.price > 0, space.name


def test_group_sizes():
    board = load_board()
    assert len(group_of(board[1], board)) == 2      # brown
    # TODO: light blue has 3, dark blue has 2, railroads 4, utilities 2
```

## Check it

`python -m pytest`: **`7 passed`**.

Then delete one comma in `board.json` and run the tests again. That error is what a broken JSON file looks like. Put the comma back.

## Save

Commit message: `Quest 07: load the board from JSON`
