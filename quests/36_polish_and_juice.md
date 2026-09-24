# Quest 36: Make it pleasant to actually play

## Why this quest
Every rule works by now. This last quest is about a stranger being able to sit down and understand what to click without you standing over their shoulder — PLAN.md's actual definition of done.

## Your tasks

Pick these off one at a time, testing after each — this is a checklist, not one big feature:

1. **Status message.** Somewhere always visible during `GameScreen`, show one sentence describing exactly what's expected right now (e.g. "Alice: roll the dice", "Bob: pay $140 rent or raise funds"). Write one small function `describe_phase(state)` that returns this string — it's a single `if`/`elif` chain over `state.phase`, so keep it in one place rather than scattered across draw calls.
2. **Disabled-button reasons.** Anywhere you show a disabled button, show *why* it's disabled next to it, reusing the reason strings your `can_*` functions already return.
3. **Confirmations.** Before Declare Bankruptcy, Restart, or Quit with an unsaved game, show a Yes/No confirmation dialog rather than acting immediately.
4. **Scrollable history.** `state.history` is probably long by now — show the last handful of entries, with a way to scroll back further (even just Up/Down arrow keys shifting which slice of the list you display, using `history[-20:]` style slicing).
5. **Pause menu.** A key (e.g. Escape) that pauses and shows Resume/Save/Main Menu, without losing state.
6. **Rules/help screen.** Flesh out `HelpScreen` (Quest 06) with a short, real explanation of controls and any house-rule choices your game makes (e.g. no Free Parking jackpot).
7. **Keyboard controls.** At minimum, Enter/Space activates the currently-focused button, and Tab moves focus between buttons — this needs a small addition to `Button` (a `focused` state) and to each screen (tracking which button index has focus).
8. **Accessible color use.** Anywhere ownership or status is shown by color alone (property borders, token colors), add a second cue — a short label, icon, or pattern — so colorblind players aren't stuck guessing.
9. **Light animation.** A short slide/hop for token movement and a brief dice-roll animation, each skippable via a "fast animations" setting. The rules engine must decide what happened *before* the animation starts — the animation only shows it, never decides it.
10. **Optional sound.** A roll sound, a cash sound, and a mute toggle, using `pygame.mixer` — entirely optional, skip it if you'd rather not deal with audio files.

## Starter code
```python
def describe_phase(state):
    player = state.current_player()
    phase = state.phase
    if phase == "WAITING_FOR_ROLL":
        return f"{player.name}: click Roll Dice"
    if phase == "IN_JAIL_DECISION":
        return f"{player.name}: pay bail, use a card, or try for doubles"
    if phase == "AWAITING_PURCHASE":
        space = state.spaces[player.position]
        return f"{player.name}: buy {space.name} for {space.price}, or send it to auction"
    if phase == "PAYMENT_REQUIRED":
        pending = state.pending_decision
        return f"{player.name}: pay {pending.amount} ({pending.reason}) or go bankrupt"
    if phase == "TURN_END":
        return f"{player.name}: click End Turn when ready"
    # TODO: cover AUCTION, TRADING, GAME_OVER, and any other phase you added
    return ""
```

A minimal confirmation dialog pattern you can reuse for bankruptcy/restart/quit:
```python
class ConfirmDialog:
    def __init__(self, message, on_yes):
        self.message = message
        self.on_yes = on_yes
        self.yes_button = Button((400, 400, 100, 50), "Yes", on_click=self._confirm)
        self.no_button = Button((520, 400, 100, 50), "No", on_click=lambda: None)
        self.done = False

    def _confirm(self):
        self.on_yes()
        self.done = True
```

## Test it yourself
There's no single automated check for "does this feel good" — instead, hand the game to someone who hasn't seen the code (or pretend to be a first-time player yourself) and watch where they hesitate or click the wrong thing. Every hesitation is a spot that needs a clearer label or a status message.

## Checkpoint
```text
git commit -m "Polish: status messages, confirmations, keyboard input, help screen"
```
You've now met PLAN.md's full definition of done: a stranger can play from setup to a winner without touching the terminal.

## Stuck? Try this
- Status message is technically correct but confusing → read it out loud as if you'd never seen the game before; if it needs jargon like "phase" or "pending decision" to make sense, rewrite it in plain terms.
- Animations start feeling like they're deciding outcomes → double-check the rule function (e.g. `move_player`) still runs and updates real state immediately; the animation should just be drawing a smooth transition toward a destination that's already been decided, over a few frames.
