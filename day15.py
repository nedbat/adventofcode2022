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

def combine_ranges(r1, r2):
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
def test_combine_ranges(r1, r2, r3):
    assert combine_ranges(r1, r2) == r3

# A range list is a list of non-overlapping ranges.
def add_range_to_range_list(rset, r):
    result = [r]
    for rs in rset:
        overlapped = combine_ranges(result[0], rs)
        if overlapped is not None:
            result[0] = overlapped
        else:
            result.append(rs)
    return result


def covered_positions(sensor_data, row_num):
    covered = []
    for sx, sy, bx, by in sensor_data:
        radius = abs(sx - bx) + abs(sy - by)
        row_rad = radius - abs(sy - row_num)
        row_covered = range(sx - row_rad, sx + row_rad + 1)
        if row_rad >= 0:
            covered = add_range_to_range_list(covered, row_covered)
    return covered

def test_covered_positions():
    data = read_data(SAMPLE)
    covered = covered_positions(data, 10)
    assert covered == [range(-2, 25)]

def part1(text, row_num):
    data = read_data(text)
    covered = covered_positions(data, row_num)
    return sum(len(r) for r in covered) - 1

def test_part1():
    assert part1(SAMPLE, 10) == 26

if __name__ == "__main__":
    text = open("day15_input.txt").read()
    print(f"Part 1: {part1(text, 2_000_000)}")
