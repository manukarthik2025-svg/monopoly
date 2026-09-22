# Pygame Monopoly — Implementation Plan

## 1. Project goal

Build a local, turn-based Monopoly-style board game in Python with Pygame. The presentation should stay intentionally simple (clean shapes, text, and lightweight effects), while the gameplay should include the complete standard rules needed to finish a real game.

The first release will support 2–6 human players sharing one computer. The design should keep player decisions and game rules separate so computer players, networking, alternate boards, and house rules can be added later without rewriting the core.

## 2. Definition of done

The game is complete when players can start a new match, play from the initial setup through bankruptcy, and reach a single winner without using the terminal or editing save data.

The finished game must support:

- Player setup, token selection, turn order, and starting cash.
- Dice rolling, doubles, three consecutive doubles, movement, passing/landing on Go, and extra turns.
- Purchasable streets, railroads, and utilities.
- Auctions when a player declines or cannot buy an unowned property.
- Correct rent for streets, monopolies, houses/hotels, railroads, and utilities.
- Property sets, even building, selling buildings, the house/hotel supply, and the building shortage auction rule.
- Mortgaging/unmortgaging, including interest and restrictions around improved colour groups.
- Trading cash, properties, and Get Out of Jail Free cards between players.
- Chance and Community Chest decks with shuffled draw piles, discard behaviour, movement cards, repairs, payments, collections, and retained jail cards.
- Income Tax, Luxury Tax, Free Parking, Go, visiting Jail, and Go To Jail spaces.
- Jail entry, jail turns, doubles release, card release, and bail.
- Payments between players and the bank, including raising funds before bankruptcy.
- Bankruptcy to another player or to the bank, asset transfer/auction handling, and player elimination.
- Save, load, pause, restart, and return-to-menu flows.
- Clear prompts, legal-action enforcement, action history, rules/help screen, and winner screen.

By default, Free Parking does not award a jackpot and landing on Go does not pay extra. Optional house rules can be introduced only after the standard rules are stable.

## 3. Technical direction

### Runtime and dependencies

- Python 3.12+.
- Pygame 2.x.
- `pytest` for rule-engine tests.
- JSON for save files and board/card data.
- No required external art or font assets for the first release; use Pygame primitives and bundled/system fonts.

### Design principles

- Keep the rules engine independent of Pygame so most behaviour can be unit-tested without opening a window.
- Represent every multi-step interaction as an explicit game phase/state, never as a blocking input loop.
- Make board spaces and cards data-driven rather than hard-coded into rendering or input code.
- Centralize all money and asset transfers to prevent inconsistent bankruptcy behaviour.
- Derive legal UI actions from the current state; disabled or illegal actions must never mutate the game.
- Use seeded randomness in tests and optional seed capture in saves for reproducibility.

## 4. Proposed repository layout

```text
monopoly/
├── main.py
├── requirements.txt
├── README.md
├── PLAN.md
├── assets/
│   ├── fonts/
│   ├── icons/
│   └── sounds/
├── data/
│   ├── board.json
│   ├── chance.json
│   └── community_chest.json
├── monopoly/
│   ├── __init__.py
│   ├── app.py
│   ├── constants.py
│   ├── models.py
│   ├── board.py
│   ├── rules.py
│   ├── actions.py
│   ├── cards.py
│   ├── persistence.py
│   ├── scenes/
│   │   ├── base.py
│   │   ├── menu.py
│   │   ├── setup.py
│   │   ├── game.py
│   │   ├── help.py
│   │   └── winner.py
│   └── ui/
│       ├── widgets.py
│       ├── board_view.py
│       ├── panels.py
│       └── dialogs.py
├── saves/
└── tests/
    ├── test_movement.py
    ├── test_rent.py
    ├── test_building.py
    ├── test_cards.py
    ├── test_jail.py
    ├── test_trades.py
    ├── test_auctions.py
    ├── test_mortgages.py
    ├── test_bankruptcy.py
    └── test_persistence.py
```

Generated save files should be ignored by version control, except for deliberate test fixtures.

## 5. Core model

Use dataclasses and enums for state that must be serialized cleanly.

### Main entities

- `GameState`: players, current player index, board, decks, bank inventory, phase, pending decision/payment, turn counters, winner, history, and settings.
- `Player`: id, name, token, cash, position, jail state, owned asset IDs, held jail cards, active/bankrupt status.
- `Space`: id, index, name, type, display colour, and type-specific configuration.
- `Property`: price, mortgage value, group, house cost, rent schedule, owner, mortgage state, and building count (`0–4`, `5` for hotel).
- `Railroad` and `Utility`: ownership and rent configuration.
- `Card`: deck, text, action type, parameters, and whether it can be retained.
- `Bank`: available houses (32), hotels (12), and ownership of unpurchased assets.
- `TradeOffer`: participants and each side's cash, assets, and cards.
- `PendingPayment`: debtor, creditor or bank, amount, reason, and resolution state.
- `AuctionState`: asset, eligible bidders, current bid, leader, and passed players.

### Game phases

At minimum:

```text
TURN_START
AWAITING_ROLL
MOVING
RESOLVING_SPACE
AWAITING_PURCHASE
AUCTION
AWAITING_CARD
IN_JAIL_DECISION
MANAGING_ASSETS
TRADING
PAYMENT_REQUIRED
TURN_END
GAME_OVER
```

Temporary overlays such as property details, pause, help, and confirmations belong to the UI layer and should not corrupt the core phase.

## 6. Rules engine responsibilities

The rules layer exposes commands such as `roll_dice`, `buy_property`, `start_auction`, `place_bid`, `build`, `sell_building`, `mortgage`, `unmortgage`, `propose_trade`, `accept_trade`, `pay_bail`, `use_jail_card`, and `end_turn`.

Each command should:

1. Validate that the command is legal in the current phase.
2. Apply one atomic state change or create a clearly defined pending decision.
3. Append a human-readable event to the game history.
4. Return structured events for animation, sound, and dialogs.

### Important rule details

- Salary is awarded whenever forward movement passes Go, including applicable card movement; direct movement to Jail does not collect it.
- Rolling doubles grants another turn unless the player is sent to Jail. Three doubles in the same turn sends the player directly to Jail.
- A player may not voluntarily end a turn while a required purchase/auction, card, payment, or other mandatory decision is unresolved.
- Owning an unimproved complete colour group doubles base street rent. A mortgaged property never charges rent.
- Buildings must be bought and sold evenly across a colour group. A hotel requires four houses on every property in the group and returns four houses from that property to the bank.
- No property in a colour group may be mortgaged while any property in that group has buildings.
- Unmortgaging costs mortgage value plus 10% interest, rounded according to the board data/rules setting.
- Trades containing improved properties are illegal; players must sell the group's buildings first. Mortgaged-property interest obligations must be presented and resolved correctly for the receiver.
- If a player owes more cash than they hold, enter `PAYMENT_REQUIRED` and allow legal asset management/trading before bankruptcy is declared.
- The bank has unlimited cash but limited houses and hotels. If multiple players want the last available buildings, resolve them by auction.
- Bankruptcy transfers assets to the creditor when the creditor is a player; bankruptcy to the bank returns buildings and auctions properties individually. Retained jail cards return to their decks when appropriate.
- Deck cards cycle through shuffled draw/discard piles; a retained jail card remains outside the deck until used, traded, or returned.

Write ambiguous or edition-dependent choices in one documented rules configuration module, then test those choices explicitly.

## 7. UI and interaction plan

### Window layout

- Default resolution: 1280×800, resizable with a minimum supported size.
- Square board on the left or centred.
- Right-side panel for current player, cash, dice, phase prompt, and context-sensitive action buttons.
- Bottom/scrollable event log for recent actions.
- Modal dialogs for auctions, trades, property management, cards, confirmations, and mandatory payments.

### Board presentation

- Draw the board with rectangles, colour bands, labels, prices, and simple icons.
- Scale all geometry from a single board rectangle so resizing stays consistent.
- Show player tokens as coloured shapes, offset when multiple tokens share a space.
- Display ownership markers, mortgage markers, and house/hotel shapes directly on spaces.
- Animate dice and token movement briefly, while offering a fast-animation setting.
- Highlight the current player and selectable/legal targets.

### Essential screens

- Main menu: New Game, Load Game, Rules, Quit.
- Setup: 2–6 player names/tokens and optional rule settings.
- Game: board, player panel, actions, event history, pause menu.
- Asset manager: filter by colour group; build, sell, mortgage, and unmortgage with before/after costs.
- Auction dialog: current bid, minimum bid, bidder controls, pass action, and winner.
- Trade dialog: two-sided offer builder with validation and accept/reject/counter flow.
- Help/rules: controls and concise explanations of major rules.
- Game over: winner, standings, and new game/menu choices.

Keyboard and mouse should both work for common actions. Provide visible hover/focus/disabled states and avoid relying on colour alone to convey ownership or status.

## 8. Persistence

- Save a versioned JSON snapshot containing all authoritative state, including deck order, retained cards, phase, unresolved decisions, settings, and history.
- Do not serialize Pygame objects, callbacks, surfaces, or fonts.
- Validate version and required fields before loading; show an in-game error rather than crashing on malformed files.
- Use an atomic save pattern: write a temporary file, validate it, then replace the target save.
- Support at least one manual save and an autosave at the end of each completed turn.
- A loaded game must produce the same legal actions and future deck order as the saved game.

## 9. Milestones

### Milestone 1 — Skeleton and testable domain

- Create package structure, dependency files, app loop, scene manager, and placeholder menu/game screens.
- Define enums/dataclasses and load/validate board data.
- Add a headless test setup and continuous test command.

Exit criterion: the app opens and closes cleanly, and tests can construct a valid new game without Pygame display dependencies.

### Milestone 2 — Basic playable loop

- Add setup for 2–6 players.
- Render the complete board and tokens.
- Implement dice, turns, movement, Go salary, doubles, taxes, Go To Jail, and basic Jail behaviour.
- Add buying and basic rent for all purchasable spaces.

Exit criterion: players can circulate the board, buy assets, pay rent/tax, visit Jail, and advance turns without invalid states.

### Milestone 3 — Cards and auctions

- Implement both shuffled decks and every card action.
- Add property auctions, bidder rotation, pass/re-entry rules as configured, and zero-cash edge cases.
- Add clear modal flows and event messages.

Exit criterion: declining any purchase always reaches a completed auction, and every card has a focused automated test.

### Milestone 4 — Full asset economy

- Implement monopolies, rent schedules, even building/selling, hotels, bank inventory, and building auctions.
- Implement mortgage/unmortgage rules.
- Build the asset-management UI with legal-action previews.

Exit criterion: all property economics and inventory rules pass unit tests, including shortages and mortgages.

### Milestone 5 — Trading, debt, and bankruptcy

- Implement validated trades with cash, assets, and jail cards.
- Add mandatory-payment mode and fund-raising flow.
- Implement bankruptcy to players and the bank, auctions, elimination, and victory detection.

Exit criterion: scripted integration games can eliminate players and end with exactly one winner while preserving total assets and card inventory.

### Milestone 6 — Save/load and usability

- Add versioned manual saves, autosaves, load menu, and corrupt-save handling.
- Add pause, restart, help, settings, action history, keyboard navigation, and confirmations.
- Add lightweight animation and optional sound with mute controls.

Exit criterion: saves can be reloaded at every interactive phase and continue identically.

### Milestone 7 — Hardening and release

- Run long simulated/scripted games to find deadlocks and illegal transitions.
- Test window resizing, small supported resolution, text overflow, and overlapping tokens.
- Profile redraws, cache static board surfaces, and remove avoidable per-frame allocations.
- Package clear run instructions and optionally produce a desktop executable with PyInstaller.

Exit criterion: a complete game can be played through repeatedly without crashes, stuck dialogs, or manual intervention.

## 10. Testing strategy

### Unit tests

- Movement wraparound, salary, card movement, and direct-to-Jail movement.
- Doubles and three-doubles handling.
- Every rent formula and ownership/mortgage combination.
- Even build/sell restrictions and house/hotel inventory conservation.
- Mortgage and unmortgage legality/cost.
- Every Chance and Community Chest card.
- Jail choices across all allowed jail turns.
- Auction bidding/pass termination and building shortage auctions.
- Trade validation, execution, and mortgaged asset handling.
- Debt resolution and each bankruptcy destination.
- JSON round trips and load validation.

### Invariants checked after every command in debug/tests

- Each asset has at most one owner and appears in the matching owner's inventory.
- Cash values and bank transactions use integers.
- Total houses and hotels (bank plus board) remain 32 and 12.
- Each retained jail card is held by at most one player and absent from its draw/discard piles.
- Current player is active unless the game is over.
- Buildings obey group ownership and even-building rules.
- The current phase has exactly the pending state it requires.
- No eliminated player can bid, trade, roll, or receive a turn.

### Integration scenarios

- Purchase declined → auction → winner pays and receives title.
- Card movement → pass Go → land on owned property → rent payment.
- Insufficient rent → sell buildings/mortgage → complete payment.
- Insufficient rent → bankruptcy to player → assets and cards transfer.
- Tax debt → bankruptcy to bank → properties auctioned.
- Hotel sale when the bank lacks enough houses to break it down.
- Save during auction/trade/payment/jail decision → load → finish the decision.
- Final opponent bankrupts → game transitions to winner screen.

## 11. Risks and safeguards

- **Rule complexity:** keep one authoritative command API and add tests before UI wiring for each rule family.
- **UI deadlocks:** every phase defines its valid commands and at least one valid path forward; add integration tests for modal phases.
- **Payment edge cases:** route all charges through `PendingPayment`, never subtract cash directly from UI code.
- **Save incompatibility:** include `save_version` and explicit migrations or a friendly incompatibility message.
- **Board readability:** use responsive geometry, abbreviated board labels, tooltips/detail panels, and a minimum resolution.
- **Copyright/trademark concerns for distribution:** keep board/card text and visual assets replaceable through data files; use original graphics and naming if publishing beyond a private learning project.

## 12. Initial implementation order

Start with the domain model, board/card data schemas, and tests. Once a full turn can run headlessly, connect it to a minimal board renderer and context-sensitive controls. Complete one rules milestone at a time, including tests and UI, rather than building all screens before the rules engine is trustworthy.

The first coding slice should be:

1. Add `requirements.txt`, package folders, and a small Pygame app/scene loop.
2. Define `GameState`, `Player`, `Space`, `Property`, and phase/action enums.
3. Add and validate the 40-space board data.
4. Implement new-game creation, dice injection, movement, Go salary, and turn advancement.
5. Unit-test those rules headlessly.
6. Render the board, players, Roll button, End Turn button, and action log.

