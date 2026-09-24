# Quest 06: Menu and screen switching

## Why this quest
The game needs a main menu, a setup screen, the actual board, a help screen, and a winner screen. Rather than cramming all of that into one giant `draw()` method, you'll give each screen its own small class, and let the app hold "whichever screen is currently active."

## New idea(s)
**Swapping which object handles the work.** Instead of one big pile of `if screen == "menu": ... elif screen == "game": ...` code, you can give each screen its own class with the same two method names (`handle_event`, `draw`), and just keep a variable pointing at "the current one." Switching screens is then just reassigning that variable — nothing else in the loop needs to change.

```python
class Cat:
    def speak(self):
        print("meow")

class Dog:
    def speak(self):
        print("woof")

current_animal = Cat()
current_animal.speak()      # meow
current_animal = Dog()
current_animal.speak()      # woof — same line of code, different object
```

## Your tasks

1. Create `monopoly/screens.py`.
2. Write a `MenuScreen` class with `__init__(self, app)` (store the app so it can switch screens later), `handle_event(self, event)`, and `draw(self, surface)`.
3. Give `MenuScreen` four `Button`s: New Game, Load Game, Rules, Quit — laid out vertically.
4. Write `SetupScreen` and `HelpScreen` as near-empty classes for now, each with a Back button that returns to the menu.
5. In `App.__init__`, replace the test button with `self.screen = MenuScreen(self)`.
6. Add a method `App.go_to(self, screen)` that sets `self.screen = screen`.
7. Update `App.handle_events` and `App.draw` to delegate to `self.screen.handle_event(event)` / `self.screen.draw(self.window)`.
8. New Game → `SetupScreen`. Rules → `HelpScreen`. Quit → set `self.running = False`. Back buttons → `MenuScreen`.

## Starter code

`monopoly/screens.py`:
```python
from monopoly.ui import Button

class MenuScreen:
    def __init__(self, app):
        self.app = app
        self.buttons = [
            Button((540, 250, 200, 60), "New Game", on_click=self.new_game),
            Button((540, 330, 200, 60), "Load Game", on_click=lambda: None),
            Button((540, 410, 200, 60), "Rules", on_click=self.show_help),
            Button((540, 490, 200, 60), "Quit", on_click=self.quit),
        ]

    def new_game(self):
        self.app.go_to(SetupScreen(self.app))

    def show_help(self):
        self.app.go_to(HelpScreen(self.app))

    def quit(self):
        self.app.running = False

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface, self.app.font)


class SetupScreen:
    def __init__(self, app):
        self.app = app
        # TODO: add a Back button at, say, (40, 40, 120, 50) that calls
        # self.app.go_to(MenuScreen(self.app))

    def handle_event(self, event):
        pass  # TODO

    def draw(self, surface):
        pass  # TODO


class HelpScreen:
    def __init__(self, app):
        self.app = app
        # TODO: same Back button pattern as SetupScreen

    def handle_event(self, event):
        pass  # TODO

    def draw(self, surface):
        pass  # TODO
```

In `monopoly/app.py`, replace the test button setup with:
```python
from monopoly.screens import MenuScreen
# ...
self.screen = MenuScreen(self)
```
and add:
```python
def go_to(self, screen):
    self.screen = screen
```
Then change `handle_events` to call `self.screen.handle_event(event)` per event, and `draw` to call `self.screen.draw(self.window)`.

## Test it yourself
Run `python main.py`. Click New Game — you should land on a screen with a Back button. Click Back — you're on the menu again. Same for Rules. Click every button several times in a row; no screen should ever leave you with no way back to the menu, and Quit should close the window.

## Checkpoint
```text
git commit -m "Add reusable menu buttons and screen switching"
```
You just built the navigation skeleton every screen in the finished game will plug into.

## Stuck? Try this
- Clicking New Game does nothing → check `self.app.go_to(...)` is actually being called, and that `App.draw`/`handle_events` reference `self.screen`, not a screen you set once and never update.
- `AttributeError: 'SetupScreen' object has no attribute 'buttons'` → if `SetupScreen.draw` loops over `self.buttons` but you never created that list, add an empty `self.buttons = []` plus your Back button.
- Old screen's buttons still respond after switching → make sure `App.handle_events` only calls `self.screen.handle_event`, not every screen you've ever created.
