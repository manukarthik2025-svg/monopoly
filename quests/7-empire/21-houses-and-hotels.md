# Quest 21 · Houses and hotels

**Goal:** build houses and hotels (with all the real rules), sell them back, and see them on the board.
**Changed:** `logic/buildings.py`, `logic/game.py`, `ui/assets_popup.py`, `ui/board_view.py`, `tests/test_buildings.py`

## The rules

To build on a street you must:
1. own **every** street of that colour
2. have none of them mortgaged
3. build **evenly**: no street can get 2 houses ahead of another in its colour
4. and the bank must have one left. There are only **32 houses** and **12 hotels** in the whole game!

After 4 houses, the next one is a **hotel**. The 4 houses go back to the bank.
Selling gives you **half** the price back, and must also be even. Selling a hotel turns it back into 4 houses (if the bank has 4 to give).

## Do it

1. In `logic/game.py` `__init__`: the bank's supply.

```python
        self.houses_left = 32
        self.hotels_left = 12
```

2. At the top of `logic/buildings.py`, after the comment, add:

```python
def why_cant_build(game, space):
    group = group_of(space, game.board)
    if space.kind != "STREET":
        return "You can only build on streets"
    if not all(other.owner is space.owner for other in group):
        return "You need every street in this colour first"
    if any(other.mortgaged for other in group):
        return "A street in this colour is mortgaged"
    if space.houses == 5:
        return "It already has a hotel"
    # TODO: if this street already has more houses than the emptiest one in its colour:
    #       return "Build evenly: add to the other streets first"   (hint: min())
    if space.houses == 4 and game.hotels_left == 0:
        return "The bank has run out of hotels"
    if space.houses < 4 and game.houses_left == 0:
        return "The bank has run out of houses"
    if space.owner.cash < space.house_cost:
        return "Not enough cash"
    return None


def build(game, space):
    if why_cant_build(game, space):
        return
    game.transfer(space.owner, BANK, space.house_cost, f"building on {space.name}")
    if space.houses == 4:
        game.houses_left += 4         # the 4 houses go back when the hotel arrives
        game.hotels_left -= 1
    else:
        game.houses_left -= 1
    space.houses += 1


def why_cant_sell(game, space):
    if space.houses == 0:
        return "There's nothing built here"
    if space.houses < max(other.houses for other in group_of(space, game.board)):
        return "Sell evenly: sell from the other streets first"
    return None


def sell(game, space):
    if why_cant_sell(game, space):
        return
    refund = space.house_cost // 2
    if space.houses == 5:
        # A hotel turns back into 4 houses, if the bank has 4 to give.
        # If it doesn't, you're paid for the houses it's missing.
        game.hotels_left += 1
        houses_back = min(4, game.houses_left)
        game.houses_left -= houses_back
        refund += (4 - houses_back) * refund
        space.houses = houses_back
    else:
        game.houses_left += 1
        space.houses -= 1
    game.transfer(BANK, space.owner, refund, f"selling a building on {space.name}")
```

3. **Tests.** Add to `tests/test_buildings.py`, and import `build`, `sell`, `why_cant_build` and `why_cant_mortgage` too:

```python
def test_you_need_the_whole_colour():
    game, ann, med, baltic = browns_for_ann()
    baltic.owner = game.players[1]
    assert why_cant_build(game, med) is not None


def test_building_a_house():
    game, ann, med, baltic = browns_for_ann()
    build(game, med)
    assert med.houses == 1
    assert ann.cash == 1450
    assert game.houses_left == 31


def test_you_must_build_evenly():
    game, ann, med, baltic = browns_for_ann()
    build(game, med)
    assert why_cant_build(game, med) is not None
    build(game, baltic)
    assert why_cant_build(game, med) is None


def test_hotel_gives_back_four_houses():
    game, ann, med, baltic = browns_for_ann()
    for _ in range(4):
        build(game, med)
        build(game, baltic)
    assert game.houses_left == 24
    build(game, med)
    assert med.houses == 5
    assert game.houses_left == 28
    assert game.hotels_left == 11


def test_selling_gives_half_back():
    game, ann, med, baltic = browns_for_ann()
    build(game, med)
    sell(game, med)
    assert med.houses == 0
    assert ann.cash == 1475


def test_cant_mortgage_with_houses_in_the_colour():
    game, ann, med, baltic = browns_for_ann()
    build(game, med)
    assert why_cant_mortgage(game, baltic) is not None
```

4. **Build and Sell buttons.** In `ui/assets_popup.py`, add two more buttons to each `row`:

```python
                "build": Button("", partial(buildings.build, self.game, space), (x + 330, y, 112, 38), theme.GREEN, 15),
                "sell": Button("", partial(buildings.sell, self.game, space), (x + 450, y, 100, 38), theme.ORANGE, 15),
```

   Replace `row_buttons`:

```python
    def row_buttons(self, row):
        buttons = [row["build"], row["sell"]]
        if row["space"].mortgaged:
            buttons.append(row["unmortgage"])
        else:
            buttons.append(row["mortgage"])
        if row["space"].kind != "STREET":
            buttons = buttons[2:]        # you can't build on railroads and utilities
        return buttons
```

   In `update_buttons`, straight after `space = row["space"]`:

```python
            half = space.house_cost // 2
            row["build"].label = "Hotel " + money(space.house_cost) if space.houses == 4 else "House " + money(space.house_cost)
            row["build"].reason = buildings.why_cant_build(self.game, space)
            row["sell"].label = "Sell +" + money(half)
            row["sell"].reason = buildings.why_cant_sell(self.game, space)
```

   And make the grey line under the title show the bank's supply:

```python
        text(surface, f"Cash: {money(self.player.cash)}      Bank has {self.game.houses_left} houses "
                      f"and {self.game.hotels_left} hotels left",
             (BOX.x + 32, BOX.y + 68), 18, theme.GREY)
```

5. **Houses on the board.** In `ui/board_view.py`, import `inner_strip` too, and add at the top (under the imports):

```python
HOUSE_GREEN = (30, 150, 60)


def draw_house(surface, center, color=HOUSE_GREEN, width=12):
    x, y = center
    body = pygame.Rect(x - width // 2, y - 2, width, width * 2 // 3)
    roof = [(x - width // 2 - 2, y - 1), (x, y - width * 2 // 3), (x + width // 2 + 2, y - 1)]
    pygame.draw.rect(surface, color, body)
    pygame.draw.polygon(surface, color, roof)
    pygame.draw.rect(surface, theme.INK, body, 1)
    pygame.draw.polygon(surface, theme.INK, roof, 1)
```

   In the `draw` loop:

```python
            if space.houses > 0:
                self.draw_buildings(surface, space)
```

   and the method. Houses sit on the colour bar, which is along the side facing the middle:

```python
    def draw_buildings(self, surface, space):
        strip = inner_strip(space.index, 24)
        if space.houses == 5:
            pygame.draw.rect(surface, theme.RED, strip.inflate(-10, -8), border_radius=3)
            pygame.draw.rect(surface, theme.INK, strip.inflate(-10, -8), 1, border_radius=3)
            return
        for i in range(space.houses):
            if strip.width > strip.height:
                center = (strip.x + 9 + i * 17, strip.centery + 2)
            else:
                center = (strip.centerx, strip.y + 11 + i * 16)
            draw_house(surface, center)
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Get a whole colour. (Quick cheat for testing: in `SetupScreen.start`, give `players[0]` both browns for a moment. Remove it afterwards!)
- [ ] Build: green houses appear on the colour bar. Hover a grey Build button to see why you can't.
- [ ] 4 houses everywhere → a red hotel

## Save

Commit message: `Quest 21: houses and hotels`
