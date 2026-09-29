# Quest 06 · Players and spaces

**Goal:** the first two pieces of the rules, `Player` and `Space`, plus your first automatic tests.
**New files:** `logic/player.py`, `logic/board.py`, `pytest.ini`, `tests/test_board.py`

## Idea: rules go in `logic/`, and get tested

Nothing in `logic/` imports pygame. A `Player` doesn't know it's drawn as a circle, it just knows its cash and position. Because of that, a **test** can check the rules in a split second without opening a window.

A test is a function whose name starts with `test_`. Inside it, `assert` something that must be true:

```python
def test_maths_still_works():
    assert 2 + 2 == 4
```

`python -m pytest` finds every `test_...` function in the `tests/` folder and runs it. Green means everything passed.

## Do it

1. Create `logic/player.py`:

```python
class Player:
    """One person playing the game."""

    def __init__(self, name, color=(200, 200, 200)):
        self.name = name
        self.color = color          # (red, green, blue) for their token
        self.cash = 1500
        self.position = 0           # which space they're on: 0 is Go, 39 is Boardwalk
        self.in_jail = False
        self.jail_turns = 0         # how many times they've failed to roll doubles in jail
        self.jail_cards = []        # "Get Out of Jail Free" cards they're holding
        self.bankrupt = False

    def __repr__(self):
        return f"Player({self.name}, ${self.cash})"
```

`__repr__` is what Python shows when you `print` a player. Without it you'd see something like `<Player object at 0x03A...>`.

2. Create `logic/board.py`:

```python
class Space:
    """One of the 40 squares on the board."""

    def __init__(self, index, name, kind, price=0, group=None, house_cost=0, rent=None):
        # Facts from board.json. These never change during a game.
        self.index = index
        self.name = name
        self.kind = kind              # "STREET", "RAILROAD", "UTILITY", "TAX", "CARD", ...
        self.price = price
        self.group = group            # "brown", "red", ... or "railroad" / "utility"
        self.house_cost = house_cost
        self.rent = rent or []        # streets: [no houses, 1, 2, 3, 4 houses, hotel]

        # Things that change while you play.
        self.owner = None             # a Player, or None while the bank owns it
        self.houses = 0               # 0-4 houses. 5 means a hotel.
        self.mortgaged = False

    def can_be_owned(self):
        pass    # TODO: True if self.kind is "STREET", "RAILROAD" or "UTILITY"

    def mortgage_value(self):
        pass    # TODO: half the price, as a whole number (use //)

    def __repr__(self):
        return f"Space({self.index}, {self.name})"
```

3. Create `pytest.ini` in the top folder. It tells pytest where the tests are, and that the top folder is where imports start from:

```ini
[pytest]
pythonpath = .
testpaths = tests
```

4. Create the folder `tests/` and inside it `test_board.py`:

```python
from logic.board import Space


def test_streets_can_be_owned_but_go_cant():
    street = Space(1, "Baltic Avenue", "STREET", price=60)
    go = Space(0, "Go", "GO")
    assert street.can_be_owned()
    assert not go.can_be_owned()


def test_mortgage_value_is_half_the_price():
    pass    # TODO: make a Space with price 60, assert its mortgage_value() is 30
```

## Check it

Run `python -m pytest`. You want: **`2 passed`**.

Now break it on purpose: change `// 2` to `// 3` and run the tests again. Read how pytest tells you what went wrong, then put it back.

## Save

Commit message: `Quest 06: Player, Space and first tests`
