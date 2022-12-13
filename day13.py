# https://adventofcode.com/2022/day/13

import ast
import itertools

SAMPLE = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

def read_pairs(text):
    pairs = []
    for two in text.split("\n\n"):
        pairs.append(tuple(map(ast.literal_eval, two.strip().split("\n"))))
    return pairs

def test_read_pairs():
    pairs = read_pairs(SAMPLE)
    assert pairs[0] == ([1,1,3,1,1], [1,1,5,1,1])
    assert pairs[6] == ([[[]]], [[]])
    assert pairs[7] == (
        [1,[2,[3,[4,[5,6,7]]]],8,9],
        [1,[2,[3,[4,[5,6,0]]]],8,9],
    )

def compare(a, b):
    match a, b:
        case int(), int():
            return (b < a) - (a < b)
        case list(), int():
            return compare(a, [b])
        case int(), list():
            return compare([a], b)
        case list(), list():
            for aa, bb in itertools.zip_longest(a, b):
                if aa is None:
                    return -1
                elif bb is None:
                    return 1
                else:
                    cmp = compare(aa, bb)
                    if cmp != 0:
                        return cmp
            return 0

def test_compare():
    pairs = read_pairs(SAMPLE)
    cmps = [compare(a, b) for a, b in pairs]
    assert cmps == [-1, -1, 1, -1, 1, -1, 1, 1]

def part1(text):
    return sum(i for i, pair in enumerate(read_pairs(text), start=1) if compare(*pair) == -1)

def test_part1():
    assert part1(SAMPLE) == 13

if __name__ == "__main__":
    text = open("day13_input.txt").read()
    print(f"Part 1: {part1(text)}")
