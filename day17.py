# https://adventofcode.com/2022/day/17

import itertools
from dataclasses import dataclass


SAMPLE = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

WIDTH = 7

@dataclass(frozen=True)
class Pt:
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

LEFT = Pt(-1, 0)
RIGHT = Pt(1, 0)
DOWN = Pt(0, -1)

@dataclass(frozen=True)
class Shape:
    pts: set[Pt]

    def __iter__(self):
        return iter(self.pts)

    def __matmul__(self, pos):
        return Shape({pt + pos for pt in self.pts})

SHAPES = [
    Shape([Pt(0, 0), Pt(1, 0), Pt(2, 0), Pt(3, 0)]),
    Shape([Pt(1, 0), Pt(0, 1), Pt(1, 1), Pt(2, 1), Pt(1, 2)]),
    Shape([Pt(0, 0), Pt(1, 0), Pt(2, 0), Pt(2, 1), Pt(2, 2)]),
    Shape([Pt(0, 0), Pt(0, 1), Pt(0, 2), Pt(0, 3)]),
    Shape([Pt(0, 0), Pt(1, 0), Pt(0, 1), Pt(1, 1)]),
]

def height(chamber):
    return max((pt.y for pt in chamber), default=-1) + 1

def can_place(chamber, shape):
    if min(pt.x for pt in shape) < 0:
        return False
    if max(pt.x for pt in shape) > WIDTH - 1:
        return False
    if min(pt.y for pt in shape) < 0:
        return False
    if chamber & shape.pts:
        return False
    return True

def draw_chamber(chamber):
    print(chamber)
    for y in range(height(chamber), -1, -1):
        print("|", end="")
        for x in range(WIDTH):
            print("#" if Pt(x, y) in chamber else ".", end="")
        print("|")
    print("+-------+\n")

def drop_rocks(jet_text):
    chamber = set()
    jets = itertools.cycle(jet_text)
    shapes = itertools.cycle(SHAPES)

    for i in range(2022):
        pos = Pt(x=2, y=height(chamber) + 3)
        shape = next(shapes) @ pos
        #print(f"Dropping {i}: {shape}")
        while True:
            # jet push
            jet_push = LEFT if next(jets) == "<" else RIGHT
            pushed_shape = shape @ jet_push
            if can_place(chamber, pushed_shape):
                shape = pushed_shape
                #print(f"Pushed {jet_push} to {shape}")

            # down
            down_shape = shape @ DOWN
            if can_place(chamber, down_shape):
                #print(f"Dropped to {down_shape}")
                shape = down_shape
            else:
                #print(f"Placing {shape}")
                chamber |= shape.pts
                #draw_chamber(chamber)
                break

    return chamber

def part1(text):
    chamber = drop_rocks(text)
    return height(chamber)

def test_part1():
    assert part1(SAMPLE) == 3068

if __name__ == "__main__":
    text = open("day17_input.txt").read().strip()
    print(f"Part 1: {part1(text)}")
