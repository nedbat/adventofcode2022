# https://adventofcode.com/2022/day/14

import itertools
import re


SAMPLE = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def from_to(a, b):
    """Generate numbers from a to b inclusive, regardless of which is larger."""
    if a > b:
        a, b = b, a
    return range(a, b + 1)

def line_points(x0, y0, x1, y1):
    if x0 == x1:
        xiter = itertools.repeat(x0)
    else:
        xiter = from_to(x0, x1)
    if y0 == y1:
        yiter = itertools.repeat(y0)
    else:
        yiter = from_to(y0, y1)
    return zip(xiter, yiter)


def read_cave(text):
    cave = {}
    for line in text.splitlines():
        x0 = y0 = None
        for m in re.finditer(r"(\d+),(\d+)", line):
            x1, y1 = map(int, m.groups())
            if x0 is not None:
                for x, y in line_points(x0, y0, x1, y1):
                    cave[x, y] = "#"
            x0, y0 = x1, y1
    return cave


def bounds(cave):
    return (
        min(pt[0] for pt in cave.keys()),
        min(pt[1] for pt in cave.keys()),
        max(pt[0] for pt in cave.keys()),
        max(pt[1] for pt in cave.keys()),
    )


def print_cave(cave):
    minx, miny, maxx, maxy = bounds(cave)
    for y in from_to(miny, maxy):
        for x in from_to(minx, maxx):
            print(cave.get((x, y), "."), end="")
        print()


def next_pts(x, y):
    yield (x, y + 1)
    yield (x - 1, y + 1)
    yield (x + 1, y + 1)

def drop_sand_part1(cave, sx, sy):
    bottom = max(pt[1] for pt in cave.keys())
    while True:
        if sy >= bottom:
            return None
        for nsx, nsy in next_pts(sx, sy):
            if cave.get((nsx, nsy)) is None:
                sx, sy = nsx, nsy
                break
        else:
            return sx, sy

def pour_sand(cave, drop_sand):
    num = 0
    while (spt := drop_sand(cave, 500, 0)):
        cave[spt] = "o"
        num += 1
        # print("=" * 8)
        # print_cave(cave)
        # import time; time.sleep(.25)
    return num

def part1(text):
    return pour_sand(read_cave(text), drop_sand=drop_sand_part1)

def test_part1():
    assert part1(SAMPLE) == 24

if __name__ == "__main__":
    text = open("day14_input.txt").read()
    print(f"Part 1: {part1(text)}")


def drop_sand_part2(cave, sx, sy):
    bottom = max(pt[1] for pt in cave.keys() if cave.get(pt) == "#")
    while True:
        for nsx, nsy in next_pts(sx, sy):
            if nsy == bottom + 2:
                continue
            if cave.get((nsx, nsy)) is None:
                sx, sy = nsx, nsy
                break
        else:
            if sy == 0:
                return None
            return sx, sy

def part2(text):
    return pour_sand(read_cave(text), drop_sand=drop_sand_part2) + 1

def test_part2():
    assert part2(SAMPLE) == 93

if __name__ == "__main__":
    text = open("day14_input.txt").read()
    print(f"Part 2: {part2(text)}")
