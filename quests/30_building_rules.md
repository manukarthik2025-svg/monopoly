# Quest 30: Houses, hotels, and even building

## Why this quest
Building is one of the rule-heaviest parts of Monopoly: full group ownership, no mortgages in the group, even building across properties, and a limited bank supply. Get this right and the "real" version of Monopoly starts to feel real.

## Your tasks

1. In `monopoly/rules.py`, write `can_build(state, player, space)` returning `None` if building is legal, or a short reason string if not. Checks, in order: player owns the full color group (`owns_full_group`); no property in the group is mortgaged; the bank has houses left (or a hotel available, if this build would create one); building here wouldn't put this property more than 1 house ahead of the least-built property in its group (the "even building" rule).
2. Write `build_house(state, player, space)`: pay `space.house_cost` to the bank, increment `space.houses`, decrement `state.houses_left` by 1 (or, if this build takes `houses` from 4 to 5 — a hotel — return 4 houses to the bank supply and decrement `hotels_left` by 1 instead).
3. Write `can_sell_building(state, player, space)` and `sell_building(state, player, space)` with matching logic in reverse: selling must also stay even across the group, refunds half the house cost, and returns houses/hotel to the bank supply correctly.
4. Wire these into `AssetManagerScreen`'s Build/Sell buttons from Quest 29, enabling/disabling based on `can_build`/`can_sell_building`, and showing the reason string when disabled.
5. If multiple players want the last available houses/hotels at the same time, PLAN.md calls for an auction of the scarce buildings — this is a stretch goal; a simpler acceptable v1 is strictly first-come-first-served (whoever clicks Build first when supply is limited gets it, and `can_build` blocks everyone else once supply hits zero).

## Starter code
```python
def houses_in_group(space, spaces):
    return [s for s in spaces if s.group == space.group]


def can_build(state, player, space):
    if not owns_full_group(space, spaces=state.spaces, owner_id=player.player_id):
        return "You need the full color group"
    group = houses_in_group(space, state.spaces)
    if any(s.mortgaged for s in group):
        return "A property in this group is mortgaged"
    would_be_hotel = space.houses == 4
    if would_be_hotel and state.hotels_left == 0:
        return "No hotels left in the bank"
    if not would_be_hotel and state.houses_left == 0:
        return "No houses left in the bank"
    lowest = min(s.houses for s in group)
    if space.houses > lowest:
        # TODO: return a reason like "Build evenly across the group first"
        pass
    return None


def build_house(state, player, space):
    pay(state, player, "BANK", space.house_cost, f"built on {space.name}")
    if space.houses == 4:
        state.houses_left += 4
        state.hotels_left -= 1
        space.houses = 5
    else:
        # TODO: increment space.houses by 1, decrement state.houses_left by 1
        pass
```

## Test it yourself
Add to `tests/test_building.py` (new file):
```python
from monopoly.models import Player, GameState, Space
from monopoly.rules import can_build, build_house

def make_monopoly_state():
    a = Space(1, "A", "STREET", group="brown", house_cost=50, rent=[2,10,30,90,160,250])
    b = Space(3, "B", "STREET", group="brown", house_cost=50, rent=[4,20,60,180,320,450])
    a.owner = 0
    b.owner = 0
    player = Player(0, "Alice", "hat")
    player.owned = [1, 3]
    state = GameState([player], [a, b])
    return state, player, a, b

def test_cannot_build_without_full_group():
    state, player, a, b = make_monopoly_state()
    b.owner = 1
    assert can_build(state, player, a) is not None

def test_cannot_build_unevenly():
    state, player, a, b = make_monopoly_state()
    a.houses = 2
    assert can_build(state, player, a) is not None  # a is already ahead of b

def test_build_reduces_bank_supply():
    state, player, a, b = make_monopoly_state()
    build_house(state, player, a)
    assert a.houses == 1
    assert state.houses_left == 31

def test_hotel_returns_four_houses_to_bank():
    state, player, a, b = make_monopoly_state()
    a.houses = 4
    b.houses = 4
    build_house(state, player, a)
    assert a.houses == 5
    assert state.hotels_left == 11
```
Run `python -m pytest tests/test_building.py -v`. Total houses (32) and hotels (12) should always be conserved — add a test that sums `houses_left` plus every space's house count and confirms it never exceeds 32 across a sequence of builds.

## Checkpoint
```text
git commit -m "Add building rules: even building, bank supply, hotels"
```
This is one of the fiddliest rule sets in the game — passing these tests means you've genuinely nailed it.

## Stuck? Try this
- "Even building" check feels backwards → picture two properties at 2 and 0 houses; you should be able to build on the one with 0 (bringing it to 1, still behind), but not on the one with 2 (which would make the gap even wider).
- Hotel supply goes negative → make sure selling a hotel (Quest 30 or 31, whichever you do it in) checks the bank actually has 4 houses available to hand back before allowing the sale.
