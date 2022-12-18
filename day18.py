# https://adventofcode.com/2022/day/18

import re

SAMPLE = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

def neighbors(x, y, z):
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)

def read_cubes(text):
    cubes = set()
    for line in text.splitlines():
        cubes.add(tuple(map(int, re.findall(r"\d+", line))))
    return cubes

def exposed_sides(cubes):
    exposed = 0
    for pt in cubes:
        for npt in neighbors(*pt):
            if npt not in cubes:
                exposed += 1
    return exposed

def part1(text):
    return exposed_sides(read_cubes(text))

def test_part1():
    assert part1(SAMPLE) == 64

if __name__ == "__main__":
    text = open("day18_input.txt").read()
    print(f"Part 1: {part1(text)}")
