# Quest 04 · A button class

**Goal:** four menu buttons that light up and lift when you hover, and do something when clicked.
**New file:** `ui/widgets.py` **Changed:** `ui/draw.py`, `ui/app.py`

## Idea: a function is a value

```python
def hello():
    print("hi")

greet = hello      # no brackets: greet IS the function now
greet()            # prints "hi"
```

A `Button` stores the function it should run in `self.on_click`, and calls it when clicked. So you write `Button("Quit", self.quit)`, **not** `self.quit()`. With brackets, it would run straight away.

## Do it

1. Add these helpers to the bottom of `ui/draw.py`:

```python
def lighter(color, amount=30):
    return tuple(min(255, part + amount) for part in color)


def darker(color, amount=30):
    return tuple(max(0, part - amount) for part in color)


def text_color_for(background):
    """Dark text on light colours, white text on dark colours."""
    red, green, blue = background[:3]
    brightness = red * 0.3 + green * 0.59 + blue * 0.11
    return theme.INK if brightness > 160 else theme.WHITE


def shadow(surface, rect, radius=12, offset=5, alpha=70):
    layer = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(layer, (0, 0, 0, alpha), layer.get_rect(), border_radius=radius)
    surface.blit(layer, rect.move(0, offset))


def panel(surface, rect, color=theme.PAPER, radius=14, border=None):
    """A rounded box with a soft shadow underneath."""
    rect = pygame.Rect(rect)
    shadow(surface, rect, radius)
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, width=3, border_radius=radius)
    return rect
```

2. Create `ui/widgets.py`:

```python
import pygame

from ui import theme
from ui.draw import darker, lighter, shadow, text, text_color_for


class Button:
    def __init__(self, label, on_click, rect=(0, 0, 160, 50), color=theme.BLUE, size=20):
        self.label = label
        self.on_click = on_click      # the function to run when clicked
        self.rect = pygame.Rect(rect)
        self.color = color
        self.size = size
        self.enabled = True

    def handle_event(self, event):
        """Returns True if this click landed on the button (even a disabled one)."""
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        # TODO: if the click (event.pos) is NOT inside self.rect, return False
        if self.enabled:
            self.on_click()
        return True

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())

        if not self.enabled:
            color = theme.DISABLED
        elif hovered:
            color = lighter(self.color, 25)
        else:
            color = self.color

        body = self.rect.move(0, -2) if hovered and self.enabled else self.rect   # lift it up a bit
        shadow(surface, self.rect, radius=10, offset=4, alpha=60)
        pygame.draw.rect(surface, color, body, border_radius=10)
        pygame.draw.rect(surface, darker(color, 35), body, width=2, border_radius=10)
        text(surface, self.label, body.center, self.size, text_color_for(color), bold=True, anchor="center")
```

3. In `ui/app.py`, add `from ui.widgets import Button`. At the end of `__init__`:

```python
        x = 800 - 150
        self.buttons = [
            Button("New game", self.new_game, (x, 440, 300, 62), theme.GREEN, 24),
            Button("Continue", self.new_game, (x, 520, 300, 62), theme.BLUE, 24),
            Button("Rules", self.new_game, (x, 600, 300, 62), theme.PURPLE, 24),
            Button("Quit", self.quit, (x, 680, 300, 62), theme.RED, 24),
        ]
        self.buttons[1].enabled = False     # nothing to continue yet
```

   Add two methods to `App`:

```python
    def new_game(self):
        print("Coming soon!")

    def quit(self):
        pass    # TODO: make the game loop stop
```

4. In `run()`: every event goes to every button (add an `else:` to the event `if`), and every button draws itself after the logo:

```python
                else:
                    for button in self.buttons:
                        button.handle_event(event)
```

```python
            for button in self.buttons:
                button.draw(self.window)
```

## Check it

- [ ] Hovering makes a button lighter and lifts it up
- [ ] "Continue" is grey and does nothing
- [ ] "New game" prints *Coming soon!* in the terminal, **once** per click
- [ ] "Quit" closes the game

## Save

Commit message: `Quest 04: a reusable Button`
