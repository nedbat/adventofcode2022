# https://adventofcode.com/2022/day/11

from dataclasses import dataclass, field
import re
from typing import Callable

SAMPLE = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

@dataclass
class Monkey:
    items: list[int] = field(default_factory=list)
    op: Callable[int, int] = None
    divisor: int = 1
    true_to: int = 0
    false_to: int = 0
    items_inspected: int =  0

    @classmethod
    def from_text(cls, text):
        monkey = cls()
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("Starting items:"):
                monkey.items = list(map(int, re.findall(r"\d+", line)))
            elif line.startswith("Operation:"):
                op, operand = line.split()[-2:]
                if operand == "old":
                    assert op == "*"
                    monkey.op = lambda old: old * old
                else:
                    if op == "+":
                        monkey.op = lambda old, num=int(operand): old + num
                    else:
                        assert op == "*"
                        monkey.op = lambda old, num=int(operand): old * num
            elif line.startswith("Test:"):
                monkey.divisor = int(line.split()[-1])
            elif line.startswith("If true:"):
                monkey.true_to = int(line.split()[-1])
            elif line.startswith("If false:"):
                monkey.false_to = int(line.split()[-1])
        return monkey

    def turn(self, monkeys, msg):
        for item in self.items:
            msg(f"Inspects {item}")
            self.items_inspected += 1
            item = self.op(item)
            msg(f" Worry goes to {item}")
            item //= 3
            msg(f" Divided by 3 to {item}")
            tf = (item % self.divisor == 0)
            msg(f" Divisible by {self.divisor}? {tf}")
            goes_to = self.true_to if tf else self.false_to
            msg(f" Throw to {goes_to}")
            monkeys[goes_to].items.append(item)
        self.items = []


@dataclass
class Monkeys:
    monkeys: list[Monkey] = field(default_factory=list)

    @classmethod
    def from_text(cls, text):
        monkeys = cls()
        for chunk in text.split("\n\n"):
            monkeys.monkeys.append(Monkey.from_text(chunk))
        return monkeys

    def __len__(self):
        return len(self.monkeys)

    def __getitem__(self, n):
        return self.monkeys[n]

    def round(self, msg=None):
        if msg is None:
            msg = lambda text: None
        for i, monkey in enumerate(self.monkeys):
            msg(f"Monkey {i}")
            monkey.turn(self, msg)
            msg(f"")

    def all_items(self):
        return [m.items for m in self.monkeys]

def test_parse_one_monkey():
    monkey = Monkey.from_text(SAMPLE.split("\n\n")[0])
    assert monkey.items == [79, 98]
    assert monkey.op(10) == 190
    assert monkey.divisor == 23
    assert monkey.true_to == 2
    assert monkey.false_to == 3

def test_parse_monkeys():
    monkeys = Monkeys.from_text(SAMPLE)
    assert monkeys.all_items() == [[79, 98], [54, 65, 75, 74], [79, 60, 97], [74]]

def test_turn():
    monkeys = Monkeys.from_text(SAMPLE)
    monkeys.round()
    assert monkeys.all_items() == [[20, 23, 27, 26], [2080, 25, 167, 207, 401, 1046], [], []]
    for _ in range(19):
        monkeys.round()
    assert monkeys.all_items() == [[10, 12, 14, 26, 34], [245, 93, 53, 199, 115], [], []]

def part1(text):
    monkeys = Monkeys.from_text(text)
    for _ in range(20):
        monkeys.round()
    by_activty = sorted(monkeys.monkeys, key=lambda m: m.items_inspected)
    return by_activty[-1].items_inspected * by_activty[-2].items_inspected

def test_part1():
    assert part1(SAMPLE) == 10605

if __name__ == "__main__":
    text = open("day11_input.txt").read()
    print(f"Part 1: {part1(text)}")
