# Quest 11 · Roll and move

**Goal:** the rules for rolling, moving, passing Go and ending a turn, all proven by tests.
**Changed:** `logic/game.py`, `ui/play_screen.py` **New:** `tests/helpers.py`, `tests/test_moving.py`, `tests/test_money.py`

## Idea: phases

At any moment the game is waiting for **one** thing. We store what it is in `game.phase`:

```text
ROLL      waiting for the player to roll
MOVING    busy moving (never waits here)
END_TURN  waiting for the player to click End turn
```

Every rule starts by checking the phase. If it's the wrong moment, it does nothing:

```python
if self.phase != ROLL:
    return
```

This is what stops you rolling twice, or ending your turn before you've rolled. More phases get added later (`JAIL`, `BUY`, `AUCTION`...).

## Idea: tests choose the dice

Real dice are random, and you can't test random. So `Game` takes the dice **function** as an argument. The real game uses `roll_dice`. Tests pass in fake dice that roll exactly what the test wants.

## Idea: one door for money

**All** money moves through `transfer()`. If money ever goes missing, there's only one place to look. `BANK` stands in for the bank, which has endless money.

## Do it

1. Replace `logic/game.py` with this version:

```python
import random

from logic.board import load_board

BANK = "BANK"
GO_MONEY = 200

# Phases: what the game is waiting for right now.
ROLL = "ROLL"              # current player should roll the dice
MOVING = "MOVING"          # the rules are busy moving someone (never waits here)
END_TURN = "END_TURN"      # nothing left to do: click End Turn


def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)


def name_of(who):
    if who == BANK:
        return "the bank"
    return who.name


class Game:
    """Everything about one game of Monopoly, and every rule for changing it."""

    def __init__(self, players, dice=roll_dice):
        self.players = players
        self.board = load_board()
        self.roll_dice = dice        # tests swap this for dice that roll what they want
        self.turn = 0                # index into self.players
        self.phase = ROLL
        self.dice = (0, 0)
        self.log = []
        self.say(f"{self.current_player().name} goes first!")

    # ---------- who and what ----------

    def current_player(self):
        return self.players[self.turn]

    def active_players(self):
        return [player for player in self.players if not player.bankrupt]

    def say(self, message):
        self.log.append(message)

    # ---------- money ----------

    def transfer(self, payer, receiver, amount, reason):
        """The ONLY place money moves. payer and receiver are Players or BANK."""
        if amount <= 0:
            return
        if payer != BANK:
            payer.cash -= amount
        if receiver != BANK:
            receiver.cash += amount
        self.say(f"{name_of(payer)} paid ${amount} to {name_of(receiver)} for {reason}")

    # ---------- a normal turn ----------

    def start_turn(self):
        player = self.current_player()
        self.say(f"--- {player.name}'s turn ---")
        self.phase = ROLL

    def roll(self):
        if self.phase != ROLL:
            return
        player = self.current_player()
        self.dice = self.roll_dice()
        die1, die2 = self.dice
        self.say(f"{player.name} rolled {die1} and {die2}")

        self.phase = MOVING
        self.move_forward(player, die1 + die2)
        self.land(player)
        if self.phase == MOVING:      # (later, landing can stop and ask a question)
            self.finish_move()

    def finish_move(self):
        """This roll is completely sorted out. What happens next?"""
        self.phase = END_TURN

    def end_turn(self):
        if self.phase != END_TURN:
            return
        self.turn = (self.turn + 1) % len(self.players)
        # TODO: while the current player is bankrupt, move self.turn on again
        self.start_turn()

    # ---------- moving ----------

    def move_forward(self, player, steps):
        player.position += steps
        # TODO: if position is 40 or more: take 40 off, and transfer GO_MONEY from the BANK
        #       to the player "for passing Go"

    def land(self, player):
        """Do whatever the space you just landed on says."""
        space = self.board[player.position]
        self.say(f"{player.name} landed on {space.name}")
```

2. Create `tests/helpers.py`. Every test file will use this:

```python
from logic.game import Game
from logic.player import Player


def make_game(*rolls, players=2):
    """A game where the dice roll exactly what you list, in order.

    make_game((3, 4), (6, 6)) -> the first roll is 3+4, the second is 6+6.
    """
    rolls = list(rolls)
    names = ["Ann", "Ben", "Cat", "Dan", "Eve", "Fin"][:players]
    return Game([Player(name) for name in names], dice=lambda: rolls.pop(0))
```

> `*rolls` collects any number of arguments into one tuple. `lambda: rolls.pop(0)` is a tiny nameless function: each time the game "rolls", it takes the next pair off the front of the list.

3. Create `tests/test_moving.py`:

```python
from helpers import make_game

from logic.game import END_TURN


def test_rolling_moves_you():
    game = make_game((2, 3))
    game.roll()
    assert game.players[0].position == 5


def test_passing_go_pays_200():
    game = make_game((1, 2))
    ann = game.players[0]
    ann.position = 38
    game.roll()
    assert ann.position == 1
    assert ann.cash == 1700


def test_no_doubles_means_end_turn():
    game = make_game((4, 6))            # lands on Jail, just visiting
    game.roll()
    assert game.phase == END_TURN


def test_end_turn_goes_to_next_player():
    game = make_game((4, 6), players=3)
    game.roll()
    game.end_turn()
    assert game.current_player().name == "Ben"


def test_end_turn_skips_bankrupt_players():
    game = make_game((4, 6), players=3)
    game.players[1].bankrupt = True
    game.roll()
    game.end_turn()
    assert game.current_player().name == "Cat"


def test_you_cant_roll_twice_without_doubles():
    game = make_game((4, 6), (3, 4))
    game.roll()
    game.roll()
    assert game.players[0].position == 10
```

4. Create `tests/test_money.py`:

```python
from helpers import make_game

from logic.game import BANK


def test_transfer_between_players():
    game = make_game()
    ann, ben = game.players
    game.transfer(ann, ben, 100, "a test")
    assert ann.cash == 1400
    assert ben.cash == 1600


def test_the_bank_has_endless_money():
    pass    # TODO: transfer 200 from BANK to Ann, and check she has 1700
```

5. Quick way to try it before there are buttons: in `PlayScreen.handle_event` (in `ui/play_screen.py`) add two temporary keys. **R** rolls, **E** ends the turn:

```python
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.game.roll()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.game.end_turn()
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] In the game, R moves the pulsing token, then E passes the turn to the next player
- [ ] Pressing R twice in a row only moves once

## Save

Commit message: `Quest 11: rolling, moving and passing Go`
