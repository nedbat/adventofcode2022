# https://adventofcode.com/2022/day/5

import re

SAMPLE = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".splitlines()

def read_input(lines):
    line_iter = iter(lines)
    stack_lines = []
    for line in line_iter:
        if "[" in line:
            stack_lines.append(line)
        else:
            break

    num_stacks = len(line.split())
    stacks = [[] for _ in range(num_stacks)]

    for stack_line in reversed(stack_lines):
        for col_num in range(num_stacks):
            col_ch = col_num * 4 + 1
            if col_ch < len(stack_line):
                ch = stack_line[col_ch]
                if ch.strip():
                    stacks[col_num].append(ch)

    line = next(line_iter)
    assert not line.strip()

    moves = []
    for line in line_iter:
        moves.append(tuple(map(int, re.findall(r"\d+", line))))

    return stacks, moves

def test_read_input():
    assert read_input(SAMPLE) == (
        [["Z", "N"], ["M", "C", "D"], ["P"]],
        [(1,2,1), (3,1,3), (2,2,1), (1,1,2)],
    )

def move_crates(crates, moves):
    for num, src, dst in moves:
        for _ in range(num):
            crates[dst-1].append(crates[src-1].pop())

def test_move_crates():
    crates, moves = read_input(SAMPLE)
    move_crates(crates, moves)
    assert crates == [["C"], ["M"], ["P", "D", "N", "Z"]]

def part1(lines):
    crates, moves = read_input(lines)
    move_crates(crates, moves)
    return "".join(stack[-1] for stack in crates)

def test_part1():
    assert part1(SAMPLE) == "CMZ"

if __name__ == "__main__":
    lines = open("day05_input.txt").read().splitlines()
    print(f"Part 1: {part1(lines)}")
