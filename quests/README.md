# Quests

One quest = one lesson, about an hour. Do them in order. Every quest ends with the game still working.

## How a quest works

| Part | What it means |
|---|---|
| **Goal** | what you'll have at the end |
| **Idea** | the new Python thing you'll learn (not every quest has one) |
| **Do it** | the steps. Code marked `# TODO` is yours to write. |
| **Check it** | how to know it worked |
| **Save** | commit your work (see below) |

**Saving your work:** open Source Control (`Ctrl+Shift+G`), type the message the quest gives you, click **Commit**. Then if you break something later, you can always get back to a version that worked.

**Stuck?** Read the *last* line of the error first. It usually names the file and line number.

## Progress

Tick a quest when you finish it: change `[ ]` to `[x]`.

**1 · Getting started**
- [ ] [01 · Fix your first window](1-getting-started/01-fix-your-first-window.md)
- [ ] [02 · Many files, one game](1-getting-started/02-many-files-one-game.md)

**2 · Looking good**
- [ ] [03 · Colours and a logo](2-looking-good/03-colours-and-a-logo.md)
- [ ] [04 · A button class](2-looking-good/04-a-button-class.md)
- [ ] [05 · Screens](2-looking-good/05-screens.md)

**3 · The board**
- [ ] [06 · Players and spaces](3-the-board/06-players-and-spaces.md)
- [ ] [07 · The board as data](3-the-board/07-the-board-as-data.md)
- [ ] [08 · Board maths](3-the-board/08-board-maths.md)
- [ ] [09 · Paint the board](3-the-board/09-paint-the-board.md)

**4 · Taking turns**
- [ ] [10 · Who's playing?](4-taking-turns/10-whos-playing.md)
- [ ] [11 · Roll and move](4-taking-turns/11-roll-and-move.md)
- [ ] [12 · The sidebar](4-taking-turns/12-the-sidebar.md)
- [ ] [13 · Doubles and jail](4-taking-turns/13-doubles-and-jail.md)

**5 · Property**
- [ ] [14 · Buying](5-property/14-buying.md)
- [ ] [15 · Title deeds](5-property/15-title-deeds.md)
- [ ] [16 · Rent](5-property/16-rent.md)
- [ ] [17 · Auctions](5-property/17-auctions.md)

**6 · Cards**
- [ ] [18 · Card decks](6-cards/18-card-decks.md)
- [ ] [19 · Cards that move you](6-cards/19-cards-that-move-you.md)

**7 · Building an empire**
- [ ] [20 · Mortgages](7-empire/20-mortgages.md)
- [ ] [21 · Houses and hotels](7-empire/21-houses-and-hotels.md)
- [ ] [22 · Debt](7-empire/22-debt.md)
- [ ] [23 · Bankruptcy and winning](7-empire/23-bankruptcy-and-winning.md)

**8 · Finishing touches**
- [ ] [24 · Trading rules](8-finishing-touches/24-trading-rules.md)
- [ ] [25 · The trade screen](8-finishing-touches/25-trade-screen.md)
- [ ] [26 · Save and load](8-finishing-touches/26-save-and-load.md)
- [ ] [27 · Juice](8-finishing-touches/27-juice.md)
- [ ] [28 · Make it yours](8-finishing-touches/28-make-it-yours.md)

## Commands

| To... | Type this in the terminal |
|---|---|
| play | `python main.py` |
| run all the tests | `python -m pytest` |
| run one test file | `python -m pytest tests/test_rent.py` |
| stop a stuck program | `Ctrl+C` in the terminal |

Keep the explorer tidy: click the **Collapse Folders** button at the top of the explorer whenever it gets long.
