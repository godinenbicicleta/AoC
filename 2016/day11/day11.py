import dataclasses
import re
import time
from collections import deque
from typing import Any, Tuple

input0 = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.""".strip()

input1 = """
The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip.
The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
The third floor contains a thulium-compatible microchip.
The fourth floor contains nothing relevant.""".strip()


input2 = """
The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip, an elerium generator, An elerium-compatible microchip, A dilithium generator, A dilithium-compatible microchip
The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
The third floor contains a thulium-compatible microchip.
The fourth floor contains nothing relevant.""".strip()

microchip_re = r"(\w+)-compatible\s+microchip"

generator_re = r"\s+(\w+)\s+generator"


@dataclasses.dataclass(frozen=True)
class Floor:
    microchips: tuple[str]
    generators: tuple[str]


@dataclasses.dataclass(frozen=True)
class State:
    floors: tuple[Floor]
    size: int
    moves: int
    prev: Any
    elevator: int

    @property
    def solved(self):
        return self.size == len(self.floors[-1].generators) + len(
            self.floors[-1].microchips
        )

    @property
    def state(self):
        def yield_floor_state():
            for floor in self.floors:
                yield tuple(sorted(floor.generators)), tuple(sorted(floor.microchips))

        return tuple(yield_floor_state()) + (self.elevator,)


def valid_floor(floor: Floor) -> bool:
    if not floor.generators:
        return True
    for m in floor.microchips:
        if m not in floor.generators:
            return False
    return True


def valid_state(s: State) -> bool:
    for f in s.floors:
        if not valid_floor(f):
            return False
    return True


def valid_move(microchips: list[str], generators: list[str]) -> bool:
    if not microchips and not generators:
        return False
    if microchips and not generators:
        return True
    if generators and not microchips:
        return True
    for microchip in microchips:
        if microchip not in generators:
            for generator in generators:
                if generator not in microchips:
                    return False
    return True


def gen_moves(
    microchips: list[str], generators: list[str]
) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    def run():
        for m in microchips:
            for g in generators:
                if m == g:
                    yield ((m,), (g,))
        yield from ((m, ()) for m in comb2(microchips))
        yield from (((), g) for g in comb2(generators))
        for m in microchips:
            yield ((m,), ())
        for g in generators:
            yield ((), (g,))

    res = list(filter(lambda x: valid_move(*x), run()))
    return res


def comb2(s):
    if not s:
        return []
    if len(s) < 2:
        return []
    if len(s) == 2:
        return [s]
    return [(s[0], k) for k in s[1:]] + comb2(s[1:])


def parse(inp: str) -> State:
    size = 0
    floors = []
    for line in inp.split("\n"):
        generators = re.findall(generator_re, line)
        size += len(generators)
        microchips = re.findall(microchip_re, line)
        size += len(microchips)
        floors.append(Floor(microchips=tuple(microchips), generators=tuple(generators)))
    return State(floors=floors, size=size, moves=0, prev=None, elevator=0)


def solve(p: State) -> State:
    seen = {p.state}
    next_states = deque([p])
    while next_states:
        s = next_states.popleft()
        i = s.elevator
        floor = s.floors[i]
        for ms, gs in gen_moves(floor.microchips, floor.generators):
            for index in i + 1, i - 1:
                if index < 0 or index >= len(s.floors):
                    continue
                up_floor = s.floors[index]
                new_ms = up_floor.microchips + ms
                new_gs = up_floor.generators + gs
                new_up_floor = Floor(microchips=new_ms, generators=new_gs)
                new_prev_floor = Floor(
                    microchips=tuple(i for i in floor.microchips if i not in ms),
                    generators=tuple(i for i in floor.generators if i not in gs),
                )
                new_floors = []
                for j in range(len(s.floors)):
                    if j == i:
                        new_floors.append(new_prev_floor)
                        continue
                    if j == index:
                        new_floors.append(new_up_floor)
                        continue
                    new_floors.append(s.floors[j])
                new_state = dataclasses.replace(
                    s, floors=new_floors, moves=s.moves + 1, prev=s, elevator=index
                )
                if new_state.solved:
                    print("solved", new_state.moves)
                    return new_state

                if valid_state(new_state) and new_state.state not in seen:
                    seen.add(new_state.state)
                    next_states.append(new_state)


def show(s: State):
    states = []
    prev = s
    while prev is not None:
        states.append(prev)
        prev = prev.prev

    states.reverse()
    for index, s in enumerate(states):
        print()
        print(f"State {index}, elevator={s.elevator}", "==" * 10)
        print()
        num_floors = len(s.floors)
        for i, floor in enumerate(s.floors[::-1], start=0):
            print(f"Floor {num_floors - i}", end="\t")
            print(floor.microchips, end="\t")
            print(floor.generators)
            print("--" * 10)


if __name__ == "__main__":

    for i in (input0, input1):
        t0 = time.time()
        solve(parse(i))
        print("elapsed_time", time.time() - t0)
