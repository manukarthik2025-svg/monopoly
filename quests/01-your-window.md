# Lesson 1: your window, your picture

**Goal:** `Monopoly.py` opens a window showing *your* picture, and you can close it.

**New idea:** the game loop. Everything inside `while running:` runs again and again, hundreds of times a second. Anything after it runs once, when the game ends.

## 1. A window you can close

Full screen has no close button. Change `set_mode` to a fixed size:

```python
screen = pygame.display.set_mode((1000, 700))
```

Run it. You should get a window with an X button. (It may crash on the picture. That's step 2.)

## 2. Your picture

- Pick any picture you like for the background.
- Save it next to `Monopoly.py` and name it `Monopoly_bg.png`.
- In VS Code, use **File → Open Folder** on the `monopoly` folder, so Python can find the picture.

Run it. No crash now, but the window is black. Why?

## 3. Draw inside the loop

Look at your code. Which lines are inside the loop, and which run only after it ends?

Hint: in Python, the indentation decides what's inside the loop. Move the two drawing lines so they happen every time round.

## 4. Escape quits

A key press is an event, just like clicking X. Here's the new pygame part:

```python
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_ESCAPE:
        ...
```

Where does it go, and what goes in the `...`? Look at how `QUIT` works.

## 5. Make the picture fit

Your picture probably isn't exactly 1000 × 700. Stretch it to fit, once, just after you load it:

```python
bg_img = pygame.transform.scale(bg_img, (1000, 700))
```

## 6. Make it yours

- Give the window a title: `pygame.display.set_caption("...")`. You choose the words.
- Try other numbers instead of 1000 and 700. What changes? Pick the size you like.

## Done when

- [ ] Your picture fills the window
- [ ] Both the X button and Escape close it
