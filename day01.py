# https://adventofcode.com/2022/day/1

def read_calories(fname):
    cals = []
    with open(fname) as fin:
        text = fin.read()
    elves = text.split("\n\n")
    cals = [list(map(int, elf.split())) for elf in elves]
    return cals

def highest_calories(cals):
    return max(map(sum, cals))

def test_part_1():
    assert highest_calories(read_calories("day01_sample.txt")) == 24000

if __name__ == "__main__":
    highest = highest_calories(read_calories("day01_input.txt"))
    print(f"Part 1: {highest}")
