# Quest 02 · Many files, one game

**Goal:** `python main.py` opens the real game window, built from files in different folders.
**New files:** `main.py`, `logic/__init__.py`, `ui/__init__.py`, `ui/app.py`

## Idea: modules and packages

- Every `.py` file is a **module**.
- A folder with an `__init__.py` file inside is a **package**. The `__init__.py` can be empty. It just tells Python "you can import from this folder".
- `from ui.app import App` means: go into the folder `ui`, open `app.py`, and bring back the thing called `App`.

The finished game has about 30 files. Each one does **one job**, so you always know where to look. The map is in the [main README](../../README.md).

The two main folders:
- `logic/`: the rules of Monopoly. It never uses pygame.
- `ui/`: everything you see. All the pygame code goes here.

## Do it

1. Make two folders, `logic` and `ui`. Put an empty file called `__init__.py` in each one.
2. Create `ui/app.py`:

```python
import os

import pygame


class App:
    """Opens the window and runs the game loop."""

    def __init__(self):
        # Window settings: sharp on high-resolution screens, and smooth when resized.
        os.environ["SDL_WINDOWS_DPI_AWARENESS"] = "permonitorv2"
        os.environ["SDL_RENDER_SCALE_QUALITY"] = "1"

        pygame.init()
        self.window = pygame.display.set_mode((1600, 900), pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("Monopoly")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("segoeui", 90)

    def run(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

            self.window.fill((22, 84, 62))
            words = self.font.render("Monopoly", True, (255, 255, 255))
            self.window.blit(words, words.get_rect(center=(800, 450)))
            # TODO: draw "a game by Manu" underneath, in a smaller font

            pygame.display.flip()

        pygame.quit()
```

3. Create `main.py` in the top folder (next to `README.md`):

```python
from ui.app import App

App().run()
```

## Idea: the 1600 × 900 canvas

`pygame.SCALED` means we **always** draw on a 1600 × 900 canvas, and pygame stretches it to fit the window. So `(800, 450)` is always the exact middle, even at full screen. All the maths in this game relies on that.

## Check it

Run `python main.py`.
- [ ] A green window with "Monopoly" in the middle
- [ ] `F11` goes full screen and back
- [ ] Drag the window's corner: everything stretches but stays centred

## Save

Commit message: `Quest 02: main.py and the App class`
