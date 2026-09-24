# Quest 03: Create two player objects (practice)

## Why this quest
The real game needs a way to bundle "name, cash, position" together for each player, and a way to move money between them without bugs. Classes are how you do that. Delete this file when you're done.

## New idea(s)
**Classes and objects.** So far, if you wanted a player, you might use separate variables like `name = "Sam"` and `cash = 1500`. That gets messy with six players. A **class** is a blueprint for a bundle of related variables (called **attributes**) and functions that act on them (called **methods**). An **object** is one specific thing built from that blueprint. `self` refers to "this particular object" inside the class.

```python
class Dog:
    def __init__(self, name):
        self.name = name          # attribute
        self.energy = 10

    def bark(self):               # method
        print(f"{self.name} says woof!")
        self.energy -= 1

rex = Dog("Rex")   # rex is an object built from the Dog class
rex.bark()         # Rex says woof!
print(rex.energy)  # 9
```

## Your tasks

1. Create `scratch_practice_c.py`.
2. Write a `Player` class with `__init__(self, name)` that sets `self.name`, `self.cash = 1500`, and `self.position = 0`.
3. Give it a method `pay(self, other, amount)` that subtracts `amount` from `self.cash` and adds it to `other.cash`.
4. Create two `Player` objects.
5. Call `.pay()` to transfer 50 from one to the other.
6. Print both players' cash before and after, and confirm the total is unchanged.

## Starter code
```python
class Player:
    def __init__(self, name):
        self.name = name
        self.cash = 1500
        self.position = 0

    def pay(self, other, amount):
        # TODO: subtract amount from self.cash, add it to other.cash
        pass

alice = Player("Alice")
bob = Player("Bob")

print(f"Before: {alice.name}={alice.cash}, {bob.name}={bob.cash}")
alice.pay(bob, 50)
print(f"After:  {alice.name}={alice.cash}, {bob.name}={bob.cash}")
```

## Test it yourself
Run `python scratch_practice_c.py`. Confirm Alice's cash dropped by exactly 50, Bob's rose by exactly 50, and `alice.cash + bob.cash` is the same number before and after (3000 total).

## Checkpoint
```text
git commit -m "Practice C: Player class with a pay method"
```
You just wrote a simplified version of the money-transfer rule the real game will use for every rent payment, tax, and trade.

## Stuck? Try this
- `TypeError: pay() missing 1 required positional argument` → you called `alice.pay(50)` instead of `alice.pay(bob, 50)` — methods still need every argument except `self`.
- Money "disappears" or duplicates → make sure you're changing `self.cash` and `other.cash`, not creating new local variables with the same names.
- `AttributeError: 'Player' object has no attribute 'cash'` → check the spelling matches exactly between `__init__` and where you use it.
