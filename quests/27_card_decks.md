# Quest 27: Shuffled Chance and Community Chest decks

## Why this quest
Before any card can do anything, you need the decks themselves: shuffled, drawable, and cycling used cards back through so the deck never runs dry.

## Your tasks

1. Create `data/chance.json` and `data/community_chest.json`, each a JSON list of card objects with `text` (what the card says) and `action` (a short code name for what it does — see Quest 28 for the list of action types) plus any extra parameters an action needs (e.g. an amount, or a destination space name).
2. Create `monopoly/cards.py`.
3. Write `load_cards(path)` — same JSON-loading pattern as `load_board`, but simpler since cards don't need a custom class; plain dictionaries are fine here.
4. Write `build_deck(cards)`: return a shuffled copy of the list (use `random.sample(cards, len(cards))`, which shuffles without changing the original list — useful for testing with a fixed known order later).
5. Write `draw_card(deck, discard_pile)`: pop the top card, append it to `discard_pile`, and if the deck is now empty, shuffle `discard_pile` back into `deck` and clear `discard_pile`. Return the drawn card.
6. Store two decks and two discard piles on `GameState` (add `chance_deck`, `chance_discard`, `chest_deck`, `chest_discard` fields).

## Starter code

`data/chance.json` (a few examples — add the full standard 16-card set):
```json
[
  {"text": "Advance to Go (Collect $200)", "action": "MOVE_TO", "target": 0},
  {"text": "Bank pays you dividend of $50", "action": "RECEIVE", "amount": 50},
  {"text": "Go to Jail. Go directly to Jail.", "action": "GO_TO_JAIL"},
  {"text": "Get out of Jail Free. This card may be kept.", "action": "KEEP_JAIL_CARD"}
]
```

`monopoly/cards.py`:
```python
import json
import random

def load_cards(path):
    with open(path) as f:
        return json.load(f)


def build_deck(cards):
    # TODO: return a shuffled copy of cards (don't shuffle the original list in place)
    pass


def draw_card(deck, discard_pile):
    card = deck.pop()
    discard_pile.append(card)
    if len(deck) == 0:
        # TODO: shuffle discard_pile back into deck, then empty discard_pile
        pass
    return card
```

Add to `GameState.__init__` in `monopoly/models.py`:
```python
self.chance_deck = []
self.chance_discard = []
self.chest_deck = []
self.chest_discard = []
```
(You'll populate these when a `GameState` is created in `SetupScreen.start_game`, using `build_deck(load_cards("data/chance.json"))`.)

## Test it yourself
Add to `tests/test_cards.py` (new file):
```python
from monopoly.cards import load_cards, build_deck, draw_card

def test_deck_never_runs_out():
    cards = load_cards("data/chance.json")
    deck = build_deck(cards)
    discard = []
    for _ in range(50):  # draw far more than the deck has, to force recycling
        card = draw_card(deck, discard)
        assert card is not None

def test_shuffle_does_not_lose_cards():
    cards = load_cards("data/chance.json")
    deck = build_deck(cards)
    assert len(deck) == len(cards)
```
Run `python -m pytest tests/test_cards.py -v`. Both should pass — the first test is a good example of deliberately abusing your own code (draw way more than exists) to catch an edge case a normal short game would rarely hit.

## Checkpoint
```text
git commit -m "Add shuffled Chance and Community Chest decks"
```
The decks are real and never run dry — the actual card effects come next.

## Stuck? Try this
- `IndexError: pop from empty list` → your empty-deck check in `draw_card` needs to run *before* you try to `.pop()` again, or right after popping, before returning — check the order of operations.
- Every game draws cards in the same order → confirm you're really shuffling in `build_deck` and not just returning `cards` unchanged.
