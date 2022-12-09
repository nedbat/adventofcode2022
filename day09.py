# https://adventofcode.com/2022/day/9

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
