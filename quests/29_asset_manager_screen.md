# Quest 29: An asset manager screen

## Why this quest
Buying and selling houses needs somewhere to happen outside the middle of a dice roll. This quest builds the screen; the actual building/mortgage rules come in the next two quests.

## Your tasks

1. In `monopoly/screens.py`, create an `AssetManagerScreen` class, reachable via a new button on `GameScreen` (enabled any time it's not a phase that blocks it, like `AUCTION` or `IN_JAIL_DECISION` — for now, allow it during `TURN_END` and `WAITING_FOR_ROLL`).
2. List every property the current player owns, grouped by color group, showing: name, current rent (use `calculate_rent` from Quest 24 with a dice_total of, say, the last rolled dice), house count, and mortgage status.
3. For each property, show Build/Sell/Mortgage/Unmortgage buttons — they can all be disabled (grayed out, doing nothing) for this quest; Quest 30 and 31 will wire up the real logic and enable/disable rules.
4. Add a Back button returning to `GameScreen`.
5. When a button is disabled, show a one-line reason next to it (e.g. "needs full color group") — build this as a small helper function that returns `None` or a reason string, since Quest 30/31 will need the exact same "why can't I do this" logic for enabling/disabling.

## Starter code
```python
class AssetManagerScreen:
    def __init__(self, app, state):
        self.app = app
        self.state = state
        self.back_button = Button((40, 40, 120, 50), "Back", on_click=self.go_back)

    def go_back(self):
        from monopoly.screens import GameScreen
        self.app.go_to(GameScreen(self.app, self.state))

    def owned_properties(self):
        player = self.state.current_player()
        # TODO: return the list of Space objects in state.spaces whose index
        # is in player.owned, sorted by group then index for a tidy display
        pass

    def handle_event(self, event):
        self.back_button.handle_event(event)
        # TODO: handle_event for each property's row of buttons once they exist

    def draw(self, surface):
        # TODO: for each property from owned_properties(), draw its name,
        # rent, house count, and mortgage status in a row; draw disabled
        # Build/Sell/Mortgage/Unmortgage buttons next to each row
        self.back_button.draw(surface, self.app.font)
```

Add an "Assets" button to `GameScreen`:
```python
self.assets_button = Button((800, 550, 160, 60), "Assets", on_click=self.open_assets)

def open_assets(self):
    from monopoly.screens import AssetManagerScreen
    self.app.go_to(AssetManagerScreen(self.app, self.state))
```

## Test it yourself
Run the game, buy a couple of properties, click Assets. Confirm every owned property is listed with correct info, grouped sensibly, and Back returns you to exactly the same point in the game (same phase, same dice, nothing reset).

## Checkpoint
```text
git commit -m "Add asset manager screen (read-only for now)"
```
This is the dashboard every building and mortgage decision in the next two quests will happen through.

## Stuck? Try this
- Returning from Assets resets the game → make sure `AssetManagerScreen` is given the *same* `state` object (not a new one) and passes it right back to `GameScreen` on Back.
- Properties show up ungrouped or in a strange order → sort using a tuple key, e.g. `sorted(properties, key=lambda s: (s.group or "", s.index))`.
