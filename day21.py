# https://adventofcode.com/2022/day/21

import collections
import re

SAMPLE = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

def read_jobs(text):
    jobs = {}
    counts = collections.Counter()
    for line in text.splitlines():
        match line.split():
            case [monkey, number]:
                jobs[monkey.strip(":")] = int(number)

            case [monkey, m1, op, m2]:
                jobs[monkey.strip(":")] = (m1, op, m2)
                counts[m1] += 1
                counts[m2] += 1

            case _:
                raise Exception(f"Buh? {line!r}")
    return jobs

OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b,
}

def yell(jobs):
    yelled = {monkey: number for monkey, number in jobs.items() if isinstance(number, int)}

    while len(yelled) < len(jobs):
        for monkey, rule in jobs.items():
            if monkey not in yelled:
                m1, op, m2 = rule
                if m1 in yelled and m2 in yelled:
                    yelled[monkey] = OPS[op](yelled[m1], yelled[m2])

    return yelled

def part1(text):
    yelled = yell(read_jobs(text))
    return yelled["root"]

def test_part1():
    assert part1(SAMPLE) == 152

if __name__ == "__main__":
    text = open("day21_input.txt").read()
    print(f"Part 1: {part1(text)}")


def work_ast(jobs):
    jobs["humn"] = "humn"
    root = jobs["root"]
    jobs["root"] = root[0], "==", root[2]

    yelled = {monkey: number for monkey, number in jobs.items() if isinstance(number, int)}

    while True:
        any_changed = False
        for monkey, rule in jobs.items():
            if monkey == "humn":
                continue
            if monkey not in yelled:
                m1, op, m2 = rule
                m1, op, m2 = rule
                if m1 in yelled and m2 in yelled:
                    yelled[monkey] = OPS[op](yelled[m1], yelled[m2])
                    any_changed = True
        if not any_changed:
            break

    a, _, b = jobs["root"]
    if a in yelled:
        name = a
        num = yelled[a]
        expr = jobs[b]
    else:
        name = b
        num = yelled[b]
        expr = jobs[a]

    while "humn" not in yelled:
        a, op, b = expr
        ya = yelled.get(a)
        yb = yelled.get(b)
        match ya, op, yb:
            case None, _, None:
                raise Exception("Stuck")

            case int(), _, int():
                raise Exception(f"Misunderstood: {name} = {ya} {op} {yb}")

            case None, "+", int():
                yelled[name := a] = num = num - yb
                expr = jobs[a]

            case None, "-", int():
                yelled[name := a] = num = num + yb
                expr = jobs[a]

            case None, "*", int():
                yelled[name := a] = num = num // yb
                expr = jobs[a]

            case None, "/", int():
                yelled[name := a] = num = num * yb
                expr = jobs[a]

            case int(), "+", None:
                yelled[name := b] = num = num - ya
                expr = jobs[b]

            case int(), "-", None:
                yelled[name := b] = num = ya - num
                expr = jobs[b]

            case int(), "*", None:
                yelled[name := b] = num = num // ya
                expr = jobs[b]

            case int(), "/", None:
                print(f"4: {num} = {ya} {op} {b}")
                raise Exception(f"Division? {num} = {ya} / {b}")

    return yelled

def part2(text):
    yelled = work_ast(read_jobs(text))
    return yelled["humn"]

def test_part2():
    assert part2(SAMPLE) == 301

if __name__ == "__main__":
    text = open("day21_input.txt").read()
    print(f"Part 2: {part2(text)}")
