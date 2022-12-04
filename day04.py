# https://adventofcode.com/2022/day/4

from dataclasses import dataclass
import re

SAMPLE = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".splitlines()

@dataclass
class Range:
    low: int
    high: int

    def fully_contains(self, other):
        return self.low <= other.low and self.high >= other.high

    def overlaps(self, other):
        return self.high >= other.low and other.high >= self.low

def range_pairs(lines):
    for line in lines:
        a, b, c, d = map(int, re.findall(r"\d+", line))
        yield Range(a, b), Range(c, d)

def test_range_pairs():
    assert next(range_pairs(SAMPLE)) == (Range(2, 4), Range(6, 8))

def part1(lines):
    contained = 0
    for r1, r2 in range_pairs(lines):
        if r1.fully_contains(r2) or r2.fully_contains(r1):
            contained += 1
    return contained

def test_part1():
    assert part1(SAMPLE) == 2

if __name__ == "__main__":
    data = open("day04_input.txt").read().splitlines()
    print(f"Part 1: {part1(data)}")


def part2(lines):
    overlaps = 0
    for r1, r2 in range_pairs(lines):
        if r1.overlaps(r2):
            overlaps += 1
    return overlaps

def test_part2():
    assert part2(SAMPLE) == 4

if __name__ == "__main__":
    data = open("day04_input.txt").read().splitlines()
    print(f"Part 2: {part2(data)}")
