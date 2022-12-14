# https://adventofcode.com/2022/day/15

import re

import pytest


SAMPLE = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

def read_data(text):
    return [
        tuple(map(int, re.findall(r"[-\d]+", line)))
        for line in text.splitlines()
    ]

def union_ranges(r1, r2):
    """If two ranges can be combined to one, return it, else None."""
    if r1.stop < r2.start or r2.stop < r1.start:
        return None     # No overlap
    return range(min(r1.start, r2.start), max(r1.stop, r2.stop))

@pytest.mark.parametrize("r1, r2, r3", [
    (range(0, 10), range(5, 15), range(0, 15)),
    (range(5, 15), range(0, 10), range(0, 15)),
    (range(0, 10), range(15, 25), None),
    (range(0, 10), range(11, 25), None),
    (range(0, 10), range(5, 8), range(0, 10)),
    (range(10, 20), range(5, 15), range(5, 20)),
])
def test_union_ranges(r1, r2, r3):
    assert union_ranges(r1, r2) == r3

def intersect_ranges(r1, r2):
    """Return the intersection of two ranges, None if empty."""
    if r1.stop < r2.start or r2.stop < r1.start:
        return None     # No overlap
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))

@pytest.mark.parametrize("r1, r2, r3", [
    (range(0, 10), range(5, 15), range(5, 10)),
    (range(5, 15), range(0, 10), range(5, 10)),
    (range(0, 10), range(15, 25), None),
    (range(0, 10), range(11, 25), None),
    (range(0, 10), range(5, 8), range(5, 8)),
    (range(10, 20), range(5, 15), range(10, 15)),
])
def test_intersect_ranges(r1, r2, r3):
    assert intersect_ranges(r1, r2) == r3


class Ranges:
    """A Ranges has a list of non-overlapping ranges."""
    def __init__(self, *ranges):
        self.ranges = list(ranges)

    def __eq__(self, other):
        # ignores order, but we only use it for 1-element ranges in our tests...
        return self.ranges == other.ranges

    def __or__(self, r):
        result = Ranges(r)
        for rs in self.ranges:
            overlapped = union_ranges(result.ranges[0], rs)
            if overlapped is not None:
                result.ranges[0] = overlapped
            else:
                result.ranges.append(rs)
        return result

    def __and__(self, r):
        result = Ranges()
        for rs in self.ranges:
            inter = intersect_ranges(r, rs)
            if inter is not None:
                result.ranges.append(inter)
        return result

    def __len__(self):
        return sum(len(r) for r in self.ranges)


def covered_positions(sensor_data, row_num):
    covered = Ranges()
    for sx, sy, bx, by in sensor_data:
        radius = abs(sx - bx) + abs(sy - by)
        row_rad = radius - abs(sy - row_num)
        if row_rad >= 0:
            row_covered = range(sx - row_rad, sx + row_rad + 1)
            covered |= row_covered
    return covered

def test_covered_positions():
    data = read_data(SAMPLE)
    covered = covered_positions(data, 10)
    assert covered == Ranges(range(-2, 25))

def part1(text, row_num):
    data = read_data(text)
    covered = covered_positions(data, row_num)
    return len(covered) - 1

def test_part1():
    assert part1(SAMPLE, 10) == 26

if __name__ == "__main__":
    text = open("day15_input.txt").read()
    print(f"Part 1: {part1(text, 2_000_000)}")

def only_possible(text, size):
    data = read_data(text)
    for row_num in range(size):
        covered = covered_positions(data, row_num)
        if len(covered.ranges) > 1:
            covered &= range(size)
            return next(r.stop for r in covered.ranges if r.start == 0), row_num

def test_only_possible():
    assert only_possible(SAMPLE, 20) == (14, 11)

def part2(text, size):
    x, y = only_possible(text, size)
    return x * 4_000_000 + y

def test_part2():
    assert part2(SAMPLE, 20) == 56_000_011

if __name__ == "__main__":
    text = open("day15_input.txt").read()
    print(f"Part 2: {part2(text, 4_000_000)}")

# Now 46s. I think a shortcut would be to examine the overlaps among diamonds,
# since the blank space must be at one of those intersections. But that seems
# like a lot of work..  :)
