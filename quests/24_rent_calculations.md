# Quest 24: Real rent — streets, railroads, utilities

## Why this quest
Quest 21 used a fake placeholder rent formula just to keep the loop moving. Now you'll replace it with the real Monopoly rent rules, including the monopoly-doubles-rent rule that's easy to get wrong.

## Your tasks

1. In `monopoly/rules.py`, write `owns_full_group(space, spaces, owner_id)`: returns `True` if every space sharing this space's `group` is owned by `owner_id`.
2. Write `calculate_street_rent(space, spaces)`: if `space.houses > 0`, return `space.rent[space.houses]` (remember index 0 is "no houses," so 1 house is index 1, and a hotel is index 5 when `houses == 5`). If `space.houses == 0` and the owner has the full color group, return `space.rent[0] * 2`. Otherwise return `space.rent[0]`.
3. Write `calculate_railroad_rent(space, spaces)`: count how many railroads the same owner holds, and return `25 * (2 ** (count - 1))` (this gives 25, 50, 100, 200 for 1, 2, 3, 4 railroads — verify this matches the real rent table in `PLAN.md` or a rules reference).
4. Write `calculate_utility_rent(space, spaces, dice_total)`: if the owner holds both utilities, return `dice_total * 10`; if just one, return `dice_total * 4`.
5. Write one entry point `calculate_rent(space, spaces, dice_total)` that dispatches to the right function based on `space.space_type`, and returns `0` if `space.mortgaged` is `True` (checked first, before anything else).
6. Replace the placeholder rent line in `resolve_space` (Quest 21) with a real call to `calculate_rent`.

## Starter code
```python
def owns_full_group(space, spaces, owner_id):
    group_spaces = [s for s in spaces if s.group == space.group]
    return all(s.owner == owner_id for s in group_spaces)


def calculate_street_rent(space, spaces):
    if space.houses > 0:
        return space.rent[space.houses]
    if owns_full_group(space, spaces, space.owner):
        # TODO: return double the base rent (space.rent[0])
        pass
    return space.rent[0]


def calculate_railroad_rent(space, spaces):
    owner = space.owner
    count = sum(1 for s in spaces if s.space_type == "RAILROAD" and s.owner == owner)
    # TODO: return 25 * (2 ** (count - 1))
    pass


def calculate_utility_rent(space, spaces, dice_total):
    owner = space.owner
    count = sum(1 for s in spaces if s.space_type == "UTILITY" and s.owner == owner)
    multiplier = 10 if count == 2 else 4
    return dice_total * multiplier


def calculate_rent(space, spaces, dice_total):
    if space.mortgaged:
        return 0
    if space.space_type == "STREET":
        return calculate_street_rent(space, spaces)
    if space.space_type == "RAILROAD":
        return calculate_railroad_rent(space, spaces)
    if space.space_type == "UTILITY":
        return calculate_utility_rent(space, spaces, dice_total)
    return 0
```

In `resolve_space`, replace the placeholder:
```python
rent = calculate_rent(space, state.spaces, sum(state.dice))
owning_player = next(p for p in state.players if p.player_id == space.owner)
pay(state, player, owning_player, rent, f"rent for {space.name}")
```

## Test it yourself
Add to `tests/test_rent.py`:
```python
from monopoly.models import Space
from monopoly.rules import calculate_rent

def make_group(owner):
    a = Space(1, "A", "STREET", group="brown", rent=[2, 10, 30, 90, 160, 250])
    b = Space(3, "B", "STREET", group="brown", rent=[4, 20, 60, 180, 320, 450])
    a.owner = owner
    b.owner = owner
    return [a, b]

def test_base_rent_without_monopoly():
    spaces = make_group(0)
    spaces[1].owner = 1  # break the monopoly
    assert calculate_rent(spaces[0], spaces, 0) == 2

def test_double_rent_with_full_monopoly_no_houses():
    spaces = make_group(0)
    assert calculate_rent(spaces[0], spaces, 0) == 4

def test_rent_with_houses_ignores_monopoly_doubling():
    spaces = make_group(0)
    spaces[0].houses = 2
    assert calculate_rent(spaces[0], spaces, 0) == 30

def test_mortgaged_property_charges_no_rent():
    spaces = make_group(0)
    spaces[0].mortgaged = True
    assert calculate_rent(spaces[0], spaces, 0) == 0
```
Run `python -m pytest tests/test_rent.py -v`. All four should pass. Then verify railroad and utility rent by hand-testing in the actual game (own 2 railroads, land on the 3rd as another player, confirm the correct rent is charged).

## Checkpoint
```text
git commit -m "Implement correct street, railroad, and utility rent"
```
Rent is the single most-used rule in the entire game — getting every case right here (monopoly doubling, mortgages, building levels) makes everything downstream trustworthy.

## Stuck? Try this
- Monopoly doubling applies even with houses built → check the `if space.houses > 0:` check comes *first* and returns immediately, before the monopoly check.
- Railroad rent numbers look wrong → recompute by hand: 1 railroad = 25, 2 = 50, 3 = 100, 4 = 200 — compare against what your formula prints for each count.
