# https://adventofcode.com/2022/day/6

import collections

import pytest

SAMPLES = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
]


def first_distinct(buffer, num):
    recent = collections.deque(maxlen=num)
    for i, c in enumerate(buffer):
        recent.append(c)
        if len(recent) == num and len(set(recent)) == num:
            return i + 1

def part1(buffer):
    return first_distinct(buffer, 4)

@pytest.mark.parametrize("buffer, answer", SAMPLES)
def test_part1(buffer, answer):
    assert part1(buffer) == answer


if __name__ == "__main__":
    data = open("day06_input.txt").read().strip()
    print(f"Part 1: {part1(data)}")


SAMPLES2 = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
]

def part2(buffer):
    return first_distinct(buffer, 14)

@pytest.mark.parametrize("buffer, answer", SAMPLES2)
def test_part2(buffer, answer):
    assert part2(buffer) == answer

if __name__ == "__main__":
    data = open("day06_input.txt").read().strip()
    print(f"Part 2: {part2(data)}")
