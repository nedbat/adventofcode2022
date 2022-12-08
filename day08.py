# https://adventofcode.com/2022/day/8

import itertools

SAMPLE = """\
30373
25512
65332
33549
35390
""".splitlines()

def read_trees(lines):
    return [[int(c) for c in line] for line in lines]

def dimensions(trees):
    return len(trees[0]), len(trees)

def sight_lines(x, y, w, h):
    yield ((xx, y) for xx in range(x))
    yield ((xx, y) for xx in range(x+1, w))
    yield ((x, yy) for yy in range(y))
    yield ((x, yy) for yy in range(y+1, h))

def visible(x, y, trees):
    w, h = dimensions(trees)
    tree = trees[y][x]
    return any(
        all(trees[yy][xx] < tree for xx, yy in sight_line)
        for sight_line in sight_lines(x, y, w, h)
    )

def range2d(endx, endy):
    yield from itertools.product(range(endx), range(endy))

def part1(lines):
    trees = read_trees(lines)
    w, h = dimensions(trees)
    return sum(visible(x, y, trees) for x, y in range2d(w, h))

def test_part1():
    assert part1(SAMPLE) == 21

if __name__ == "__main__":
    lines = open("day08_input.txt").read().splitlines()
    print(f"Part 1: {part1(lines)}")
