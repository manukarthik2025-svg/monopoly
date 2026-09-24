# Quest 04: Open a real game window

## Why this quest
This is the first code that becomes part of the actual game, not throwaway practice. Every future quest builds on top of this window. Keep it boring and reliable before adding anything exciting.

## Your tasks

1. Create `monopoly/app.py` with an `App` class (see starter code).
2. Create `main.py` at the project root that imports `App` and runs it.
3. The window should be 1280x800, resizable, titled "Monopoly".
4. The loop should: read events, update, draw — in that order, every frame.
5. Closing the window (the X button) should exit cleanly, no errors in the terminal.
6. Limit the game to 60 frames per second using `pygame.time.Clock`.
7. Fill the background with one solid color.
8. Render the text "Monopoly" and draw it centered in the window.

## Starter code

`monopoly/app.py`:
```python
import pygame

class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Monopoly")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 64)
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass  # nothing to update yet

    def draw(self):
        self.window.fill((20, 90, 40))
        # TODO: render "Monopoly" with self.font and blit it centered
        # in self.window (hint: text.get_rect(center=self.window.get_rect().center))
        pygame.display.flip()
```

`main.py`:
```python
from monopoly.app import App

# TODO: create an App and call .run() on it
```

## Test it yourself
Run `python main.py` from the project root (with your venv active). Confirm: the window opens at 1280x800, shows "Monopoly" centered on a solid background, doesn't freeze or spike your CPU fan, and closes instantly when you click the X.

## Checkpoint
```text
git commit -m "Create Pygame window and clean exit"
```
You just built the app shell that every screen, button, and board drawing in the rest of the project will run inside.

## Stuck? Try this
- `ModuleNotFoundError: No module named 'monopoly'` → run `python main.py` from the project's root folder, not from inside `monopoly/`, and make sure `monopoly/__init__.py` exists.
- Window doesn't close → you're missing the `pygame.QUIT` check inside the `for event in pygame.event.get()` loop, or `handle_events` isn't being called.
- Text is invisible → check the color you rendered it in isn't the same as the background color.
