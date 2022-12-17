# https://adventofcode.com/2022/day/17

import itertools
from dataclasses import dataclass, field


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

@dataclass
class Chamber:
    cells: set[Pt] = field(default_factory=set)
    heights: list[int] = field(default_factory=lambda: [0] * WIDTH)
    removed: int = 0

    def height(self):
        return max((pt.y for pt in self.cells), default=-1) + 1

    def can_place(self, shape):
        if min(pt.x for pt in shape) < 0:
            return False
        if max(pt.x for pt in shape) > WIDTH - 1:
            return False
        if min(pt.y for pt in shape) < 0:
            return False
        if self.cells & shape.pts:
            return False
        return True

    def place(self, shape):
        self.cells |= shape.pts
        for pt in shape:
            if pt.y >= self.heights[pt.x]:
                self.heights[pt.x] = pt.y + 1
        self.removed = min(self.heights)
        self.cells = {pt for pt in self.cells if pt.y >= self.removed - 1}

    def draw(self):
        for y in range(self.height(), self.removed-2, -1):
            print(f"{y:5} |", end="")
            for x in range(WIDTH):
                print("#" if Pt(x, y) in self.cells else ".", end="")
            print("|")
        print()

def drop_rocks(jet_text):
    chamber = Chamber()
    jets = itertools.cycle(jet_text)
    shapes = itertools.cycle(SHAPES)

    for i in range(30):
        pos = Pt(x=2, y=chamber.height() + 3)
        shape = next(shapes) @ pos
        while True:
            # jet push
            jet_push = LEFT if next(jets) == "<" else RIGHT
            pushed_shape = shape @ jet_push
            if chamber.can_place(pushed_shape):
                shape = pushed_shape

            # down
            down_shape = shape @ DOWN
            if chamber.can_place(down_shape):
                shape = down_shape
            else:
                chamber.place(shape)
                chamber.draw()
                break

    return chamber

def part1(text):
    chamber = drop_rocks(text)
    chamber.draw()
    return chamber.height()

def test_part1():
    assert part1(SAMPLE) == 3068

if __name__ == "__main__":
    text = open("day17_input.txt").read().strip()
    print(f"Part 1: {part1(text)}")
