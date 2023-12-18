import heapq
from typing import Any, NamedTuple


class Pos(NamedTuple):
    heat: int
    x: int
    y: int
    conseq: int
    dir: str
    prev: Any = None

    def __lt__(self, other):
        return (self.heat, -self.x - self.y) < (other.heat, -other.x - other.y)

    @property
    def key(self):
        return (self.x, self.y, self.conseq, self.dir)


def is_valid(d1, d2):
    return not (
        (d1 == "^" and d2 == "v") or (d1 == "v" and d2 == "^") or (d1 == "<" and d2 == ">") or (d1 == ">" and d2 == "<")
    )


def get_conseq(current_c, current_dir, new_dir):
    if new_dir == current_dir:
        return current_c + 1
    return 1


def p1():
    return solve(filter1, -1, set())


def p2():
    return solve(filter2, 3, {})


def solve(filter_func, min_conseq, seen):
    with open("../data/day17.txt") as f:
        data = [list(map(int, (line.strip()))) for line in f]
    goal = (len(data[0]) - 1, len(data) - 1)

    queue = [
        Pos(heat=data[0][1], x=1, y=0, conseq=1, dir=">", prev=None),
        Pos(heat=data[1][0], x=0, y=1, conseq=1, dir="v", prev=None),
    ]

    if min_conseq == -1:
        seen.add(queue[0].key)
        seen.add(queue[0].key)
    else:
        seen[queue[0].key] = queue[0].heat
        seen[queue[1].key] = queue[1].heat

    heapq.heapify(queue)

    depth = 0
    while queue:
        current = heapq.heappop(queue)
        depth += 1
        if not queue:
            break

        if (current.x, current.y) == goal and current.conseq > min_conseq:
            print(current.heat, depth)
            break

        candidates = [
            (current.x + 1, current.y, ">"),
            (current.x - 1, current.y, "<"),
            (current.x, current.y + 1, "v"),
            (current.x, current.y - 1, "^"),
        ]

        candidates = [c for c in candidates if c[0] < len(data[0]) and c[1] < len(data) and c[0] >= 0 and c[1] >= 0]

        candidates = [
            Pos(
                x=candidate[0],
                y=candidate[1],
                heat=current.heat + data[candidate[1]][candidate[0]],
                conseq=get_conseq(current.conseq, current.dir, candidate[2]),
                dir=candidate[2],
                prev=current,
            )
            for candidate in candidates
        ]
        filtered = filter_func(current, candidates, seen)
        for c in filtered:
            heapq.heappush(queue, c)


def filter2(current, candidates, seen):
    filtered = []
    if current.conseq > 10:
        raise ValueError()
    candidates = [c for c in candidates if c.key not in seen or seen[c.key] >= c.heat]
    if current.conseq < 4:
        for c in candidates:
            if c.dir == current.dir:
                filtered.append(c)
    elif current.conseq == 10:
        for c in candidates:
            if c.dir != current.dir and is_valid(c.dir, current.dir):
                filtered.append(c)
    else:
        for c in candidates:
            if is_valid(c.dir, current.dir):
                filtered.append(c)
    for c in filtered:
        seen[c.key] = c.heat
    return filtered


def filter1(current, candidates, seen):
    candidates = [c for c in candidates if c.key not in seen]
    filtered = []
    if current.conseq == 3:
        for c in candidates:
            if c.dir != current.dir and is_valid(c.dir, current.dir):
                filtered.append(c)
    else:
        for c in candidates:
            if is_valid(c.dir, current.dir):
                filtered.append(c)
    for c in filtered:
        seen.add(c.key)
    return filtered


if __name__ == "__main__":
    p1()
    p2()
