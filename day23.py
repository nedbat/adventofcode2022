# https://adventofcode.com/2022/day/23

import collections
import itertools


SAMPLE = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""

SAMPLE2 = """\
.....
..##.
..#..
.....
..##.
.....
"""

def read_elves(text):
    elves = set()
    for y, line in enumerate(text.splitlines()):
        for x, ch in enumerate(line.strip()):
            if ch == "#":
                elves.add((x, y))
    return elves

def empty_squares(elves):
    minx = min(x for x, _ in elves)
    maxx = max(x for x, _ in elves)
    miny = min(y for _, y in elves)
    maxy = max(y for _, y in elves)

    rectw = maxx - minx + 1
    recth = maxy - miny + 1
    return (rectw * recth) - len(elves)

def draw_elves(elves):
    minx = min(x for x, _ in elves)
    maxx = max(x for x, _ in elves)
    miny = min(y for _, y in elves)
    maxy = max(y for _, y in elves)

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print("#" if (x, y) in elves else ".", end="")
        print()

def test_empty_squares():
    assert empty_squares(read_elves(SAMPLE)) == 27


def neighbors(x, y):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == dy == 0:
                continue
            yield (x + dx, y + dy)


LOOKS = [
    ([(0, -1), (-1, -1), (1, -1)], (0, -1)),
    ([(0,  1), (-1,  1), (1,  1)], (0,  1)),
    ([(-1, 0), (-1, -1), (-1, 1)], (-1, 0)),
    ([(1,  0), (1,  -1), (1,  1)], (1,  0)),
]

def looks(nround):
    modlook = nround % 4
    for i in range(modlook, modlook + 4):
        yield LOOKS[i % 4]

def do_round(elves, nround):
    moves = {}
    for x, y in elves:
        if not any(npos in elves for npos in neighbors(x, y)):
            # No adjacent elf: don't move
            moves[(x, y)] = (x, y)
        else:
            for other_three, (mx, my) in looks(nround):
                for dx, dy in other_three:
                    if (x + dx, y + dy) in elves:
                        break
                else:
                    moves[(x, y)] = (x + mx, y + my)
                    break
            else:
                moves[(x, y)] = (x, y)

    elf_per_move = collections.Counter(moves.values())

    new_elves = set()
    for x, y in elves:
        nx, ny = moves[(x, y)]
        if elf_per_move[nx, ny] == 1:
            new_elves.add((nx, ny))
        else:
            new_elves.add((x, y))

    return new_elves

def do_rounds(elves, nrounds):
    for nround in range(nrounds):
        elves = do_round(elves, nround)
    return elves

def part1(text):
    elves = read_elves(text)
    elves = do_rounds(elves, 10)
    return empty_squares(elves)

def test_part1():
    assert part1(SAMPLE) == 110

if __name__ == "__main__":
    text = open("day23_input.txt").read()
    print(f"Part 1: {part1(text)}")

def do_rounds_until_stable(elves):
    for nround in itertools.count():
        next_elves = do_round(elves, nround)
        if next_elves == elves:
            return nround + 1
        elves = next_elves

def part2(text):
    elves = read_elves(text)
    return do_rounds_until_stable(elves)

def test_part2():
    assert part2(SAMPLE) == 20

if __name__ == "__main__":
    text = open("day23_input.txt").read()
    print(f"Part 2: {part2(text)}")
