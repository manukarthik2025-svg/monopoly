# Quest 18 · Card decks

**Goal:** Chance and Community Chest cards: a shuffled pile of each, shown on the stage when drawn, including the "Get Out of Jail Free" card you can keep.
**New files:** `data/chance.json`, `data/community_chest.json`, `logic/cards.py`, `tests/test_cards.py` **Changed:** `logic/game.py`, `ui/card_art.py`, `ui/stage.py`, `ui/sidebar.py`, tests

## Idea: cards are data too

Every card is a small dictionary: its `text`, an `action` saying what kind of card it is, and whatever numbers that action needs:

```json
{"text": "Doctor's fee. Pay $50.", "action": "MONEY", "amount": -50}
```

`draw_card` looks at `card["action"]` and runs the matching rule. 32 cards, but only 8 kinds of action.

## Idea: a pile that never runs out

In the real game you take the top card and slide it under the pile. A list does exactly that: `pop(0)` takes the first card, and `append` puts it at the end. The Jail Free card is the exception: it stays in your hand until you use it, then goes back under the pile.

## Do it

1. Create `data/chance.json`:

```json
[
  {"text": "Advance to Boardwalk.", "action": "MOVE_TO", "target": 39},
  {"text": "Advance to Go. Collect $200.", "action": "MOVE_TO", "target": 0},
  {"text": "Advance to Illinois Avenue. If you pass Go, collect $200.", "action": "MOVE_TO", "target": 24},
  {"text": "Advance to St. Charles Place. If you pass Go, collect $200.", "action": "MOVE_TO", "target": 11},
  {"text": "Take a trip to Reading Railroad. If you pass Go, collect $200.", "action": "MOVE_TO", "target": 5},
  {"text": "Advance to the nearest Railroad. If it is owned, pay the owner twice the rent.", "action": "NEAREST", "kind": "RAILROAD"},
  {"text": "Advance to the nearest Railroad. If it is owned, pay the owner twice the rent.", "action": "NEAREST", "kind": "RAILROAD"},
  {"text": "Advance to the nearest Utility. If it is owned, roll the dice and pay the owner 10 times the roll.", "action": "NEAREST", "kind": "UTILITY"},
  {"text": "Bank pays you a dividend of $50.", "action": "MONEY", "amount": 50},
  {"text": "Your building loan matures. Collect $150.", "action": "MONEY", "amount": 150},
  {"text": "Speeding fine. Pay $15.", "action": "MONEY", "amount": -15},
  {"text": "Go back 3 spaces.", "action": "BACK", "steps": 3},
  {"text": "Go to Jail. Go directly to Jail. Do not pass Go, do not collect $200.", "action": "GO_TO_JAIL"},
  {"text": "Make general repairs on all your property. Pay $25 per house and $100 per hotel.", "action": "REPAIRS", "house": 25, "hotel": 100},
  {"text": "You have been elected Chairman of the Board. Pay each player $50.", "action": "EACH_PLAYER", "amount": -50},
  {"text": "Get Out of Jail Free. Keep this card until you need it.", "action": "JAIL_FREE"}
]
```

   and `data/community_chest.json`:

```json
[
  {"text": "Advance to Go. Collect $200.", "action": "MOVE_TO", "target": 0},
  {"text": "Bank error in your favour. Collect $200.", "action": "MONEY", "amount": 200},
  {"text": "Doctor's fee. Pay $50.", "action": "MONEY", "amount": -50},
  {"text": "From sale of stock you get $50.", "action": "MONEY", "amount": 50},
  {"text": "Holiday fund matures. Collect $100.", "action": "MONEY", "amount": 100},
  {"text": "Income tax refund. Collect $20.", "action": "MONEY", "amount": 20},
  {"text": "Life insurance matures. Collect $100.", "action": "MONEY", "amount": 100},
  {"text": "Pay hospital fees of $100.", "action": "MONEY", "amount": -100},
  {"text": "Pay school fees of $50.", "action": "MONEY", "amount": -50},
  {"text": "Receive a $25 consultancy fee.", "action": "MONEY", "amount": 25},
  {"text": "You won second prize in a beauty contest. Collect $10.", "action": "MONEY", "amount": 10},
  {"text": "You inherit $100.", "action": "MONEY", "amount": 100},
  {"text": "It is your birthday. Collect $10 from every player.", "action": "EACH_PLAYER", "amount": 10},
  {"text": "You are assessed for street repairs. Pay $40 per house and $115 per hotel.", "action": "REPAIRS", "house": 40, "hotel": 115},
  {"text": "Go to Jail. Go directly to Jail. Do not pass Go, do not collect $200.", "action": "GO_TO_JAIL"},
  {"text": "Get Out of Jail Free. Keep this card until you need it.", "action": "JAIL_FREE"}
]
```

2. Create `logic/cards.py`:

```python
import json
import random

from logic.board import DATA_FOLDER


class Deck:
    """A pile of Chance or Community Chest cards."""

    def __init__(self, name, cards, shuffle=True):
        self.name = name
        self.cards = list(cards)
        if shuffle:
            random.shuffle(self.cards)

    def draw(self):
        """Take the top card. Most cards go straight back under the pile."""
        card = self.cards.pop(0)
        if card["action"] != "JAIL_FREE":    # that one stays in the player's hand
            self.cards.append(card)
        return card

    def put_back(self, card):
        self.cards.append(card)


def load_deck(name, filename):
    with open(DATA_FOLDER / filename) as file:
        cards = json.load(file)
    for card in cards:
        card["deck"] = name      # so a Jail Free card remembers which pile it belongs to
    return Deck(name, cards)
```

3. In `logic/game.py`, import `from logic.cards import load_deck`. In `__init__`, after `self.board = ...`:

```python
        self.decks = {
            "Chance": load_deck("Chance", "chance.json"),
            "Community Chest": load_deck("Community Chest", "community_chest.json"),
        }
```

   and further down: `self.last_card = None`.

   In `land()`, add (the space's name is also the deck's name!):

```python
        elif space.kind == "CARD":
            self.draw_card(player, self.decks[space.name])
```

   In `end_turn()`, right after the `if ... return` check: `self.last_card = None` (so the card disappears from the stage).

   Add a `use_jail_card` rule to the jail section:

```python
    def use_jail_card(self):
        player = self.current_player()
        if self.phase != JAIL or not player.jail_cards:
            return
        card = player.jail_cards.pop()
        self.decks[card["deck"]].put_back(card)
        self.say(f"{player.name} used a Get Out of Jail Free card")
        self.leave_jail(player)
        self.phase = ROLL
```

   And a new section for the cards themselves. The cards that **move** you come next quest. Until then they just show up and do nothing.

```python
    # ---------- cards ----------

    def draw_card(self, player, deck):
        card = deck.draw()
        self.last_card = card
        self.say(f"{deck.name}: {card['text']}")
        action = card["action"]

        if action == "MONEY":
            if card["amount"] > 0:
                self.transfer(BANK, player, card["amount"], deck.name)
            else:
                self.transfer(player, BANK, -card["amount"], deck.name)

        elif action == "EACH_PLAYER":
            for other in self.active_players():
                if other is player:
                    continue
                if card["amount"] > 0:
                    self.transfer(other, player, card["amount"], deck.name)
                else:
                    pass    # TODO: the player pays -card["amount"] to `other`

        elif action == "GO_TO_JAIL":
            self.send_to_jail(player)

        elif action == "JAIL_FREE":
            player.jail_cards.append(card)
```

4. **Card art.** Add to `ui/card_art.py`:

```python
def draw_card(surface, card, center):
    """A Chance or Community Chest card."""
    color = theme.CHANCE_ORANGE if card["deck"] == "Chance" else theme.CHEST_BLUE
    outside = pygame.Rect(0, 0, 420, 250)
    outside.center = center
    panel(surface, outside, color, radius=14)
    inside = outside.inflate(-18, -18)
    pygame.draw.rect(surface, theme.WHITE, inside, border_radius=10)

    mark = theme.title_font(170).render("?", True, color)
    mark.set_alpha(45)
    surface.blit(mark, mark.get_rect(center=inside.center))

    text(surface, card["deck"].upper(), (inside.centerx, inside.y + 12), 24, color, bold=True, anchor="midtop")
    text_block(surface, card["text"], inside.centerx, inside.y + 64, inside.width - 50, 22)
    return outside
```

   In `ui/stage.py`, import `draw_card` too, and in `draw()` add this **between** the `BUY` part and the hover part:

```python
        elif game.last_card is not None:
            self.cover(surface)
            draw_card(surface, game.last_card, CENTER.center)
```

5. **Sidebar.** In `ui/sidebar.py`:
   - a new button in `__init__`: `self.card_button = Button("Use jail card", game.use_jail_card, color=theme.PURPLE)`
   - the `JAIL` line in `main_buttons` returns all three: `[self.jail_roll_button, self.bail_button, self.card_button]`
   - in `update`:

```python
        self.card_button.enabled = len(self.game.current_player().jail_cards) > 0
        self.card_button.reason = "You don't have a Get Out of Jail Free card"
```

   - the `JAIL` sentence in `describe` becomes: `f"You're in jail. Pay {money(BAIL)}, use a card, or try to roll doubles "`
   - one more badge, after the "IN JAIL" one:

```python
            if player.jail_cards:
                badges.append((f"FREE CARD x{len(player.jail_cards)}", theme.PURPLE))
```

6. **Tests.** Add to `tests/helpers.py`:

```python
def put_card_on_top(game, deck_name, words):
    """Make the next card drawn from this deck the one whose text contains `words`."""
    deck = game.decks[deck_name]
    for card in deck.cards:
        if words in card["text"]:
            break
    deck.cards.remove(card)
    deck.cards.insert(0, card)
    return card
```

   Create `tests/test_cards.py`:

```python
from helpers import make_game, put_card_on_top

from logic.cards import load_deck


def land_on_chance(game, words):
    """Stack the deck, then roll from space 4 to the Chance on space 7."""
    put_card_on_top(game, "Chance", words)
    game.players[0].position = 4
    game.roll_dice = lambda: (1, 2)
    game.roll()


def test_deck_has_16_cards_and_never_runs_out():
    deck = load_deck("Chance", "chance.json")
    assert len(deck.cards) == 16
    for _ in range(100):
        card = deck.draw()
        if card["action"] == "JAIL_FREE":    # that card leaves the pile...
            deck.put_back(card)              # ...until someone uses it
    assert len(deck.cards) == 16


def test_money_card():
    game = make_game()
    put_card_on_top(game, "Community Chest", "Bank error")
    game.draw_card(game.players[0], game.decks["Community Chest"])
    assert game.players[0].cash == 1700


def test_birthday_card_takes_from_everyone():
    game = make_game(players=3)
    deck = game.decks["Community Chest"]
    put_card_on_top(game, "Community Chest", "birthday")
    game.draw_card(game.players[0], deck)
    assert [p.cash for p in game.players] == [1520, 1490, 1490]


def test_go_to_jail_card():
    game = make_game()
    land_on_chance(game, "Go to Jail")
    assert game.players[0].in_jail
```

   And add to `tests/test_jail.py` (change its first line to `from helpers import make_game, put_card_on_top`):

```python
def test_get_out_of_jail_free_card():
    game = make_game((1, 1))
    ann = game.players[0]
    ann.position = 5
    put_card_on_top(game, "Chance", "Get Out of Jail Free")
    game.roll()                                   # lands on Chance (7)
    assert len(ann.jail_cards) == 1
    game.send_to_jail(ann)
    game.start_turn()
    game.use_jail_card()
    assert not ann.in_jail
    assert ann.jail_cards == []
    assert len(game.decks["Chance"].cards) == 16  # the card went back in the pile
```

## Check it

- [ ] `python -m pytest`: all passed
- [ ] Land on Chance → an orange card appears in the middle until you end your turn
- [ ] Get the Jail Free card and it shows as a badge. In jail, "Use jail card" lights up.

## Save

Commit message: `Quest 18: Chance and Community Chest`

⭐ **Extra:** write your own card! Invent one that uses an action that already exists.
