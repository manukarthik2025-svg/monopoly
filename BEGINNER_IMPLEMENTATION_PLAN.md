# Beginner's Step-by-Step Monopoly Project Plan

This guide is for someone building their first big Python project. You are not expected to know everything before you begin. You will learn by making one small working piece at a time.

The goal is a complete local Monopoly-style game for 2-6 people using one computer. The graphics will be simple, but the game rules will be detailed.

## 1. The most important rule: build a little, test a little

Do not try to write the whole game at once. Large games are made from many small programs that work together.

For every step:

1. Read the goal.
2. Make the smallest version that could work.
3. Run it.
4. Fix errors before adding anything else.
5. Save a working copy with Git.
6. Take a break when a checkpoint is complete.

It is normal for code not to work on the first try. An error message is a clue, not a failure.

## 2. What you will learn

This project will teach you how to use:

- Variables, numbers, strings, lists, and dictionaries.
- `if`, `elif`, and `else` decisions.
- `for` and `while` loops.
- Functions that do one clear job.
- Classes and objects for players, properties, and the game.
- Modules, which split a large program into smaller files.
- JSON files for board information and saved games.
- Pygame for windows, drawing, mouse clicks, and keyboard input.
- Tests to check game rules automatically.
- Git to save safe checkpoints.

You do not need to master all of these first. Learn each one when the plan reaches it.

## 3. Rules for keeping the project manageable

- Keep functions short. If a function is hard to explain in one sentence, split it.
- Give things clear names such as `current_player`, not names such as `x`.
- Put game rules in normal Python files, not inside drawing code.
- Make the game work with plain shapes before adding pictures or sounds.
- Finish the current milestone before starting an exciting later feature.
- Never copy a large piece of code without reading it line by line.
- When stuck, create the smallest example that still has the problem.

## 4. Tools to install

Install Python 3.12 or newer. In the project folder, create a virtual environment and install Pygame and pytest.

PowerShell commands:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pygame pytest
```

Later, put the dependencies in `requirements.txt`:

```text
pygame
pytest
```

Useful commands:

```powershell
python main.py
python -m pytest
```

The first command runs the game. The second runs the automatic rule checks.

## 5. The finished folder structure

Do not create every file immediately. Add each file when its step asks for it.

```text
monopoly/
|-- main.py
|-- requirements.txt
|-- README.md
|-- PLAN.md
|-- BEGINNER_IMPLEMENTATION_PLAN.md
|-- data/
|   |-- board.json
|   |-- chance.json
|   `-- community_chest.json
|-- monopoly/
|   |-- __init__.py
|   |-- app.py
|   |-- models.py
|   |-- rules.py
|   |-- cards.py
|   |-- persistence.py
|   |-- screens.py
|   `-- ui.py
|-- saves/
`-- tests/
    |-- test_movement.py
    |-- test_properties.py
    |-- test_jail.py
    |-- test_cards.py
    `-- test_bankruptcy.py
```

What the folders mean:

- `data` holds facts such as property names, prices, and card text.
- `monopoly` holds the Python code for the game.
- `saves` holds saved matches.
- `tests` holds small programs that check the rules.

## 6. Before the real game: three tiny practice programs

These exercises should be separate scratch files. They can be deleted later.

### Practice A: move around a board

Make a list containing the numbers 0 through 39. Start a player at 0, roll two random dice, and move them. Use `% 40` so moving past space 39 returns to space 0.

Learn:

- Lists.
- Random numbers.
- Functions.
- The remainder operator `%`.

Success check: the program prints ten rolls and every new position is between 0 and 39.

### Practice B: draw and click a button

Open a Pygame window. Draw a rectangle containing the word `ROLL`. When it is clicked, print `Button clicked`.

Learn:

- The Pygame game loop.
- Events.
- Rectangles.
- Mouse collision.

Success check: the window stays responsive and every click inside the button prints once.

### Practice C: create two player objects

Make a `Player` class with a name, cash, and position. Create two players and transfer 50 from one to the other.

Learn:

- Classes.
- Objects.
- Attributes.
- Methods.

Success check: no money disappears. One player loses exactly what the other player receives.

## 7. Milestone 1: open a real game window

### Goal

Create a reliable empty application before adding game rules.

### Files to create

- `main.py`
- `monopoly/__init__.py`
- `monopoly/app.py`
- `requirements.txt`

### Tasks

1. In `main.py`, import and start an `App` object.
2. In `app.py`, initialize Pygame and create a 1280 by 800 window.
3. Make a main loop with these three parts:
   - Read events.
   - Update the game.
   - Draw the screen.
4. Close the program when the window's close button is clicked.
5. Limit the game to 60 frames per second using `pygame.time.Clock`.
6. Fill the screen with one background colour.
7. Draw the title `Monopoly` in the middle.

### Manual test

- The window opens.
- It does not freeze.
- The title is visible.
- The close button exits cleanly.

### Checkpoint

Commit the working window. Do not build the board until this is stable.

## 8. Milestone 2: make a menu and switch screens

### Goal

Show a main menu and learn how one application can display different screens.

### Files to create

- `monopoly/screens.py`
- `monopoly/ui.py`

### Tasks

1. Create a reusable `Button` class in `ui.py`.
2. Give it a rectangle, label, normal colour, hover colour, and disabled state.
3. Give it `handle_event` and `draw` methods.
4. Create these screen names: `MENU`, `SETUP`, `GAME`, `HELP`, and `WINNER`.
5. Draw four menu buttons: New Game, Load Game, Rules, and Quit.
6. Make New Game switch to the setup screen.
7. Make Rules switch to a help screen.
8. Add Back buttons so the user can return to the menu.

### Manual test

Click every button several times. A button should only work when the mouse is inside it. No screen should trap the user.

### New idea: a state

A state is a value that says what the program is doing now. For example, when `screen == "MENU"`, draw the menu. This idea will later control turns and auctions too.

## 9. Milestone 3: create the game objects without graphics

### Goal

Represent a player, a board space, a property, and a game using Python objects.

### File to create

- `monopoly/models.py`

### Objects to add

#### Player

Store:

- A unique number.
- Name.
- Token colour or shape.
- Cash, starting at 1500.
- Board position, starting at 0.
- Property IDs owned.
- Whether they are in jail.
- Turns spent in jail.
- Number of Get Out of Jail Free cards.
- Whether they are bankrupt.

#### Space

Store:

- Number from 0 to 39.
- Name.
- Type such as `GO`, `STREET`, `RAILROAD`, `UTILITY`, `TAX`, or `CHANCE`.

#### Property

In addition to the space information, store:

- Purchase price.
- Owner ID or `None`.
- Mortgage value.
- Whether it is mortgaged.
- Colour group.
- Building price.
- Rent amounts.
- Number of buildings: 0-4 houses or 5 for a hotel.

#### GameState

Store:

- List of players.
- List of spaces.
- Current player number.
- Current turn phase.
- Dice values.
- Number of doubles rolled this turn.
- Houses and hotels left in the bank.
- Message history.
- Any decision that is waiting for the player.

### Keep data and code separate

The price of a property is data. The rule that charges rent is code. Put changing facts in JSON and behaviour in Python.

### Manual test

Write a temporary block that creates two players and prints their names and cash. Create one property, give it to a player, and print its owner. Remove the temporary block after it works.

## 10. Milestone 4: build the board data

### Goal

Describe all 40 spaces accurately without writing 40 giant Python statements.

### File to create

- `data/board.json`

### Tasks

1. Add all spaces in order from Go at index 0 to Boardwalk/Mayfair at index 39.
2. For a street, include its colour, price, house price, mortgage value, and six rent values:
   - No buildings.
   - One house.
   - Two houses.
   - Three houses.
   - Four houses.
   - Hotel.
3. Include railroad and utility prices and mortgage values.
4. Include tax amounts.
5. Write a `load_board()` function in `models.py`.
6. Check that every required key is present.
7. Check that the indexes are exactly 0 through 39.

### Automatic tests to add

- The board has exactly 40 spaces.
- No index is repeated.
- Every purchasable space has a positive price.
- Every street has exactly six rent numbers.
- Every street belongs to a valid colour group.

### Checkpoint

Print the 40 loaded names in order. If any are missing or out of order, fix the data before continuing.

## 11. Milestone 5: draw the board

### Goal

Turn the board data into a visible board.

### Tasks

1. Reserve a square area for the board and a side area for controls.
2. Draw the four corner spaces first.
3. Draw nine spaces between each pair of corners.
4. Write one function that converts a board index into a rectangle.
5. Draw each space's name.
6. Draw street colour strips.
7. Draw the centre of the board.
8. Draw simple player tokens as circles, squares, or triangles.
9. If players share a space, offset their tokens so all can be seen.

Do not use 40 separate drawing functions. Calculate where each space belongs from its index.

### Manual test

- All 40 spaces appear once.
- Go is in the correct corner.
- Space names are readable or shortened neatly.
- Resizing the window does not scramble the board.

### Optional polish

When the mouse rests over a property, show its full name, price, owner, rent, and mortgage state in the side panel.

## 12. Milestone 6: player setup and turn order

### Goal

Allow 2-6 people to begin a new game.

### Tasks

1. On the setup screen, choose the player count.
2. Add a text box for each player's name.
3. Let each player choose a different token colour or shape.
4. Reject blank or duplicate names.
5. Reject duplicate tokens.
6. Create all players with 1500 cash at Go.
7. Decide turn order with a dice roll, rerolling ties.
8. Show the final order before starting.

### Manual test

Try the minimum and maximum player counts. Try bad names and duplicate tokens. The game should explain what needs fixing instead of crashing.

## 13. Milestone 7: dice, movement, and turns

### Goal

Complete the smallest real game loop: roll, move, resolve, end turn.

### File to create

- `monopoly/rules.py`

### Turn phases

Use named values instead of many confusing booleans:

```text
TURN_START
WAITING_FOR_ROLL
MOVING
RESOLVING_SPACE
WAITING_FOR_DECISION
TURN_END
GAME_OVER
```

More phases will be added later.

### Tasks

1. Add a Roll Dice button that only works in `WAITING_FOR_ROLL`.
2. Generate two values from 1 through 6.
3. Move the token one space at a time.
4. Add 200 when a player passes Go.
5. Do not add 200 when a player is sent directly to jail.
6. If the dice match, allow another roll after resolving the space.
7. If a player rolls doubles three times in one turn, send them to jail.
8. Only enable End Turn when all required actions are complete.
9. Move to the next active player when the turn ends.
10. Write each important action into the message history.

### First tests to create

In `tests/test_movement.py`, check:

- A player at 0 who rolls 3 and 4 reaches 7.
- A player at 38 who moves 5 reaches 3 and receives 200.
- A direct trip to jail does not receive 200.
- Three consecutive doubles sends the player to jail.
- A bankrupt player never receives a turn.

### Helpful testing trick

Let the movement function accept dice numbers in tests. Random dice are fun for players but make tests unpredictable.

## 14. Milestone 8: landing on basic spaces

### Goal

Make every non-card space perform its basic action.

### Implement in this order

1. Go: record a message; salary was already handled while moving.
2. Free Parking: nothing happens under standard rules.
3. Visiting Jail: nothing happens.
4. Go To Jail: move directly to jail and end the turn.
5. Income Tax: pay the amount in the board data.
6. Luxury Tax: pay the amount in the board data.
7. Unowned property: offer it for sale.
8. Your own property: nothing happens.
9. Another player's property: pay rent.
10. Mortgaged property: no rent is charged.

### Money rule

Create one function for transferring money. It should record who paid, who received it, the amount, and why. Do not change cash from random UI functions.

### Manual test

Temporarily add a developer key that moves the current player to a chosen space. Use it to test every type of space quickly. Remove or hide this key in the release version.

## 15. Milestone 9: buying and auctioning properties

### Goal

Follow the real rule that an unwanted property is auctioned.

### Buying tasks

1. When a player lands on an unowned property, show Buy and Auction buttons.
2. Disable Buy if the player cannot afford it.
3. Buying removes cash and changes the owner.
4. Declining starts an auction.
5. If the player cannot afford the listed price, start an auction automatically.

### Auction tasks

1. Show the property being auctioned.
2. Let every active player bid, including the player who declined to buy.
3. Keep the current bid and current leader.
4. A bid must be higher than the current bid and affordable.
5. A player may pass and leave that auction.
6. Continue until only the highest bidder remains.
7. The winner pays the bank and receives the property.
8. If everyone passes before any bid, the property stays with the bank.

### Tests

- A purchase changes cash and ownership correctly.
- A player cannot buy an owned property.
- An unaffordable bid is rejected.
- An auction finishes with one winner.
- Ownership does not change if nobody bids.

## 16. Milestone 10: calculate rent correctly

### Goal

Handle street, railroad, and utility rent.

### Street rent

- Use the rent number matching the building count.
- If the owner has every street in the colour group and there are no buildings, double the base rent.
- Do not double rent on a mortgaged street.

### Railroad rent

Rent depends on how many railroads the owner has: 1, 2, 3, or 4.

### Utility rent

- One utility: dice total multiplied by 4.
- Both utilities: dice total multiplied by 10.
- Some cards use a special dice roll and multiplier; add that during the card milestone.

### Tests

Create a test for every rent row and every ownership count. Also test that a mortgaged property charges zero.

## 17. Milestone 11: jail

### Goal

Support every normal way to enter and leave jail.

### Entering jail

A player enters jail by:

- Landing on Go To Jail.
- Drawing a Go To Jail card.
- Rolling doubles three times in one turn.

Set the position to the jail space, mark the player as jailed, reset doubles, and end the turn.

### Starting a jail turn

Offer these legal choices:

- Pay 50 and leave jail before rolling.
- Use a Get Out of Jail Free card and leave before rolling.
- Try to roll doubles.

### Jail roll rules

- Doubles release the player and move them, but do not give an extra roll.
- A failed first or second attempt ends the turn.
- After a failed third attempt, the player must pay 50 and move by that roll.
- If payment cannot be made immediately, enter the debt process described later.

### Tests

Write a test for every choice, including the third failed roll and doubles on each jail turn.

## 18. Milestone 12: Chance and Community Chest

### Goal

Create shuffled decks and implement every card.

### Files to create

- `data/chance.json`
- `data/community_chest.json`
- `monopoly/cards.py`

### Card action types

Use action names plus values instead of putting Python code in JSON:

- Receive money from bank.
- Pay money to bank.
- Receive money from every player.
- Pay money to every player.
- Move to an exact space.
- Move forward to the nearest railroad or utility.
- Move backward a number of spaces.
- Go directly to jail.
- Pay for repairs based on houses and hotels.
- Keep a Get Out of Jail Free card.

### Deck tasks

1. Shuffle each deck at the beginning.
2. Draw from the top.
3. Put used cards at the bottom or in a discard pile.
4. Keep a jail card outside the deck while a player owns it.
5. Return the jail card when it is used or returned during bankruptcy.
6. If a movement card lands on another active space, resolve that space too.

### Tests

Test every individual card with a prepared game state. Do not rely only on drawing random cards during play.

## 19. Milestone 13: property management

### Goal

Let owners build, sell, mortgage, and unmortgage without breaking the rules.

### Asset manager screen

Show:

- All properties owned by the current player.
- Colour groups.
- Current rent and building count.
- Mortgage status.
- The exact cost or money received before an action is confirmed.
- A reason when an action is disabled.

### Building rules

- The player must own the complete colour group.
- No property in the group may be mortgaged.
- Build evenly: one property cannot get too far ahead of the others.
- Sell evenly too.
- Houses cost the amount listed for the group.
- Selling a building returns half its purchase cost.
- The bank begins with 32 houses and 12 hotels.
- A hotel can replace four houses only when every property in the group has four houses.
- Selling a hotel normally requires four houses to be available from the bank.

### Mortgage rules

- A property with buildings cannot be mortgaged.
- No property in its colour group may have buildings.
- Mortgaging pays the printed mortgage value.
- Mortgaged property charges no rent.
- Unmortgaging costs the mortgage amount plus 10 percent interest.

### Shortage rule

If several players want the last available houses or hotels, the bank auctions the buildings. Implement this after ordinary building works correctly.

### Tests

- Reject building without a complete colour group.
- Reject uneven building and selling.
- Keep the total number of houses at 32.
- Keep the total number of hotels at 12.
- Reject mortgaging an improved group.
- Charge the correct unmortgage price.

## 20. Milestone 14: trading

### Goal

Allow two active players to exchange assets safely.

### A trade can contain

- Cash.
- Unimproved properties.
- Get Out of Jail Free cards.

### Tasks

1. Choose another active player.
2. Build both sides of the offer.
3. Show a clear summary.
4. Let the other player accept, reject, or change the offer.
5. Validate everything again when Accept is clicked.
6. Move all parts of an accepted trade together.
7. Explain the interest rule when a mortgaged property changes owner.

Properties in a colour group with buildings cannot be traded until all buildings in that group are sold.

### Important coding idea: all or nothing

Do not transfer half a trade and then discover the other half is illegal. Validate first, then apply every change.

## 21. Milestone 15: debt and bankruptcy

### Goal

Prevent negative cash and give players a chance to raise money.

### Pending payment

When a player owes more cash than they have:

1. Store who must pay.
2. Store who should receive the money: a player or the bank.
3. Store the full amount and reason.
4. Pause normal turn actions.
5. Allow the debtor to sell buildings, mortgage properties, and make legal trades.
6. Add a Pay button when enough money has been raised.
7. Add a Declare Bankruptcy button.

### Bankruptcy to another player

- Transfer remaining cash, properties, and jail cards to the creditor.
- Explain and charge mortgage interest according to the chosen standard rules.
- Remove the bankrupt player from future turns.

### Bankruptcy to the bank

- Return buildings to the bank.
- Return jail cards to their decks.
- Reset properties and auction them one at a time.
- Remove the bankrupt player from future turns.

### Winning

When only one active player remains, change to `GAME_OVER` and show the winner screen.

### Tests

- A player can raise funds and finish a payment.
- Assets go to the correct creditor.
- Bankrupt players never act again.
- Bankruptcy to the bank creates the required auctions.
- The game finds exactly one winner.

## 22. Milestone 16: save and load

### Goal

Save a match at any important decision and continue it later.

### File to create

- `monopoly/persistence.py`

### What to save

- A save format version number.
- Every player and property.
- Current player and phase.
- Dice and doubles information.
- Jail information.
- Bank house and hotel supply.
- Deck order and held jail cards.
- Pending auctions, trades, and payments.
- Game settings and recent history.

### Rules

- Save plain information such as numbers, strings, lists, and dictionaries.
- Do not save Pygame fonts, images, rectangles, or functions.
- Validate a file before loading it.
- Show a friendly message for a broken or incompatible save.
- Autosave after each fully completed turn.

### Tests

1. Create a known game state.
2. Save it.
3. Load it.
4. Compare every important value.
5. Continue playing and make sure the same actions are legal.

Also test saving during an auction, jail choice, and unpaid debt.

## 23. Milestone 17: make it friendly to use

Only begin this milestone when the rules work.

Add:

- A visible message explaining what the current player must do.
- Disabled buttons for illegal actions.
- Helpful explanations when an action is disabled.
- Confirmation before bankruptcy, restart, or quitting an unsaved game.
- A scrollable action history.
- A pause menu.
- A rules/help screen.
- Keyboard controls as well as mouse controls.
- Large readable text and strong colour contrast.
- Symbols or patterns so colour is not the only clue.
- Short token and dice animations.
- A setting to make animations faster or skip them.
- Optional sound and a mute button.

Do not let an animation decide a rule. The rules engine decides what happened; the animation only shows it.

## 24. A sensible weekly schedule

This is only a guide. Taking longer is completely fine.

### Week 1

- Complete the three practice programs.
- Create the app window.
- Create buttons and screen switching.

### Week 2

- Create the model classes.
- Enter and validate all board data.
- Draw the board.

### Week 3

- Build player setup.
- Add dice, movement, turns, doubles, and passing Go.
- Begin movement tests.

### Week 4

- Resolve basic spaces.
- Buy properties.
- Build the property auction.

### Week 5

- Add all rent calculations.
- Add all jail rules.
- Expand automatic tests.

### Week 6

- Add Chance and Community Chest.
- Test every card.

### Week 7

- Add buildings, hotels, shortages, and mortgages.
- Create the asset manager.

### Week 8

- Add trading.
- Add debt and bankruptcy.
- Finish winner detection.

### Week 9

- Add save and load.
- Add help, history, keyboard controls, and confirmations.

### Week 10

- Play complete games.
- Fix problems.
- Improve the look only after the game is reliable.

## 25. How to debug without feeling lost

When something goes wrong:

1. Read the final line of the error first.
2. Find the first line mentioning one of your files.
3. Print or inspect the values used on that line.
4. Ask what you expected and what actually happened.
5. Make a tiny test that repeats the problem.
6. Fix one cause at a time.
7. Run all earlier tests after the fix.

Useful temporary information to display:

- Current phase.
- Current player.
- Dice values.
- Player position before and after movement.
- Pending payment or decision.
- Legal actions right now.

Remove noisy debug printing when the problem is fixed, or put it behind a `DEBUG` setting.

## 26. Git checkpoints

Make a commit whenever one small piece works. Example commit messages:

```text
Create Pygame window and clean exit
Add reusable menu buttons
Load and validate 40 board spaces
Draw board spaces from data
Implement passing Go
Add property purchase and auction
Implement jail choices
Add building rules and tests
Save and load complete game state
```

Avoid a commit called `finished everything`. Small commits make mistakes easier to find and undo.

## 27. Tests to run before calling the game complete

### Starting and turns

- Start games with 2 and 6 players.
- Roll ordinary numbers and doubles.
- Roll three doubles.
- Pass Go by dice and by card.
- Skip bankrupt players.

### Properties

- Buy and decline every kind of property.
- Finish auctions with many bidders and no bidders.
- Charge every street rent level.
- Charge railroad and utility rent.
- Land on mortgaged properties.

### Buildings and mortgages

- Build and sell evenly.
- Upgrade to and sell a hotel.
- Run out of houses and hotels.
- Auction scarce buildings.
- Mortgage and unmortgage legal properties.
- Try every illegal action and check it is rejected.

### Cards and jail

- Use every Chance and Community Chest card.
- Hold, trade, use, and return jail cards.
- Enter jail in all three ways.
- Leave jail in every allowed way.

### Money and game ending

- Pay the bank and other players.
- Raise money while in debt.
- Go bankrupt to another player.
- Go bankrupt to the bank.
- Reach one winner.

### Saving

- Save and load during normal turns.
- Save during an auction, jail decision, and debt.
- Try to load a broken file.

## 28. Final release checklist

The project is ready when:

- A new player can understand what to click without help from the programmer.
- A full game can finish without using the terminal.
- All standard spaces, cards, and property types work.
- Illegal moves are blocked with useful explanations.
- Save and load preserve the exact game state.
- Automated tests pass.
- Several complete games have been played without getting stuck.
- `README.md` explains installation, controls, and rules choices.

## 29. Features to save for later

These ideas are fun, but they should not delay the first complete version:

- Computer-controlled players.
- Online multiplayer.
- Fancy art and 3D dice.
- Custom board editor.
- Different board themes.
- Achievements.
- Player statistics.
- Optional house rules such as a Free Parking jackpot.

Add these only after the standard local game works from beginning to winner.

## 30. Your first task

Do only this first:

1. Install the tools from section 4.
2. Complete Practice A, B, and C.
3. Create the window from Milestone 1.
4. Stop and make sure it closes cleanly.
5. Commit that working version.

That may look like a tiny start, but it creates the foundation for everything else in the game.
