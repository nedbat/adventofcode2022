# https://adventofcode.com/2022/day/10

import itertools

SAMPLE = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".splitlines()

def run(lines):
    x = 1
    cycles = iter(itertools.count(start=1))
    for line in lines:
        match line.split():
            case ["addx", n]:
                yield next(cycles), x
                yield next(cycles), x
                x += int(n)
            case ["noop"]:
                yield next(cycles), x
            case _:
                raise Exception(f"What? {line=}")

def signal_strengths(lines):
    for cycle, x in run(lines):
        if cycle in range(20, 221, 40):
            yield cycle * x

def test_signal_strengths():
    assert list(signal_strengths(SAMPLE)) == [420, 1140, 1800, 2940, 2880, 3960]

def part1(lines):
    return sum(signal_strengths(lines))

def test_part1():
    assert part1(SAMPLE) == 13140

if __name__ == "__main__":
    lines = open("day10_input.txt").read().splitlines()
    print(f"Part 1: {part1(lines)}")


def crt(lines):
    signal = iter(run(lines))
    for row in range(6):
        crt_row = ""
        for pixel_x in range(40):
            _, x = next(signal)
            if abs(x - pixel_x) <= 1:
                crt_row += "#"
            else:
                crt_row += "."
        yield crt_row

def test_crt():
    assert list(crt(SAMPLE)) == [
        "##..##..##..##..##..##..##..##..##..##..",
        "###...###...###...###...###...###...###.",
        "####....####....####....####....####....",
        "#####.....#####.....#####.....#####.....",
        "######......######......######......####",
        "#######.......#######.......#######.....",
    ]

if __name__ == "__main__":
    lines = open("day10_input.txt").read().splitlines()
    print("Part 2:")
    for crt_row in crt(lines):
        print(crt_row)
