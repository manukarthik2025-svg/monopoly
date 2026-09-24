# Quest 31: Mortgage and unmortgage

## Why this quest
Mortgaging is how a cash-poor player raises money without selling a property outright. It comes with two restrictions that are easy to forget: no rent while mortgaged, and no mortgaging a property that has (or shares a group with) buildings.

## Your tasks

1. In `monopoly/rules.py`, write `can_mortgage(state, player, space)`: `None` if legal, else a reason. Illegal if `space.owner != player.player_id`, if `space.mortgaged` is already `True`, or if any property in the same color group has `houses > 0`.
2. Write `mortgage_property(state, player, space)`: `pay(state, "BANK", player, space.mortgage_value, ...)`, set `space.mortgaged = True`.
3. Write `can_unmortgage(state, player, space)`: `None` if legal, else a reason. Illegal if not mortgaged, or if the player can't afford the payoff amount.
4. Write `unmortgage_property(state, player, space)`: the payoff is the mortgage value plus 10% interest, rounded to the nearest whole number (use `round()`); pay the bank that amount, set `space.mortgaged = False`.
5. Wire both into `AssetManagerScreen`'s Mortgage/Unmortgage buttons, enabling/disabling via the `can_*` functions and showing the reason when disabled.
6. Double check `calculate_rent` (Quest 24) already returns `0` for a mortgaged property — you built that in, but confirm it with a quick manual test.

## Starter code
```python
def can_mortgage(state, player, space):
    if space.owner != player.player_id:
        return "You don't own this property"
    if space.mortgaged:
        return "Already mortgaged"
    group = houses_in_group(space, state.spaces)
    if any(s.houses > 0 for s in group):
        return "Sell the buildings in this group first"
    return None


def mortgage_property(state, player, space):
    pay(state, "BANK", player, space.mortgage_value, f"mortgaged {space.name}")
    space.mortgaged = True


def unmortgage_payoff(space):
    # TODO: return space.mortgage_value plus 10% interest, rounded to a whole number
    pass


def can_unmortgage(state, player, space):
    if not space.mortgaged:
        return "Not mortgaged"
    if player.cash < unmortgage_payoff(space):
        return "Not enough cash to pay off the mortgage"
    return None


def unmortgage_property(state, player, space):
    payoff = unmortgage_payoff(space)
    # TODO: pay(state, player, "BANK", payoff, ...), set space.mortgaged = False
    pass
```

## Test it yourself
Add to `tests/test_mortgages.py` (new file):
```python
from monopoly.models import Player, GameState, Space
from monopoly.rules import can_mortgage, mortgage_property, unmortgage_payoff, unmortgage_property

def test_mortgage_pays_mortgage_value():
    space = Space(1, "A", "STREET", group="brown", mortgage_value=30)
    space.owner = 0
    player = Player(0, "Alice", "hat")
    state = GameState([player], [space])
    mortgage_property(state, player, space)
    assert space.mortgaged is True
    assert player.cash == 1530

def test_cannot_mortgage_with_buildings_in_group():
    a = Space(1, "A", "STREET", group="brown", mortgage_value=30)
    b = Space(3, "B", "STREET", group="brown", mortgage_value=30)
    a.owner = 0
    b.owner = 0
    b.houses = 1
    player = Player(0, "Alice", "hat")
    state = GameState([player], [a, b])
    assert can_mortgage(state, player, a) is not None

def test_unmortgage_costs_ten_percent_interest():
    space = Space(1, "A", "STREET", group="brown", mortgage_value=30)
    space.owner = 0
    space.mortgaged = True
    assert unmortgage_payoff(space) == 33
```
Run `python -m pytest tests/test_mortgages.py -v`.

## Checkpoint
```text
git commit -m "Add mortgage and unmortgage with interest"
```
Players now have a legal way to raise cash under pressure — this is what Quest 33 (raising funds before bankruptcy) will lean on.

## Stuck? Try this
- Interest calculation is off by a dollar → `round()` in Python rounds `.5` to the nearest *even* number by default (e.g. `round(2.5) == 2`); if your board data ever produces a `.5` case, decide on a rule (e.g. always round up) and apply it consistently, then document the choice in a comment.
- Mortgaging doesn't block rent → re-check `calculate_rent`'s very first line handles `space.mortgaged` before checking anything else.
