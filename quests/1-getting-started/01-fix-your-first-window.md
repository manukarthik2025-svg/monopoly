# Quest 01 · Fix your first window

**Goal:** your window from last time shows your own picture, full screen, and `Esc` closes it.
**Files:** `sandbox/first_window.py` (yours!) and a new `assets/background.png`

## Get set up

1. In VS Code: **File → Open Folder** → choose the `monopoly` folder. Always open this folder, not the one above it.
2. Open the terminal (`` Ctrl+` ``) and run:
   ```text
   pip install -r requirements.txt
   ```
3. Your code from last time is now in `sandbox/`. That folder is for practice code that isn't part of the game.

## Idea: the game loop

Every game is one loop that runs about 60 times a second:

```text
while running:
    1. events   what did the player do? (keys, clicks, closing the window)
    2. update   change things (move, count, score)
    3. draw     paint the screen, then flip() to show it
```

Code after the loop only runs once the game is over.

## Do it

1. Run it: `python sandbox/first_window.py`. It crashes. Read the **last line** of the error. What can't it find?
2. Choose a background picture: a Monopoly board, something you drew, anything you like. Make a folder called `assets` (next to `sandbox`), put the picture inside, and rename it `background.png`.
3. Change the load line to use `"assets/background.png"`.
4. Run it again. You get a black screen, and you can't close it! (`Alt+F4` gets you out.) Using the game loop idea, work out why nothing shows. Where are `blit` and `flip`?
5. Fix it:
   - Move the drawing inside the loop.
   - Pressing `Esc` sets `running = False`. Full screen has no ✕ button!
   - Stretch the picture to fit: `bg_img = pygame.transform.smoothscale(bg_img, screen.get_size())`
   - Add `clock = pygame.time.Clock()` before the loop and `clock.tick(60)` at the end of the loop. Without it the loop runs thousands of times a second and your laptop fan gets loud.
   - Delete `import random`, since nothing uses it.

<details><summary>Only if you're really stuck: one way it can look</summary>

```python
import pygame

pygame.init()

# Screen setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
bg_img = pygame.image.load("assets/background.png")
bg_img = pygame.transform.smoothscale(bg_img, screen.get_size())
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(bg_img, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```
</details>

## Check it

- [ ] Your picture fills the whole screen
- [ ] `Esc` closes it straight away

Your picture comes back in Quest 03 as the game's background.

## Save

Commit message: `Quest 01: fix my first window`

⭐ **Extra:** before `flip()`, draw a rectangle with `pygame.draw.rect(screen, (255, 255, 255), (100, 100, 300, 150))`. Then make it follow the mouse using `pygame.mouse.get_pos()`.
