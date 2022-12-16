# https://adventofcode.com/2022/day/16

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

        # if the current valve is closed, open it, if it's more than zero.
        if self.valve not in self.opened and self.valve in cave.valves:
            yield State(
                self.valve,
                self.opened | {self.valve},
                self.pressure + pressure_incr,
                self.minutes + 1,
                #self.trail + f"open {self.valve}; ",
            )

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
            # move to all adjacent valves.
            for next_valve in cave.pipes[self.valve]:
                yield State(
                    next_valve,
                    self.opened,
                    self.pressure + pressure_incr,
                    self.minutes + 1,
                    #self.trail + f"move to {next_valve}; ",
                )


def search(cave):
    state0 = State()
    states = [state0]
    visited = {state0: state0}
    best = 0
    while True:
        #print(len(states),len(visited))
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
                else:
                    if new_state:
                        next_states.append(ns)
        if not next_states:
            return best
        states = next_states

def test_search():
    assert search(Cave.from_text(SAMPLE)) == 1651

if __name__ == "__main__":
    cave = Cave.from_text(open("day16_input.txt").read())
    print(f"Part 1: {search(cave)}")
