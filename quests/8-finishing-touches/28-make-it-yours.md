# Quest 28 · Make it yours

**Goal:** play a whole real game with people, fix whatever goes wrong, then add something that's completely your own idea.

## Part 1: the big playtest (about half the lesson)

Play a full game with at least 3 people. Keep this file open and write down **anything** odd:

- something that looked wrong, or text that didn't fit
- a moment where nobody knew what to click
- any crash (copy the last lines of the error!)

Then fix them, one at a time. For each bug: can you write a test that fails **before** your fix and passes after? That's how professionals stop a bug from ever coming back.

**Bugs found:**
-
-
-

## Part 2: your own feature

Pick one (or invent your own):

| Idea | Where it goes | How hard |
|---|---|---|
| Your own board: your town's streets, or your favourite game's places | `data/board.json` | ⭐ |
| New Chance cards you made up | `data/chance.json` (+ a new action in `draw_card`?) | ⭐ |
| House rule: tax money goes into a Free Parking jackpot | `logic/game.py` | ⭐⭐ |
| Sounds for dice, cash and jail | `ui/play_screen.py`, `pygame.mixer` | ⭐⭐ |
| Stats on the winner screen (most rent collected, times in jail) | `Player` + `screens.py` | ⭐⭐ |
| Choose your token shape (car, hat, dog) instead of a letter | `draw.token` + `SetupScreen` | ⭐⭐⭐ |
| A computer player that makes its own decisions | a new `logic/robot.py` | ⭐⭐⭐⭐ |

Whichever you pick: rules go in `logic/` (with a test), and anything visual goes in `ui/`.

## Save

Commit message: `Quest 28: <what you added>`

**You built a complete Monopoly game: about 2,000 lines of Python in around 30 files, with tests.** 🎉
