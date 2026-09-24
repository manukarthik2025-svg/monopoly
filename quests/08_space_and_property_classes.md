# Quest 08: A Space class for the whole board

## Why this quest
Every one of the 40 board spaces — Go, streets, railroads, tax spaces, Jail — needs to be represented as an object. Streets and railroads need extra information (price, rent) that Go and Jail don't. Rather than building a separate class for every space type, you'll build one flexible `Space` class that only uses the fields that make sense for its type.

## New idea(s)
**Optional fields with default values.** A function or method parameter can have a default, so callers only need to supply the values that matter for them:

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Sam")                  # Hello, Sam!
greet("Sam", "Good morning")  # Good morning, Sam!
```
You'll use this so that `Space(0, "Go", "GO")` works fine without a price, while `Space(1, "Mediterranean Avenue", "STREET", price=60, ...)` fills in the extra property details.

## Your tasks

1. In `monopoly/models.py`, add a `Space` class below `Player`.
2. Store: `index`, `name`, `space_type` (one of `"GO"`, `"STREET"`, `"RAILROAD"`, `"UTILITY"`, `"TAX"`, `"CHANCE"`, `"COMMUNITY_CHEST"`, `"JAIL"`, `"GO_TO_JAIL"`, `"FREE_PARKING"`), and these optional fields defaulting sensibly: `price=0`, `mortgage_value=0`, `group=None`, `house_cost=0`, `rent=None`.
3. In `__init__`, if `rent` is `None`, set `self.rent = []` (an empty list) instead — this avoids a classic Python trap where every object would otherwise share the *same* list.
4. Add mutable game-state fields that start the same for every space regardless of type: `self.owner = None`, `self.mortgaged = False`, `self.houses = 0`.
5. Add a method `is_property(self)` that returns `True` if `space_type` is `"STREET"`, `"RAILROAD"`, or `"UTILITY"`.
6. Test it temporarily by creating one `Space` for Go and one `Space` for a street with a price, printing both, then delete the test code.

## Starter code
```python
class Space:
    def __init__(self, index, name, space_type, price=0, mortgage_value=0,
                 group=None, house_cost=0, rent=None):
        self.index = index
        self.name = name
        self.space_type = space_type
        self.price = price
        self.mortgage_value = mortgage_value
        self.group = group
        self.house_cost = house_cost
        self.rent = rent if rent is not None else []
        # Fields below change during play, not from the board data:
        self.owner = None       # a player_id, or None if unowned
        self.mortgaged = False
        self.houses = 0         # 0-4 houses, 5 means a hotel

    def is_property(self):
        # TODO: return True for "STREET", "RAILROAD", or "UTILITY"
        pass
```

## Test it yourself
Temporarily add and run:
```python
go = Space(0, "Go", "GO")
med = Space(1, "Mediterranean Avenue", "STREET", price=60,
            mortgage_value=30, group="brown", house_cost=50,
            rent=[2, 10, 30, 90, 160, 250])
print(go.is_property(), med.is_property())   # False True
```
Then remove this test code — the real board will come from a data file in the next quest.

## Checkpoint
```text
git commit -m "Add Space class for board spaces and properties"
```
Every one of the 40 spaces on the board — buyable or not — will be one of these objects.

## Stuck? Try this
- All your `Space` objects seem to share the same `rent` list, and changing one changes them all → this is the classic "mutable default argument" bug; make sure you used `rent=None` as the default and built a fresh `[]` inside `__init__`, not `rent=[]` in the parameter list.
- `is_property()` always returns `False` → double check you're comparing `self.space_type` against the exact strings, including capitalization.
