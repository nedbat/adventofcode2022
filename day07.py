# https://adventofcode.com/2022/day/7

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

import pytest


SAMPLE = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".splitlines()


@dataclass
class Dir:
    parent: Optional[Dir]
    name: str
    dirs: dict[str, Dir] = field(default_factory=dict)
    files: dict[int] = field(default_factory=dict)

    def total_size(self):
        return sum(self.files.values()) + sum(d.total_size() for d in self.dirs.values())

    def __getitem__(self, name):
        here, _, more = name.partition("/")
        d = self.dirs[here]
        if more:
            d = d[more]
        return d

    def print(self, indent=""):
        print(f"{indent}- {self.name}")
        for d in self.dirs.values():
            d.print(indent + "  ")
        for name, size in self.files.items():
            print(f"{indent}  - {name}: {size}")

    def walk_dirs(self):
        for name, subdir in self.dirs.items():
            yield name, subdir
            for sname, ssubdir in subdir.walk_dirs():
                yield f"{name}/{sname}", ssubdir


class RegexMatcher:
    def __init__(self, text):
        self.text = text
        self.m = None

    def __eq__(self, pattern):
        self.m = re.fullmatch(pattern, self.text)
        return bool(self.m)

    def __getitem__(self, num):
        return self.m[num]

def read_terminal_output(lines):
    root = Dir(parent=None, name="")

    cwd = root
    for line in lines:
        match m := RegexMatcher(line):
            case r"\$ cd ..":
                cwd = cwd.parent
            case r"\$ cd /":
                cwd = root
            case r"\$ cd (\w+)":
                cwd = cwd.dirs[m[1]]
            case r"\$ ls":
                pass
            case r"dir (\w+)":
                cwd.dirs[m[1]] = Dir(cwd, m[1])
            case r"(\d+) ([.\w]+)":
                cwd.files[m[2]] = int(m[1])
            case _:
                raise ValueError(f"Don't understand {line=}")

    return root


@pytest.mark.parametrize("name, size", [
    ("a/e", 584),
    ("a", 94853),
    ("d", 24933642),
])
def test_sizes(name, size):
    filesys = read_terminal_output(SAMPLE)
    assert filesys[name].total_size() == size

def part1(lines):
    filesys = read_terminal_output(lines)
    big_sum = 0
    for _, subdir in filesys.walk_dirs():
        size = subdir.total_size()
        if size <= 100_000:
            big_sum += size
    return big_sum

def test_part1():
    assert part1(SAMPLE) == 95437

if __name__ == "__main__":
    lines = open("day07_input.txt").read().splitlines()
    print(f"Part 1: {part1(lines)}")
