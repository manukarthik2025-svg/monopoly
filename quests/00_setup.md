# Quest 00: Get your tools ready

## Why this quest
Before you write a single line of the game, you need Python, Pygame, and pytest installed, and a place for your code to live. This quest gets your computer ready so every later quest just works.

## Your tasks

1. Check you have Python 3.12 or newer: open a terminal and run `python --version`.
2. In your project folder, create a virtual environment (a private box of Python packages just for this project):
   ```powershell
   python -m venv .venv
   ```
3. Turn it on:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   You'll know it worked because your terminal prompt now starts with `(.venv)`.
4. Install the two packages you'll need:
   ```powershell
   python -m pip install pygame pytest
   ```
5. Create a file called `requirements.txt` in your project folder containing:
   ```text
   pygame
   pytest
   ```
6. Create empty folders: `monopoly/`, `data/`, `tests/`, `saves/`.
7. Inside `monopoly/`, create an empty file called `__init__.py`. This tells Python "this folder is a package you can import from."
8. Run `git init` if you haven't already, and make a `.gitignore` file containing:
   ```text
   .venv/
   __pycache__/
   saves/*.json
   ```

## Test it yourself
Run this and confirm both lines print a version number with no errors:
```powershell
python -c "import pygame; print(pygame.ver)"
python -c "import pytest; print(pytest.__version__)"
```

## Checkpoint
```text
git commit -m "Set up project structure and dependencies"
```
You just built the foundation every other quest depends on — nothing fancy, but nothing else works without it.

## Stuck? Try this
- `python` not found → try `py` instead on Windows, or reinstall Python and check "Add to PATH" during install.
- `Activate.ps1 cannot be loaded because running scripts is disabled` → run PowerShell as your normal user and use `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then try activating again.
- `pip install` fails with a permissions error → make sure the `(.venv)` prefix is showing in your prompt; if it's not, the venv isn't active.
