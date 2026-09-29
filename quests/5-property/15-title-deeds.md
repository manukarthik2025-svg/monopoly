# Quest 15 · Title deeds

**Goal:** a real-looking title deed card when you can buy something, or when you hover over any property. Greyed-out buttons explain *why* when you hover over them.
**New file:** `ui/card_art.py` **Changed:** `ui/stage.py`, `ui/board_view.py`, `ui/widgets.py`, `ui/app.py`, `ui/play_screen.py`, `ui/screens.py`

## Idea: "why not?" instead of just "no"

A grey button with no explanation is annoying. So every `Button` gets a `reason`: a short sentence shown in a little tooltip when you hover over it while it's disabled. Later, the rules themselves will give the reasons ("Build evenly: add to the other streets first").

## Do it

1. Create `ui/card_art.py`:

```python
"""Title deeds and Chance / Community Chest cards."""
import pygame

from ui import theme
from ui.board_art import draw_icon
from ui.draw import money, panel, text, text_block, text_color_for

DEED_SIZE = (260, 312)


def deed_rows(space):
    """The (label, value) lines printed on a title deed."""
    if space.kind == "STREET":
        rent = space.rent
        return [
            ("Rent", money(rent[0])),
            ("With colour set", money(rent[0] * 2)),
            ("With 1 house", money(rent[1])),
            ("With 2 houses", money(rent[2])),
            ("With 3 houses", money(rent[3])),
            ("With 4 houses", money(rent[4])),
            ("With a hotel", money(rent[5])),
            None,                                   # a dividing line
            ("Houses cost", f"{money(space.house_cost)} each"),
            ("Mortgage value", money(space.mortgage_value())),
        ]
    if space.kind == "RAILROAD":
        return [
            ("Rent", "$25"),
            ("If 2 railroads owned", "$50"),
            ("If 3 railroads owned", "$100"),
            ("If 4 railroads owned", "$200"),
            None,
            ("Mortgage value", money(space.mortgage_value())),
        ]
    return [
        ("Own 1 utility:", "4 x dice"),
        ("Own both:", "10 x dice"),
        None,
        ("Mortgage value", money(space.mortgage_value())),
    ]


def draw_deed(surface, space, center):
    card = pygame.Rect((0, 0), DEED_SIZE)
    card.center = center
    panel(surface, card, theme.WHITE, radius=10)
    inside = card.inflate(-20, -20)

    header = pygame.Rect(inside.x, inside.y, inside.width, 76)
    if space.kind == "STREET":
        color = theme.GROUP_COLORS[space.group]
        pygame.draw.rect(surface, color, header)
        ink = text_color_for(color)
        text(surface, "TITLE DEED", (header.centerx, header.y + 6), 12, ink, anchor="midtop")
        text_block(surface, space.name.upper(), header.centerx, header.y + 24, header.width - 10, 19, ink, bold=True)
    else:
        draw_icon(surface, space, (header.centerx, header.y + 26))
        text_block(surface, space.name.upper(), header.centerx, header.y + 50, header.width - 10, 17, bold=True)
    pygame.draw.rect(surface, theme.INK, header, 2)

    y = header.bottom + 12
    for row in deed_rows(space):
        if row is None:
            pygame.draw.line(surface, theme.LIGHT_GREY, (inside.x, y + 4), (inside.right, y + 4), 2)
            y += 12
            continue
        label, value = row
        text(surface, label, (inside.x + 4, y), 16)
        text(surface, value, (inside.right - 4, y), 16, bold=True, anchor="topright")
        y += 21

    if space.mortgaged:
        stamp = theme.title_font(30).render("MORTGAGED", True, theme.RED)
        stamp = pygame.transform.rotate(stamp, 25)
        surface.blit(stamp, stamp.get_rect(center=card.center))
    return card
```

2. In `ui/stage.py`, import `from ui.card_art import draw_deed`, then change `draw`. It now also shows the deed of whatever property the mouse is over:

```python
    def draw(self, surface, hovered_space):
        game = self.game
        if game.phase == BUY:
            self.cover(surface)
            space = game.board[game.current_player().position]
            draw_deed(surface, space, (CENTER.centerx, CENTER.y + 250))
            text(surface, "FOR SALE", (CENTER.centerx, CENTER.y + 50), 22, theme.GREY, bold=True, anchor="midtop")
        elif hovered_space is not None and hovered_space.can_be_owned():
            self.cover(surface)
            draw_deed(surface, hovered_space, (CENTER.centerx, CENTER.centery - 20))
            owner = hovered_space.owner
            words = f"Owned by {owner.name}" if owner else f"For sale: {money(hovered_space.price)}"
            text(surface, words, (CENTER.centerx, CENTER.centery + 160), 22, theme.INK, bold=True, anchor="midtop")

        for button in self.buttons():
            button.draw(surface)
```

   And in `update`, give the Buy button a reason:

```python
            self.buy_button.reason = "Not enough cash. Mortgage something, or auction it."
```

3. In `ui/board_view.py`, add a method that finds the space under the mouse:

```python
    def space_under_mouse(self):
        mouse = pygame.mouse.get_pos()
        for space in self.game.board:
            if space_rect(space.index).collidepoint(mouse):
                return space
        return None
```

   and in `draw`, just before `self.draw_tokens(...)`, outline it in gold:

```python
        hovered = self.space_under_mouse()
        if hovered is not None:
            pygame.draw.rect(surface, theme.GOLD, space_rect(hovered.index), 3)
```

4. In `PlayScreen.draw` (`ui/play_screen.py`), pass the hovered space to the stage:

```python
        hovered = self.board_view.space_under_mouse()
        self.stage.draw(surface, hovered)
```

5. **Tooltips.** In `ui/widgets.py`:
   - under the imports, add:

```python
# A tooltip is drawn last, on top of everything. Buttons fill this in when hovered.
tooltip = None
```

   - in `Button.__init__`: `self.reason = None            # why it's disabled, shown when you hover`
   - replace the start of `Button.draw` (everything up to `elif hovered:`) with:

```python
    def draw(self, surface):
        global tooltip
        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)

        if not self.enabled:
            color = theme.DISABLED
            if hovered and self.reason:
                tooltip = (self.reason, mouse)
```

   - add this function at the bottom:

```python
def draw_tooltip(surface):
    global tooltip
    if tooltip is None:
        return
    words, (x, y) = tooltip
    image = theme.font(16).render(words, True, theme.WHITE)
    box = image.get_rect(bottomleft=(x + 14, y - 10)).inflate(18, 12)
    box.clamp_ip(surface.get_rect())
    pygame.draw.rect(surface, (35, 35, 40), box, border_radius=8)
    surface.blit(image, image.get_rect(center=box.center))
    tooltip = None
```

6. In `ui/app.py`: `from ui import theme, widgets`, and draw the tooltip **after** the screen, so it's on top:

```python
            self.screen.draw(self.window)
            widgets.draw_tooltip(self.window)
```

7. Reasons for the buttons you already have. In `ui/screens.py`:
   - `MenuScreen.__init__`: `self.continue_button.reason = "There's no saved game yet"`
   - `SetupScreen.update`: `self.start_button.reason = self.problem()`

   And in `ui/sidebar.py` `update`: `self.bail_button.reason = "Not enough cash"`

## Check it

- [ ] Hover over any property → its deed appears in the middle, and the space gets a gold outline
- [ ] Land on one → the deed shows with Buy / Auction it
- [ ] Hover over a grey button → a tooltip says why

## Save

Commit message: `Quest 15: title deeds and tooltips`
