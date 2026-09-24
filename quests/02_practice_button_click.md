# Quest 02: Draw and click a button (practice)

## Why this quest
Every screen in the real game is built from a loop that reads input, updates something, and draws the result. This practice file gets that loop under your fingers with the simplest possible example: one clickable rectangle. Delete this file when you're done.

## New idea(s)
**The game loop and events.** A Pygame program doesn't run top-to-bottom once like your scripts so far — it runs the same block of code, called the "game loop," dozens of times per second, forever, until you close the window. Each time through the loop it: (1) checks what happened since last time (did you click, press a key, close the window — these are called "events"), (2) updates anything that needs to change, (3) redraws the screen. Nothing appears on screen until you `pygame.display.flip()`.

```python
import pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 30))
    pygame.display.flip()
pygame.quit()
```

## Your tasks

1. Create `scratch_practice_b.py`.
2. Open a 400x300 window with a game loop like the one above.
3. Make a `pygame.Rect` for a button, roughly 100 wide and 50 tall, centered in the window.
4. Every frame, draw the rectangle and the text `ROLL` centered inside it.
5. In the event loop, check for `pygame.MOUSEBUTTONDOWN`. If it happened and `button_rect.collidepoint(event.pos)` is true, print `Button clicked`.

## Starter code
```python
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
font = pygame.font.SysFont(None, 36)
button_rect = pygame.Rect(150, 125, 100, 50)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # TODO: if button_rect.collidepoint(event.pos), print "Button clicked"
            pass

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (70, 110, 70), button_rect)
    # TODO: render the text "ROLL" and blit it centered inside button_rect
    pygame.display.flip()

pygame.quit()
```

## Test it yourself
Run `python scratch_practice_b.py`. Click inside the rectangle five times — you should see `Button clicked` printed exactly five times in the terminal. Click outside it — nothing should print. Close the window with the X button — it should close instantly, not freeze.

## Checkpoint
```text
git commit -m "Practice B: clickable button in a Pygame window"
```
You just built the loop and click-detection pattern every button in the finished game will reuse.

## Stuck? Try this
- Window opens but freezes immediately → you're missing the `pygame.QUIT` check, or it's outside the `while running` loop.
- Click does nothing → print `event.pos` to see what coordinates you're actually clicking, and compare against `button_rect`.
- Text doesn't show up → `font.render("ROLL", True, (255,255,255))` returns a surface; you must `screen.blit(surface, position)` it, and do this *after* filling the background each frame or it gets painted over.
