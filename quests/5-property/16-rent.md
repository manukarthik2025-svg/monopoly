# Quest 16 · Rent

**Goal:** landing on someone else's property costs you rent, worked out by the real rules. The board shows who owns what.
**New files:** `logic/rent.py`, `tests/test_rent.py` **Changed:** `logic/game.py`, `ui/board_view.py`, `ui/sidebar.py`

## The rules

| Property | Rent |
|---|---|
| Street | `rent[0]`, **doubled** if the owner has the whole colour and it has no houses. With houses: `rent[houses]` (a hotel is `rent[5]`). |
| Railroad | $25 / $50 / $100 / $200 for owning 1 / 2 / 3 / 4 railroads |
| Utility | 4 × the dice roll, or 10 × if the owner has both |
| Mortgaged | nothing |

## Do it

1. Create `logic/rent.py`:

```python
from logic.board import group_of

RAILROAD_RENT = [0, 25, 50, 100, 200]    # index = how many railroads the owner has


def rent_for(space, board, dice_total):
    """How much you pay when you land on someone else's property."""
    if space.owner is None or space.mortgaged:
        return 0

    group = group_of(space, board)
    owned_by_same_person = [other for other in group if other.owner is space.owner]

    if space.kind == "RAILROAD":
        return RAILROAD_RENT[len(owned_by_same_person)]

    if space.kind == "UTILITY":
        pass    # TODO: 10 x dice_total if they own both utilities, otherwise 4 x

    # It's a street.
    if space.houses > 0:
        return space.rent[space.houses]
    # TODO: if they own the whole group, return double rent[0]
    return space.rent[0]
```

2. Create `tests/test_rent.py`. Write the tests **before** you fill in the TODOs, then make them pass:

```python
from helpers import make_game

from logic.rent import rent_for


def test_basic_street_rent():
    game = make_game()
    ann = game.players[0]
    game.board[1].owner = ann
    assert rent_for(game.board[1], game.board, 7) == 2


def test_whole_colour_set_doubles_rent():
    game = make_game()
    ann = game.players[0]
    game.board[1].owner = ann
    game.board[3].owner = ann
    assert rent_for(game.board[1], game.board, 7) == 4


def test_houses_change_the_rent():
    game = make_game()
    ann = game.players[0]
    game.board[1].owner = ann
    game.board[3].owner = ann
    game.board[1].houses = 3
    assert rent_for(game.board[1], game.board, 7) == 90


def test_hotel_rent():
    game = make_game()
    ann = game.players[0]
    game.board[39].owner = ann
    game.board[37].owner = ann
    game.board[39].houses = 5
    assert rent_for(game.board[39], game.board, 7) == 2000


def test_mortgaged_means_no_rent():
    game = make_game()
    game.board[1].owner = game.players[0]
    game.board[1].mortgaged = True
    assert rent_for(game.board[1], game.board, 7) == 0


def test_railroad_rent_goes_up_with_each_railroad():
    game = make_game()
    ann = game.players[0]
    expected = {5: 25, 15: 50, 25: 100, 35: 200}
    for index, rent in expected.items():
        game.board[index].owner = ann
        assert rent_for(game.board[5], game.board, 7) == rent


def test_utility_rent_uses_the_dice():
    game = make_game()
    ann = game.players[0]
    game.board[12].owner = ann
    assert rent_for(game.board[12], game.board, 7) == 28
    game.board[28].owner = ann
    assert rent_for(game.board[12], game.board, 7) == 70


def test_landing_on_someone_elses_street_pays_them():
    game = make_game((1, 2))
    ann, ben = game.players
    game.board[3].owner = ben
    game.roll()
    assert ann.cash == 1496
    assert ben.cash == 1504
```

3. In `logic/game.py`, import `from logic.rent import rent_for`. In `land()`, add to the `can_be_owned` part:

```python
            elif space.owner is not player:
                self.pay_rent(player, space)
```

   and add this method after `land`:

```python
    def pay_rent(self, player, space):
        if space.mortgaged:
            self.say(f"{space.name} is mortgaged, so there's no rent")
            return
        rent = rent_for(space, self.board, sum(self.dice))
        self.transfer(player, space.owner, rent, f"rent on {space.name}")
```

4. **Show owners on the board.** In `ui/board_view.py`, import `outer_strip` too. At the start of `draw`, straight after the `blit`:

```python
        for space in self.game.board:
            if space.owner is not None:
                pygame.draw.rect(surface, space.owner.color, outer_strip(space.index, 8))
```

5. **Show owners in the sidebar**, as a little coloured chip for every property someone owns. In `ui/sidebar.py`, import `from logic.board import properties_of`, then in `draw_players`, just before `badges = []`:

```python
            # Little coloured chips, one for each property they own.
            x = card.x + 60
            for space in properties_of(player, self.game.board):
                chip = pygame.Rect(x, card.y + 50, 11, 18)
                pygame.draw.rect(surface, theme.GROUP_COLORS[space.group], chip, border_radius=2)
                pygame.draw.rect(surface, theme.INK, chip, 1, border_radius=2)
                x += 13
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Buy something as one player, land on it as another → the rent shows in the log and both cash amounts change
- [ ] Owned spaces have a strip in the owner's colour along the outside edge

## Save

Commit message: `Quest 16: rent`
