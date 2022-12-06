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


def part1(buffer):
    last4 = collections.deque(maxlen=4)
    for i, c in enumerate(buffer):
        last4.append(c)
        if len(last4) == 4 and len(set(last4)) == 4:
            return i + 1

@pytest.mark.parametrize("buffer, answer", SAMPLES)
def test_part1(buffer, answer):
    assert part1(buffer) == answer


if __name__ == "__main__":
    data = open("day06_input.txt").read().strip()
    print(f"Part 1: {part1(data)}")
