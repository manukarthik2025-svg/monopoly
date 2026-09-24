# Monopoly Quests

This is your path to building a full working Monopoly game in Python, from an empty folder to a finished, playable game. It's split into small quests — each one is a single sitting, each one leaves you with something that actually runs.

The full technical rules reference lives in [`../PLAN.md`](../PLAN.md). You don't need to read it to start — check it later if you ever want the exact detail behind a rule (like the precise railroad rent formula, or what counts as a legal trade).

## How to use this

- Do the quests **in order**. Later ones assume the classes and functions from earlier ones already exist, under the same names.
- Read the whole quest before writing code. Each one tells you *why* you're doing it, not just *what* to type.
- Get the "Test it yourself" section passing before moving on. If something's broken, the next quest will be harder to debug, not easier.
- **Commit to git after every quest**, using the suggested commit message. This means if you break something three quests from now, you can always look back at — or go back to — a version that worked. Small commits make mistakes easy to find and undo.
- It's completely normal for code to not work on the first try. An error message is a clue, not a failure. Read the last line of the error first.
- Some quests have a "New idea(s)" section introducing a concept you haven't used yet, with a tiny unrelated example. Read that part slowly — it'll come up again and again after this.

## Quest checklist

### Chapter 0: Get your tools ready
- [ ] [00. Get your tools ready](00_setup.md)

### Chapter 1: Warm-up practice
- [ ] [01. Move around a board (practice)](01_practice_moving_board.md)
- [ ] [02. Draw and click a button (practice)](02_practice_button_click.md)
- [ ] [03. Create two player objects (practice)](03_practice_player_objects.md)

### Chapter 2: A real window
- [ ] [04. Open a real game window](04_real_window.md)
- [ ] [05. Build a reusable Button class](05_reusable_button.md)
- [ ] [06. Menu and screen switching](06_screen_switching.md)

### Chapter 3: Game objects
- [ ] [07. A real Player class](07_player_class.md)
- [ ] [08. A Space class for the whole board](08_space_and_property_classes.md)
- [ ] [09. The GameState class](09_gamestate_class.md)

### Chapter 4: The board
- [ ] [10. Describe the board in JSON](10_board_data_json.md)
- [ ] [11. Load and check the board data](11_load_and_validate_board.md)
- [ ] [12. Turn a space index into screen coordinates](12_board_math.md)
- [ ] [13. Draw the actual board](13_draw_the_board.md)

### Chapter 5: Playing a turn
- [ ] [14. Player setup screen](14_player_setup_screen.md)
- [ ] [15. Decide turn order](15_turn_order.md)
- [ ] [16. A Roll Dice button that actually rolls](16_roll_dice_button.md)
- [ ] [17. Move the token and pass Go](17_movement_and_passing_go.md)
- [ ] [18. Doubles give another turn (mostly)](18_doubles_and_jail_streak.md)
- [ ] [19. End Turn and advance to the next player](19_ending_a_turn.md)

### Chapter 6: Landing on spaces
- [ ] [20. One function for all money movement](20_pay_and_transfer_money.md)
- [ ] [21. React to every space type](21_landing_on_spaces.md)
- [ ] [22. Buy or decline a property](22_buying_property.md)

### Chapter 7: Rent and auctions
- [ ] [23. Auction a declined property](23_auctions.md)
- [ ] [24. Real rent — streets, railroads, utilities](24_rent_calculations.md)

### Chapter 8: Jail
- [ ] [25. All three ways into jail](25_entering_jail.md)
- [ ] [26. Getting out of jail](26_jail_turn_choices.md)

### Chapter 9: Cards
- [ ] [27. Shuffled Chance and Community Chest decks](27_card_decks.md)
- [ ] [28. Make every card actually do something](28_card_actions.md)

### Chapter 10: Buildings and mortgages
- [ ] [29. An asset manager screen](29_asset_manager_screen.md)
- [ ] [30. Houses, hotels, and even building](30_building_rules.md)
- [ ] [31. Mortgage and unmortgage](31_mortgages.md)

### Chapter 11: Trading and bankruptcy
- [ ] [32. Trading between players](32_trading.md)
- [ ] [33. Owing more than you have](33_debt_and_raising_funds.md)
- [ ] [34. Bankruptcy and finding a winner](34_bankruptcy_and_winning.md)

### Chapter 12: Save/load and polish
- [ ] [35. Save and load a game](35_save_and_load.md)
- [ ] [36. Make it pleasant to actually play](36_polish_and_juice.md)

That's it — 37 quests, each one a real step toward a real game. Start with [00](00_setup.md).
