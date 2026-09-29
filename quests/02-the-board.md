# Lesson 2: the board

**Goal:** the 40 squares of a Monopoly board, drawn by loops.

**New idea:** a list of positions. We build it once, before the game loop, and then draw from it every frame. Next lesson your token uses the same list to know where to stand.

## 1. One square

Here's the new pygame part. Put it inside the game loop, after the background and before `flip`:

```python
pygame.draw.rect(screen, (255, 255, 255), (20, 20, 60, 60), 2)
```

- `(255, 255, 255)` is the colour (red, green, blue).
- `(20, 20, 60, 60)` is x, y, width, height.
- `2` means an outline 2 pixels thick. Take it away and see what happens.

## 2. Think of the board as a grid

The board is 11 × 11 squares. Each square has a **col** (0 on the left, 10 on the right) and a **row** (0 at the top, 10 at the bottom).

Go is in the bottom-right corner (col 10, row 10). Players move to the left along the bottom, then up, then right, then down.

| side | squares | col | row |
|---|---|---|---|
| bottom | 0–9 | 10, 9, 8 … 1 | 10 |
| left | 10–19 | 0 | 10, 9, 8 … 1 |
| top | 20–29 | 0, 1, 2 … 9 | 0 |
| right | 30–39 | 10 | 0, 1, 2 … 9 |

Each side has 10 squares. The next corner belongs to the next side.

## 3. Build the list

Put this before `while running:`. It runs once, so it doesn't belong in the game loop.

```python
squares = []
for i in range(10):
    squares.append((10 - i, 10))
```

Check it with `print(squares)`. Is the first one Go?

Now write the other three loops yourself, using the table. When you're done, `print(len(squares))` should say **40**.

## 4. Draw the list

Inside the game loop, replace your one square with a loop over `squares`:

- `square[0]` is the col, and `square[1]` is the row.
- x on screen = `20 + col * 60`, and y on screen = `20 + row * 60`.

Run it. You should see a square ring of 40 squares.

## 5. Where's Go?

Draw `squares[0]` again, but filled (no `2`) and in a different colour. Is it in the bottom-right corner? Try `squares[10]` (Jail) and `squares[20]` (Free Parking).

## 6. Make it yours

- Pick your own colours. Try drawing each square filled first, then an outline on top.
- Change the square size from 60 to 50. How many places did you have to change? Put it in a variable called `size`, so next time it's one change.

## Done when

- [ ] 40 squares make a ring around the board
- [ ] Go is a different colour, in the bottom-right corner
