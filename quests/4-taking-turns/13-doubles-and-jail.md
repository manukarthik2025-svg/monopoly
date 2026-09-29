# Quest 13 · Doubles and jail

**Goal:** doubles give you another roll, three doubles in a row send you to jail, and jail has its own rules for getting out.
**Changed:** `logic/game.py`, `ui/sidebar.py`, `ui/play_screen.py`, `ui/board_view.py`, tests

## The rules

- Roll doubles and you roll again. The **third** double in a row sends you straight to jail.
- Land on **Go To Jail** and you go straight to jail. You don't pass Go, so no $200.
- On your turn in jail, choose one:
  - **Pay $50**, then roll and move normally
  - **Try for doubles**: if you get them you're free and move, but with no extra roll. If not, you stay in jail. After the **3rd** failed try you must pay $50, and then you move.

## Do it

1. In `logic/game.py`, add the new names at the top:

```python
BAIL = 50
JAIL_SPACE = 10

JAIL = "JAIL"              # current player is in jail: pay, or try for doubles
```

   In `__init__`, after `self.dice = (0, 0)`:

```python
        self.doubles_in_a_row = 0
        self.roll_again = False
```

2. Replace `start_turn`, `roll` and `finish_move`:

```python
    def start_turn(self):
        player = self.current_player()
        self.doubles_in_a_row = 0
        self.roll_again = False
        self.say(f"--- {player.name}'s turn ---")
        if player.in_jail:
            self.phase = JAIL
        else:
            self.phase = ROLL

    def roll(self):
        if self.phase != ROLL:
            return
        player = self.current_player()
        self.dice = self.roll_dice()
        die1, die2 = self.dice
        self.say(f"{player.name} rolled {die1} and {die2}")

        self.roll_again = die1 == die2
        if die1 == die2:
            self.doubles_in_a_row += 1
            # TODO: on the 3rd double: say "Three doubles in a row. Speeding!",
            #       send them to jail, set the phase to END_TURN, and return

        self.phase = MOVING
        self.move_forward(player, die1 + die2)
        self.land(player)
        if self.phase == MOVING:
            self.finish_move()

    def finish_move(self):
        """This roll is completely sorted out. What happens next?"""
        player = self.current_player()
        if self.roll_again and not player.in_jail:
            self.phase = ROLL
        else:
            self.phase = END_TURN
```

3. Add a new section of jail rules to `Game`:

```python
    # ---------- jail ----------

    def send_to_jail(self, player):
        player.position = JAIL_SPACE
        player.in_jail = True
        player.jail_turns = 0
        self.roll_again = False
        self.say(f"{player.name} goes to jail!")

    def leave_jail(self, player):
        player.in_jail = False
        player.jail_turns = 0

    def pay_bail(self):
        player = self.current_player()
        if self.phase != JAIL or player.cash < BAIL:
            return
        self.transfer(player, BANK, BAIL, "bail")
        self.leave_jail(player)
        self.phase = ROLL

    def roll_in_jail(self):
        if self.phase != JAIL:
            return
        player = self.current_player()
        self.dice = self.roll_dice()
        die1, die2 = self.dice
        self.say(f"{player.name} rolled {die1} and {die2}")

        if die1 == die2:
            self.say(f"Doubles! {player.name} is free")
        else:
            player.jail_turns += 1
            if player.jail_turns < 3:
                self.say(f"No doubles. Still in jail (try {player.jail_turns} of 3)")
                self.phase = END_TURN
                return
            self.say("Third try failed, so bail must be paid")
            self.transfer(player, BANK, BAIL, "bail")

        # Leaving jail this way moves you, but never gives a bonus roll.
        self.leave_jail(player)
        self.phase = MOVING
        self.move_forward(player, die1 + die2)
        self.land(player)
        if self.phase == MOVING:
            self.finish_move()
```

4. In `land`, after the `self.say(...)` line:

```python
        if space.kind == "GO_TO_JAIL":
            self.send_to_jail(player)
```

5. **Tests.** Add to `tests/test_moving.py` (and add `ROLL` to its import from `logic.game`):

```python
def test_doubles_means_roll_again():
    game = make_game((2, 2))
    game.roll()
    assert game.phase == ROLL


def test_three_doubles_sends_you_to_jail():
    game = make_game((5, 5), (5, 5), (5, 5))
    ann = game.players[0]
    game.roll()
    game.roll()
    game.roll()
    assert ann.in_jail
    assert ann.position == 10
    assert game.phase == END_TURN
```

   Add to `tests/test_money.py`:

```python
def test_go_to_jail_space():
    game = make_game((2, 3))
    ann = game.players[0]
    ann.position = 25
    game.roll()                      # 25 + 5 = 30: Go To Jail
    assert ann.in_jail
    assert ann.position == 10
    assert ann.cash == 1500          # no $200 for "passing" Go on the way to jail
```

   Create `tests/test_jail.py`:

```python
from helpers import make_game

from logic.game import END_TURN, JAIL, ROLL


def jailed_game(*rolls):
    game = make_game(*rolls)
    game.send_to_jail(game.players[0])
    game.start_turn()
    return game


def test_jail_turn_starts_in_jail_phase():
    game = jailed_game()
    assert game.phase == JAIL


def test_paying_bail():
    game = jailed_game()
    ann = game.players[0]
    game.pay_bail()
    assert not ann.in_jail
    assert ann.cash == 1450
    assert game.phase == ROLL


def test_rolling_doubles_gets_you_out_but_no_extra_roll():
    game = jailed_game((3, 3))
    ann = game.players[0]
    game.roll_in_jail()
    assert not ann.in_jail
    assert ann.position == 16
    assert game.phase != ROLL


def test_failing_to_roll_doubles_keeps_you_in():
    game = jailed_game((1, 2))
    ann = game.players[0]
    game.roll_in_jail()
    assert ann.in_jail
    assert ann.position == 10
    assert game.phase == END_TURN


def test_third_fail_makes_you_pay_and_move():
    pass    # TODO: jailed_game((1, 2)), set Ann's jail_turns to 2, roll_in_jail,
            #       then check she's out, has $1450, and is on space 13
```

6. **Sidebar.** In `ui/sidebar.py`, import `BAIL` and `JAIL` from `logic.game` too. Then:
   - in `__init__`, add two buttons:

```python
        self.jail_roll_button = Button("Try for doubles", screen.roll_in_jail, color=theme.GREEN)
        self.bail_button = Button(f"Pay {money(BAIL)}", game.pay_bail, color=theme.ORANGE)
```

   - in `main_buttons`, add: `if self.game.phase == JAIL: return [self.jail_roll_button, self.bail_button]`
   - at the top of `update`: `self.bail_button.enabled = self.game.current_player().cash >= BAIL`
   - in `describe`, put these **before** the plain `ROLL` line:

```python
    player = game.current_player()
    if game.phase == ROLL and game.roll_again:
        return "Doubles! Roll again."
```

   and add:

```python
    if game.phase == JAIL:
        return (f"You're in jail. Pay {money(BAIL)} or try to roll doubles "
                f"(try {player.jail_turns + 1} of 3).")
```

   - at the end of `draw_players`, inside the loop, show an "IN JAIL" badge:

```python
            badges = []
            if player.in_jail:
                badges.append(("IN JAIL", theme.ORANGE))
            right = card.right - 14
            for words, color in badges:
                width = theme.font(13, True).size(words)[0] + 14
                badge = pygame.Rect(right - width, card.y + 50, width, 20)
                pygame.draw.rect(surface, color, badge, border_radius=10)
                text(surface, words, badge.center, 13, theme.WHITE, bold=True, anchor="center")
                right = badge.x - 6
```

   (`badges` is a list because more badges are coming later.)

7. In `ui/play_screen.py`, add the method the new button calls:

```python
    def roll_in_jail(self):
        self.game.roll_in_jail()
```

8. **Jail tokens.** In `ui/board_view.py`, import `from logic.game import JAIL_SPACE` and `CORNER` from `ui.board_layout`. Players *in* jail sit behind the bars, and visitors sit along the edge. In `draw_tokens`, right after `rect = space_rect(index)`:

```python
            if index == JAIL_SPACE:
                self.draw_jail_tokens(surface, rect, players, current, pulse)
                continue
```

   and add the method:

```python
    def draw_jail_tokens(self, surface, rect, players, current, pulse):
        cell = pygame.Rect(rect.right - 80, rect.y, 80, 80)
        visiting = pygame.Rect(rect.x, rect.bottom - 33, CORNER, 33)
        inside = [player for player in players if player.in_jail]
        outside = [player for player in players if not player.in_jail]
        for group, area in ((inside, cell), (outside, visiting)):
            for player, spot in zip(group, spots_in(area, len(group), gap=24)):
                if player is current:
                    pygame.draw.circle(surface, theme.WHITE, spot, 16 + pulse, 2)
                token(surface, player, spot, radius=12)
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Doubles → "Doubles! Roll again." and the Roll button comes back
- [ ] Land on Go To Jail → your token jumps behind the bars, and next turn you get the jail buttons

## Save

Commit message: `Quest 13: doubles and jail`
