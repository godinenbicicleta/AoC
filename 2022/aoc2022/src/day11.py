from dataclasses import dataclass
import re
from pathlib import Path
from typing import Callable


@dataclass
class Monkey:
    id: int
    items: [int]
    operation: Callable
    test: Callable
    dest: dict
    inspected: int

    def __repr__(self):
        return f"Monkey(id={self.id}, inspected={self.inspected})"


def parse(m: str) -> Monkey:
    global factors_prod
    lines = m.split("\n")
    id_ = int(re.findall(r'\d+', lines[0])[0])
    operation_parts = lines[2].split("= ")[-1].split(" ")

    def operation(old):
        op = operation_parts[1]
        left = old
        try:
            right = int(operation_parts[-1])
        except Exception:
            right = old
        if op == "*":
            return left * right
        if op == "+":
            return left + right
        raise ValueError("Invalid op %s, %s, %s", op, operation_parts, m)

    items = [int(k) for k in lines[1].split("items: ")[-1].split(", ")]

    def test(inp):
        return (inp % int(lines[3].split(" ")[-1]))
    factors_prod *= int(lines[3].split(" ")[-1])
    dest = {}
    dest[True] = int(lines[4].split(" ")[-1])
    dest[False] = int(lines[5].split(" ")[-1])
    return Monkey(id_, items, operation, test, dest, 0)


def setup():
    fname = Path(__file__).parent.absolute() / "../data/day11.txt"
    with open(fname) as f:
        data = f.read().strip().split("\n\n")
    monkeys = [parse(d) for d in data]
    return monkeys


def run(monkeys, op):
    for monkey in monkeys:
        items = monkey.items
        monkey.items = []
        monkey.inspected += len(items)
        for item in items:
            wl = monkey.operation(item)
            wl = op(wl)
            dest = monkey.dest[monkey.test(wl) == 0]
            monkeys[dest].items.append(wl)


def runs(rounds, monkeys, op):
    for i in range(rounds):
        run(monkeys, op)
    ms = sorted(monkeys, key=lambda x: x.inspected)[-2:]
    print(ms[0].inspected * ms[1].inspected)


if __name__ == "__main__":

    factors_prod = 1
    for n, op in zip([20, 10000], [lambda x: x // 3, lambda x: x % factors_prod]):
        monkeys = setup()
        runs(n, monkeys, op)
