# Quest 11: Load and check the board data

## Why this quest
A typo in `board.json` (a duplicate index, a missing rent value) should be caught immediately with a clear error — not discovered three weeks from now when rent comes out wrong during a real game. You'll write a loader function and your first real automated tests.

## New idea(s)
**pytest.** A test is a small function that checks one specific thing is true, using the `assert` keyword. `assert` does nothing if its condition is true, and crashes with a helpful message if it's false. pytest finds every function starting with `test_` in files starting with `test_`, runs them all, and reports which passed or failed.

```python
def add(a, b):
    return a + b

def test_add_two_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_number():
    assert add(5, -2) == 3
```
Running `python -m pytest` finds and runs both `test_` functions automatically — no need to call them yourself.

## Your tasks

1. In `monopoly/models.py`, write `load_board(path="data/board.json")` that reads the JSON file and returns a list of 40 `Space` objects (not raw dictionaries — build real `Space` objects from each entry's fields).
2. Create `tests/test_board.py`.
3. Write `test_board_has_forty_spaces()`.
4. Write `test_no_duplicate_indexes()` — build a list of every `index` and check its length equals the length of the `set()` of that list (a `set` automatically drops duplicates, so if the lengths differ, something repeats).
5. Write `test_purchasable_spaces_have_positive_price()` — every space where `is_property()` is `True` should have `price > 0`.
6. Write `test_streets_have_six_rent_values()`.

## Starter code

Add to `monopoly/models.py`:
```python
import json

def load_board(path="data/board.json"):
    with open(path) as f:
        raw_spaces = json.load(f)
    spaces = []
    for entry in raw_spaces:
        space = Space(
            index=entry["index"],
            name=entry["name"],
            space_type=entry["space_type"],
            price=entry.get("price", 0),
            mortgage_value=entry.get("mortgage_value", 0),
            group=entry.get("group"),
            house_cost=entry.get("house_cost", 0),
            rent=entry.get("rent"),
        )
        # TODO: append space to the spaces list
    return spaces
```

`tests/test_board.py`:
```python
from monopoly.models import load_board

def test_board_has_forty_spaces():
    spaces = load_board()
    assert len(spaces) == 40

def test_no_duplicate_indexes():
    spaces = load_board()
    indexes = [space.index for space in spaces]
    # TODO: assert len(indexes) == len(set(indexes))

def test_purchasable_spaces_have_positive_price():
    spaces = load_board()
    for space in spaces:
        if space.is_property():
            # TODO: assert space.price > 0, with a helpful message naming the space
            pass

def test_streets_have_six_rent_values():
    spaces = load_board()
    for space in spaces:
        if space.space_type == "STREET":
            # TODO: assert len(space.rent) == 6
            pass
```

## Test it yourself
Run:
```powershell
python -m pytest tests/test_board.py -v
```
All four tests should show `PASSED`. If any fail, pytest prints exactly which assertion failed and what the actual value was — read that message before changing anything.

## Checkpoint
```text
git commit -m "Load and validate 40 board spaces"
```
You now have an automatic safety net: any future typo in your board data gets caught in seconds instead of during a real game.

## Stuck? Try this
- `KeyError: 'price'` while loading → some non-property space's JSON entry might have used the wrong key name; check `entry.get("price", 0)` is being used, not `entry["price"]`, for optional fields.
- A test fails naming a specific space → that's the loader working correctly — go fix the data in `board.json`, not the test.
- `test_streets_have_six_rent_values` fails on a space that isn't really a street → double-check that space's `space_type` in the JSON file.
