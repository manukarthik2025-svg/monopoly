# Quest 25: All three ways into jail

## Why this quest
You already built "sent to jail via Go To Jail" and "sent to jail via three doubles." This quest makes sure jail entry is consistent everywhere, and prepares the ground for actually getting *out* of jail next quest.

## Your tasks

1. Confirm `send_to_jail` (Quest 18) always does exactly these things, in order: sets `player.position` to the jail space, sets `player.in_jail = True`, resets `player.jail_turns` to `0` (new field usage — you added this to `Player` back in Quest 07), and ends the turn without paying Go money regardless of the numeric position crossed.
2. Chance and Community Chest "Go to Jail" cards (built in Quest 28) should also call this same function — don't write a second version.
3. Add a small visible indicator in the UI when a player is in jail (e.g. the token draws with a small "J" badge, or the player panel shows "(in jail)" next to their name).
4. Write a test confirming a player already past the jail's board index doesn't collect Go money when teleported there directly.

## Starter code
Double-check your `send_to_jail` from Quest 18 now looks like this:
```python
def send_to_jail(player, spaces):
    player.position = find_jail_index(spaces)
    player.in_jail = True
    player.jail_turns = 0
```
Note there's no call to `pay()` here at all — direct-to-jail teleportation never awards Go money, which is why this function doesn't go through `move_player`.

For the UI indicator, in `GameScreen.draw`, wherever you draw player tokens (Quest 17):
```python
if player.in_jail:
    # TODO: draw a small marker (e.g. a yellow ring, or the letter "J")
    # near this player's token
    pass
```

## Test it yourself
Add to `tests/test_jail.py` (new file):
```python
from monopoly.models import Player, Space
from monopoly.rules import send_to_jail, find_jail_index

def test_send_to_jail_resets_jail_turns():
    player = Player(0, "Alice", "hat")
    player.jail_turns = 2
    spaces = [Space(0, "Go", "GO"), Space(10, "Jail", "JAIL")]
    send_to_jail(player, spaces)
    assert player.in_jail is True
    assert player.jail_turns == 0
    assert player.position == 10
```
Run `python -m pytest tests/test_jail.py -v`. Then play manually: trigger all three ways into jail (land on Go To Jail, roll three doubles, and — once Quest 28 exists — draw the card) and confirm each one lands the player in the same place with the same state.

## Checkpoint
```text
git commit -m "Consistent jail entry from all three triggers"
```
Small quest, but it prevents a very common bug: three different half-working copies of "go to jail" scattered across the codebase that slowly drift out of sync.

## Stuck? Try this
- Different entry points behave slightly differently → search your code for anywhere you set `player.position` to the jail index directly instead of calling `send_to_jail` — replace it.
