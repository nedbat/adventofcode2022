# https://adventofcode.com/2022/day/9

import pytest


SAMPLE = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".splitlines()

DIRECTIONS = {
    "R": (1, 0),
    "U": (0, -1),
    "L": (-1, 0),
    "D": (0, 1),
}

class Rope:
    def __init__(self):
        self.hx = self.hy = 0
        self.tx = self.ty = 0
        self.visited = {(0, 0)}

    def move(self, dhx, dhy):
        self.hx += dhx
        self.hy += dhy
        dx = self.hx - self.tx
        dy = self.hy - self.ty
        if abs(dx) > 1 or abs(dy) > 1:
            if dx != 0:
                self.tx += dx // abs(dx)
            if dy != 0:
                self.ty += dy // abs(dy)
        self.visited.add((self.tx, self.ty))

    def run(self, lines):
        for line in lines:
            direction, number = line.split()
            dhx, dhy = DIRECTIONS[direction]
            for _ in range(int(number)):
                self.move(dhx, dhy)

def part1(lines):
    rope = Rope()
    rope.run(lines)
    return len(rope.visited)

def test_part1():
    assert part1(SAMPLE) == 13

if __name__ == "__main__":
    data = open("day09_input.txt").read().splitlines()
    print(f"Part 1: {part1(data)}")


class Knot:
    def __init__(self, next_knot=None):
        self.x = self.y = 0
        self.visited = {(0, 0)}
        self.next = next_knot

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.visited.add((self.x, self.y))
        if self.next:
            self.next.follow(self.x, self.y)

    def follow(self, kx, ky):
        dx = kx - self.x
        dy = ky - self.y
        if abs(dx) > 1 or abs(dy) > 1:
            if dx != 0:
                dx = dx // abs(dx)
            if dy != 0:
                dy = dy // abs(dy)
            self.move(dx, dy)


class Rope2:
    def __init__(self, length):
        knot = self.tail = Knot()
        for _ in range(length - 1):
            knot = Knot(knot)
        self.head = knot

    def run(self, lines):
        for line in lines:
            direction, number = line.split()
            dhx, dhy = DIRECTIONS[direction]
            for _ in range(int(number)):
                self.head.move(dhx, dhy)

def part2(lines, length=10):
    rope = Rope2(length)
    rope.run(lines)
    return len(rope.tail.visited)

def test_part2_as_1():
    assert part2(SAMPLE, 2) == 13

SAMPLE2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".splitlines()

@pytest.mark.parametrize(
    "lines, answer",
    [(SAMPLE, 1), (SAMPLE2, 36)]
)
def test_part2(lines, answer):
    assert part2(lines) == answer

if __name__ == "__main__":
    data = open("day09_input.txt").read().splitlines()
    print(f"Part 2: {part2(data)}")
