# https://adventofcode.com/2022/day/16

import itertools
import re
from dataclasses import dataclass, field


SAMPLE = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

@dataclass
class Cave:
    valves: dict[str, int] = field(default_factory=dict)
    pipes: dict[str, list[str]] = field(default_factory=dict)

    @classmethod
    def from_text(cls, text):
        cave = cls()
        for line in text.splitlines():
            m = re.fullmatch(r"Valve (..) .*=(\d+); .* valves? (.*)", line)
            if m:
                valve = m[1]
                if m[2] != "0":
                    cave.valves[valve] = int(m[2])
                cave.pipes[valve] = m[3].split(", ")
        return cave

def test_from_text():
    cave = Cave.from_text(SAMPLE)
    assert len(cave.valves) == 6
    assert cave.valves["DD"] == 20
    assert cave.pipes["DD"] == ["CC", "AA", "EE"]


@dataclass(frozen=True)
class State:
    valve: str = "AA"
    opened: frozenset = frozenset()
    pressure: int = field(default=0, compare=False)
    minutes: int = field(default=0, compare=False)
    #trail: str = field(default="", compare=False)

    def moves(self, cave):
        pressure_incr = sum(cave.valves[v] for v in self.opened)

        # check if all the valves are opened.
        if len(cave.valves) == len(self.opened):
            # If all the valves are opened, sit tight and wait.
            yield State(
                self.valve,
                self.opened,
                self.pressure + (30 - self.minutes) * pressure_incr,
                30,
                #self.trail + f"wait {30 - self.minutes}",
            )
        else:
            # if the current valve is closed, open it, if it's more than zero.
            if self.valve not in self.opened and self.valve in cave.valves:
                yield State(
                    self.valve,
                    self.opened | {self.valve},
                    self.pressure + pressure_incr,
                    self.minutes + 1,
                    #self.trail + f"open {self.valve}; ",
                )

            # move to all adjacent valves.
            for next_valve in cave.pipes[self.valve]:
                yield State(
                    next_valve,
                    self.opened,
                    self.pressure + pressure_incr,
                    self.minutes + 1,
                    #self.trail + f"move to {next_valve}; ",
                )


def search(cave, state0):
    states = [state0]
    visited = {state0: state0}
    best = 0
    #best_trail = None
    while True:
        print(f"{len(states):12,d};  {len(visited):12,d}")
        next_states = []
        for s in states:
            for ns in s.moves(cave):
                prev = visited.get(ns)
                new_state = (
                    prev is None or
                    ns.minutes < prev.minutes or
                    ns.pressure > prev.pressure
                )
                if new_state:
                    visited[ns] = ns

                if ns.minutes == 30:
                    if ns.pressure > best:
                        #print(f"{ns.pressure}: {ns.trail}")
                        best = ns.pressure
                        #best_trail = ns.trail
                else:
                    if new_state:
                        next_states.append(ns)
        if not next_states:
            #print(best_trail)
            return best
        states = next_states

def part1(text):
    return search(Cave.from_text(text), State())

def test_part1():
    assert part1(SAMPLE) == 1651

if __name__ == "__main__":
    text = open("day16_input.txt").read()
    print(f"Part 1: {part1(text)}")


@dataclass(frozen=True)
class State2:
    you: str = "AA"
    elephant: str = "AA"
    opened: frozenset = frozenset()
    pressure: int = field(default=0, compare=False)
    minutes: int = field(default=4, compare=False)

    def steps(self, cave, valve):
        """Yield pairs (new position, valve to open)"""
        if valve not in self.opened and valve in cave.valves:
            yield valve, valve
        for next_valve in cave.pipes[valve]:
            yield next_valve, None

    def moves(self, cave):
        pressure_incr = sum(cave.valves[v] for v in self.opened)

        if len(cave.valves) == len(self.opened):
            # If all the valves are opened, sit tight and wait.
            yield State2(
                self.you,
                self.elephant,
                self.opened,
                self.pressure + (30 - self.minutes) * pressure_incr,
                30,
            )
        else:
            you_moves = list(self.steps(cave, self.you))
            ele_moves = list(self.steps(cave, self.elephant))

            for (new_you, you_open), (new_ele, ele_open) in itertools.product(you_moves, ele_moves):
                # if you_open == ele_open:
                #     continue
                new_opened = frozenset(self.opened)
                if you_open is not None:
                    new_opened |= {you_open}
                if ele_open is not None:
                    new_opened |= {ele_open}

                yield State2(
                    new_you,
                    new_ele,
                    new_opened,
                    self.pressure + pressure_incr,
                    self.minutes + 1,
                )

def part2(text):
    return search(Cave.from_text(text), State2())

def test_part2():
    assert part2(SAMPLE) == 1707

if __name__ == "__main__":
    text = open("day16_input.txt").read()
    print(f"Part 2: {part2(text)}")
