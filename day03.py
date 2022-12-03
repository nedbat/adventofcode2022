# https://adventofcode.com/2022/day/3

import string

SAMPLE = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".splitlines()

def items(input_lines):
    for line in input_lines:
        line = line.strip()
        half_len = len(line) // 2
        yield line[:half_len], line[half_len:]

az = string.ascii_lowercase
priority = {c: i+1 for i, c in enumerate(az + az.upper())}

def common_types(input_lines):
    for first, second in items(input_lines):
        yield (set(first) & set(second)).pop()

def part1(input_lines):
    return sum(priority[t] for t in common_types(input_lines))

def test_part1():
    assert part1(SAMPLE) == 157

if __name__ == "__main__":
    ans = part1(open("day03_input.txt"))
    print(f"Part 1: {ans}")
