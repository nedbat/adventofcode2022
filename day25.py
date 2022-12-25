# https://adventofcode.com/2022/day/25

import pytest

TESTS = [
(        1,              "1"),
(        2,              "2"),
(        3,             "1="),
(        4,             "1-"),
(        5,             "10"),
(        6,             "11"),
(        7,             "12"),
(        8,             "2="),
(        9,             "2-"),
(       10,             "20"),
(       15,            "1=0"),
(       20,            "1-0"),
(     2022,         "1=11-2"),
(    12345,        "1-0---0"),
(314159265,  "1121-1110-1=0"),
]

DIGITS = {
    "0": 0,
    "1": 1,
    "2": 2,
    "-": -1,
    "=": -2,
}

def from_snafu(snafu):
    num = 0
    place = 1
    for c in snafu:
        num *= 5
        num += DIGITS[c]
    return num

@pytest.mark.parametrize("num, snafu", TESTS)
def test_from_snafu(num, snafu):
    assert from_snafu(snafu) == num

TO_DIGITS = {
    0: ("0", 0),
    1: ("1", 0),
    2: ("2", 0),
    3: ("=", 5),
    4: ("-", 5),
}

def to_snafu(num):
    snafu = ""
    while num > 0:
        num_digit = num % 5
        digit, add = TO_DIGITS[num_digit]
        snafu = digit + snafu
        num = (num + add) // 5
    return snafu

@pytest.mark.parametrize("num, snafu", TESTS)
def test_to_snafu(num, snafu):
    assert to_snafu(num) == snafu

SAMPLE = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

def part1(text):
    return to_snafu(sum(from_snafu(s) for s in text.splitlines()))

def test_part1():
    assert part1(SAMPLE) == "2=-1=0"

if __name__ == "__main__":
    text = open("day25_input.txt").read()
    print(f"Part 1: {part1(text)}")
