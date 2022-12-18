# https://adventofcode.com/2022/day/18

import re

SAMPLE = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

def neighbors(x, y, z):
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)

def read_cubes(text):
    cubes = set()
    for line in text.splitlines():
        cubes.add(tuple(map(int, re.findall(r"\d+", line))))
    return cubes

def exposed_sides(cubes):
    exposed = 0
    for pt in cubes:
        for npt in neighbors(*pt):
            if npt not in cubes:
                exposed += 1
    return exposed

def part1(text):
    return exposed_sides(read_cubes(text))

def test_part1():
    assert part1(SAMPLE) == 64

if __name__ == "__main__":
    text = open("day18_input.txt").read()
    print(f"Part 1: {part1(text)}")


def range2d_incl(la, ha, lb, hb):
    for a in range(la, ha + 1):
        for b in range(lb, hb + 1):
            yield a, b

def exterior(cubes):
    lx = min(x for x, _, _ in cubes)
    ly = min(y for _, y, _ in cubes)
    lz = min(z for _, _, z in cubes)
    hx = max(x for x, _, _ in cubes)
    hy = max(y for _, y, _ in cubes)
    hz = max(z for _, _, z in cubes)

    # add a skin around the whole grid of outside cubes
    outside = set()
    candidates = set()
    for y, z in range2d_incl(ly, hy, lz, hz):
        outside.add((lx-1, y, z))
        outside.add((hx+1, y, z))
        candidates.add((lx, y, z))
        candidates.add((hx, y, z))
    for x, z in range2d_incl(lx, hx, lz, hz):
        outside.add((x, ly-1, z))
        outside.add((x, hy+1, z))
        candidates.add((x, ly, z))
        candidates.add((x, hy, z))
    for x, y in range2d_incl(lx, hx, ly, hy):
        outside.add((x, y, lz-1))
        outside.add((x, y, hz+1))
        candidates.add((x, y, lz))
        candidates.add((x, y, hz))

    while True:
        next_candidates = set()
        for cand in candidates:
            if cand in cubes:
                continue
            if cand in outside:
                continue
            for ncand in neighbors(*cand):
                if ncand in outside:
                    outside.add(cand)
                elif ncand not in cubes:
                    next_candidates.add(ncand)
        if not next_candidates:
            break
        candidates = next_candidates

    exposed = 0
    for pt in cubes:
        for npt in neighbors(*pt):
            if npt in outside:
                exposed += 1
    return exposed

def part2(text):
    return exterior(read_cubes(text))

def test_part2():
    assert part2(SAMPLE) == 58

if __name__ == "__main__":
    text = open("day18_input.txt").read()
    print(f"Part 2: {part2(text)}")
