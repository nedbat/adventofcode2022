# https://adventofcode.com/2022/day/12

from dataclasses import dataclass, field

import astar

SAMPLE = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def taxi_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def neighbors(self):
        yield Point(self.x - 1, self.y)
        yield Point(self.x, self.y - 1)
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y + 1)

@dataclass
class Map:
    map: dict[Point, int] = field(default_factory=dict)
    start: Point = Point(0, 0)
    goal: Point = Point(0, 0)

    @classmethod
    def from_text(cls, text):
        map = cls()
        for y, line in enumerate(text.splitlines()):
            for x, ch in enumerate(line):
                if ch == "S":
                    map.start = Point(x, y)
                    ch = "a"
                elif ch == "E":
                    map.goal = Point(x, y)
                    ch = "z"
                map.map[Point(x, y)] = ord(ch)
        return map


def test_parsing():
    map = Map.from_text(SAMPLE)
    assert map.start == Point(0, 0)
    assert map.goal == Point(5, 2)
    assert map.map[Point(0, 4)] == ord("a")


class ClimbState(astar.State):
    def __init__(self, map, pt):
        self.map = map
        self.pt = pt

    @classmethod
    def first(cls, map):
        return cls(map, map.start)

    def __hash__(self):
        return hash(self.pt)

    def __eq__(self, other):
        return self.pt == other.pt

    def is_goal(self):
        return self.pt == self.map.goal

    def next_states(self, cost):
        my_height = self.map.map[self.pt]
        for npt in self.pt.neighbors():
            dest_height = self.map.map.get(npt)
            if dest_height is not None:
                if dest_height - my_height <= 1:
                    yield ClimbState(self.map, npt), cost + 1

    def guess_completion_cost(self):
        return self.pt.taxi_distance(self.map.goal)

def part1(text):
    map = Map.from_text(text)
    best, cost = astar.search(ClimbState.first(map))
    return cost

def test_part1():
    assert part1(SAMPLE) == 31

if __name__ == "__main__":
    text = open("day12_input.txt").read()
    print(f"Part 1: {part1(text)}")
