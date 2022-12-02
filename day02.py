# https://adventofcode.com/2022/day/2

SAMPLE = """\
A Y
B X
C Z
""".splitlines()

rock, paper, scissors = range(3)

wins = {
    rock: scissors,
    paper: rock,
    scissors: paper,
}

loses = {v:k for k,v in wins.items()}

points = {
    rock: 1,
    paper: 2,
    scissors: 3,
}

part1_translation = {
    "A": rock,
    "B": paper,
    "C": scissors,
    "X": rock,
    "Y": paper,
    "Z": scissors,
}

def part1_score(guide_lines):
    score = 0
    for line in guide_lines:
        him, me = line.split()
        him = part1_translation[him]
        me = part1_translation[me]
        score += points[me]
        if wins[me] == him:
            score += 6
        elif me == him:
            score += 3
    return score

def test_part1():
    assert part1_score(SAMPLE) == 15

if __name__ == "__main__":
    score = part1_score(open("day02_input.txt"))
    print(f"Part 1: {score = }")


def part2_score(guide_lines):
    score = 0
    for line in guide_lines:
        him, me = line.split()
        him = part1_translation[him]
        if me == "X":
            # lose
            me = wins[him]
        elif me == "Y":
            # tie
            me = him
            score += 3
        else:
            # win
            me = loses[him]
            score += 6
        score += points[me]
    return score

def test_part2():
    assert part2_score(SAMPLE) == 12

if __name__ == "__main__":
    score = part2_score(open("day02_input.txt"))
    print(f"Part 2: {score = }")
