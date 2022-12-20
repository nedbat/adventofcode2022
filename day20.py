# https://adventofcode.com/2022/day/20

SAMPLE = """\
1
2
-3
3
-2
0
4
"""

class Num:
    def __init__(self, n):
        self.n = int(n)

    def __int__(self):
        return self.n

    def __lt__(self, other):
        return self.n < other

    def __radd__(self, other):
        return self.n + other


def test_num():
    na = Num(1)
    nb = Num(1)
    nums = [na, nb]
    assert nums.index(na) == 0
    assert nums.index(nb) == 1
    assert nums.pop(1) is nb

def read_numbers(text):
    nums = list(map(Num, text.split()))
    assert len(set(nums)) == len(nums)
    return nums

def mix(numbers):
    original = list(numbers)
    for num in original:
        i = numbers.index(num)
        new_i = (i + num) % len(numbers)
        if num < 0:
            new_i -= 1
        numbers.pop(i)
        numbers.insert(new_i, num)

def test_mix():
    numbers = read_numbers(SAMPLE)
    mix(numbers)
    assert list(map(int, numbers)) == [1, 2, -3, 4, 0, 3, -2]

def grove_coordinates(numbers):
    i0 = next(i for i, n in enumerate(numbers) if int(n) == 0)
    return sum(numbers[(i0 + i) % len(numbers)] for i in [1000, 2000, 3000])

def part1(text):
    numbers = read_numbers(text)
    mix(numbers)
    return grove_coordinates(numbers)

def test_part1():
    assert part1(SAMPLE) == 3

if __name__ == "__main__":
    text = open("day20_input.txt").read()
    print(f"Part 1: {part1(text)}")
