# Quest 05: Build a reusable Button class

## Why this quest
You're about to need dozens of buttons: menu options, Roll Dice, Buy, Auction, End Turn. Instead of copy-pasting rectangle-and-text code everywhere (Practice B style), you'll write it once as a class and reuse it everywhere — this is exactly the class idea from Quest 03, applied to something visual.

## Your tasks

1. Create `monopoly/ui.py`.
2. Write a `Button` class storing: a `pygame.Rect`, a label string, a callback function to run when clicked (`on_click`), whether the mouse is hovering, and whether it's disabled.
3. Give it `handle_event(self, event)`: track hovering on `MOUSEMOTION`, and call `on_click()` on `MOUSEBUTTONDOWN` inside the rect — but only if not disabled.
4. Give it `draw(self, surface, font)`: pick a color based on disabled/hovered/normal, draw the rectangle, then draw the label centered inside it.
5. In `app.py`, create one test `Button` in `__init__` that prints a message when clicked, and call its `handle_event` and `draw` from the app's loop.

## Starter code

`monopoly/ui.py`:
```python
import pygame

NORMAL_COLOR = (70, 110, 70)
HOVER_COLOR = (95, 150, 95)
DISABLED_COLOR = (90, 90, 90)
TEXT_COLOR = (255, 255, 255)

class Button:
    def __init__(self, rect, label, on_click=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.hovered = False
        self.disabled = False

    def handle_event(self, event):
        if self.disabled:
            return
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        # TODO: if event.type == pygame.MOUSEBUTTONDOWN and the click is inside
        # self.rect, call self.on_click() if it's not None

    def draw(self, surface, font):
        # TODO: pick NORMAL_COLOR, HOVER_COLOR, or DISABLED_COLOR based on
        # self.disabled and self.hovered, then draw the rect and the
        # centered label text (reuse the centering trick from Quest 04)
        pass
```

Add to `monopoly/app.py` inside `__init__` (after `self.font = ...`):
```python
from monopoly.ui import Button

def say_hello():
    print("Button clicked!")

self.test_button = Button((540, 400, 200, 60), "TEST", on_click=say_hello)
```

And wire it into the existing methods:
```python
# inside handle_events(), for each event:
self.test_button.handle_event(event)

# inside draw(), after filling the background:
self.test_button.draw(self.window, self.font)
```

## Test it yourself
Run `python main.py`. Move your mouse over the TEST button and confirm the color changes. Click it several times and confirm `Button clicked!` prints once per click, not zero and not multiple times per click.

## Checkpoint
```text
git commit -m "Add reusable Button class"
```
This one class will power the entire menu, every in-game action button, and every dialog for the rest of the project.

## Stuck? Try this
- Clicking anywhere prints the message → you forgot the `collidepoint` check, so every click counts.
- Multiple prints per click → you're calling `on_click()` on every event type instead of just `MOUSEBUTTONDOWN`, or calling it from inside `draw()` by mistake.
- Hover color never changes → confirm `handle_event` is actually being called every frame from your event loop, for every event, not just once.
