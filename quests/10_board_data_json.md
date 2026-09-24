# Quest 10: Describe the board in JSON

## Why this quest
Forty spaces means forty sets of names, prices, and rents. Writing that as Python code would mean editing source code every time you wanted to tweak a price. Instead, you'll put it in a data file — this is the "keep data and code separate" idea: prices and names are *facts*, not *behavior*.

## New idea(s)
**JSON.** JSON is a plain-text way to write down lists and dictionaries that both humans and programs can read. A Python dictionary and a chunk of JSON look almost identical:

```python
# Python
person = {"name": "Sam", "age": 13, "hobbies": ["chess", "coding"]}
```
```json
// JSON
{"name": "Sam", "age": 13, "hobbies": ["chess", "coding"]}
```
The only real differences: JSON has no comments, and JSON's `true`/`false`/`null` are Python's `True`/`False`/`None`.

## Your tasks

1. Create `data/board.json`.
2. It should contain a JSON list of exactly 40 objects, one per space, index 0 (Go) through 39 (Boardwalk).
3. Every space needs `index`, `name`, `space_type`.
4. Every `"STREET"` space additionally needs: `price`, `mortgage_value`, `group` (the color name), `house_cost`, and `rent` (a list of exactly 6 numbers: no houses, 1, 2, 3, 4 houses, hotel).
5. Every `"RAILROAD"` needs `price` and `mortgage_value` (railroads don't use `rent` here — you'll calculate railroad rent from a formula in a later quest).
6. Every `"UTILITY"` needs `price` and `mortgage_value`.
7. `"TAX"` spaces need a `price` field holding the amount owed (reuse `price` rather than invent a new field name).
8. You can find the standard US-edition board layout, prices, and rents online or in `PLAN.md`'s references — don't retype them from memory, look them up and double check your list has no typos.

## Starter code
Just the first few entries to show the shape — you fill in the remaining 36:
```json
[
  {"index": 0, "name": "Go", "space_type": "GO"},
  {"index": 1, "name": "Mediterranean Avenue", "space_type": "STREET",
   "price": 60, "mortgage_value": 30, "group": "brown", "house_cost": 50,
   "rent": [2, 10, 30, 90, 160, 250]},
  {"index": 2, "name": "Community Chest", "space_type": "COMMUNITY_CHEST"},
  {"index": 3, "name": "Baltic Avenue", "space_type": "STREET",
   "price": 60, "mortgage_value": 30, "group": "brown", "house_cost": 50,
   "rent": [4, 20, 60, 180, 320, 450]},
  {"index": 4, "name": "Income Tax", "space_type": "TAX", "price": 200},
  {"index": 5, "name": "Reading Railroad", "space_type": "RAILROAD",
   "price": 200, "mortgage_value": 100}
  // TODO: continue through index 39 (Boardwalk)
]
```
Note: real JSON files can't contain `//` comments — remove that line before you're done.

## Test it yourself
Run this to confirm the file at least parses and has 40 entries:
```powershell
python -c "import json; data = json.load(open('data/board.json')); print(len(data))"
```
It should print `40` with no error. If it crashes, JSON is very picky about commas and quotes — read the error message, it tells you the line number.

## Checkpoint
```text
git commit -m "Add 40-space board data"
```
This file *is* the Monopoly board now — every future quest reads from it instead of hardcoding space info.

## Stuck? Try this
- `json.decoder.JSONDecodeError` → almost always a missing comma between entries, a trailing comma after the last entry (not allowed in JSON), or single quotes instead of double quotes.
- Fewer or more than 40 entries → count them, or wait for Quest 11's automatic check, which will tell you exactly what's wrong.
- Unsure of exact prices/rents → check `PLAN.md`'s milestone descriptions and any standard Monopoly rules reference; accuracy here matters because every rent test later depends on it.
