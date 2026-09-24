# Quest 07: A real Player class

## Why this quest
This is the same idea as Practice C (Quest 03), but built for real inside the project, with every field the finished game will need for a player.

## Your tasks

1. Create `monopoly/models.py`.
2. Write a `Player` class storing: `player_id`, `name`, `token`, `cash` (starts at 1500), `position` (starts at 0), `owned` (a list of space indexes they own, starts empty), `in_jail` (starts `False`), `jail_turns` (starts `0`), `jail_cards` (starts `0`), and `bankrupt` (starts `False`).
3. Add a method `is_active(self)` that returns `True` if the player is not bankrupt.
4. Temporarily, at the bottom of `models.py` under `if __name__ == "__main__":`, create two players and print their names and starting cash — this is just to check your class works. Delete this block once it does.

## Starter code

`monopoly/models.py`:
```python
class Player:
    def __init__(self, player_id, name, token):
        self.player_id = player_id
        self.name = name
        self.token = token
        self.cash = 1500
        self.position = 0
        self.owned = []
        self.in_jail = False
        self.jail_turns = 0
        self.jail_cards = 0
        self.bankrupt = False

    def is_active(self):
        # TODO: return True if this player is not bankrupt
        pass


if __name__ == "__main__":
    p1 = Player(0, "Alice", "hat")
    p2 = Player(1, "Bob", "car")
    # TODO: print each player's name and cash
```

## Test it yourself
Run `python -m monopoly.models` from the project root. Confirm it prints both players' names with 1500 cash each, no errors. Then delete the `if __name__ == "__main__":` block — it was only for checking your work.

## Checkpoint
```text
git commit -m "Add real Player class"
```
Every player in every game you play from now on is one of these objects.

## Stuck? Try this
- `python -m monopoly.models` fails with an import error → make sure you're running it from the project root, not from inside `monopoly/`.
- Forgot what `self` means → re-read the class explanation in Quest 03; every method needs `self` as its first parameter so it knows *which* player it's working on.
