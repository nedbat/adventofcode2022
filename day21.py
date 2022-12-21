# https://adventofcode.com/2022/day/21

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
    for line in text.splitlines():
        match line.split():
            case [monkey, number]:
                jobs[monkey.strip(":")] = int(number)

            case [monkey, m1, op, m2]:
                jobs[monkey.strip(":")] = (m1, op, m2)

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
