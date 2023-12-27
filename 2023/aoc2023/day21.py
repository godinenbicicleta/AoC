from typing import Sequence

with open("data/day21.txt") as f:
    grid = [d.strip().split() for d in f.readlines()]

grid = [i for j in grid for i in j]


def getS(g) -> tuple[int, int]:
    for y, row in enumerate(g):
        for x, v in enumerate(row):
            if v == "S":
                return x, y
    raise ValueError


start: tuple[int, int] = getS(grid)
dimx = len(grid[0])
dimy = len(grid)


def rescale1(x, dim):
    if x >= 0:
        return x % dim
    temp = dim - (abs(x) % dim)
    return temp % dim


def rescale(x, y):
    x = rescale1(x, dimx)
    y = rescale1(y, dimy)
    return x, y


def moves(i, j):
    for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        sx, sy = rescale(x, y)
        if grid[sy][sx] != "#":
            yield x, y


def renderPoints(ps):
    if not ps:
        print()
        return
    minx = min(0, min(p[0] for p in ps))
    maxx = max(dimx - 1, max(p[0] for p in ps))
    miny = min(0, min(p[1] for p in ps))
    maxy = max(dimy - 1, max(p[1] for p in ps))
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            sx, sy = rescale(x, y)
            if grid[sy][sx] == "#":
                print("#", end="")
            elif x == 5 and y == 5:
                print("S", end="")
            elif (x, y) in ps:
                print("O", end="")
            else:
                print(".", end="")
        print()


def p1():
    maxsteps = 64

    total = 1
    steps = 0
    prev = set()
    queue: Sequence[tuple[int, int]] = [start]

    while steps < maxsteps:
        steps += 1
        candidates = set()
        for p in queue:
            for c in moves(p[0], p[1]):
                if c not in prev:
                    candidates.add(c)
        if steps % 2 == 0:
            total += len(candidates)
        prev = set(queue)
        queue = sorted(candidates)

    print(total)


def p2():
    maxsteps = 1000

    total = 0
    steps = 0
    prev = set()
    queue: Sequence[tuple[int, int]] = [start]

    deltas = []
    totals = []
    while steps < maxsteps:
        steps += 1
        candidates = set()
        for p in queue:
            for c in moves(p[0], p[1]):
                if c not in prev:
                    candidates.add(c)
        if steps % 2 == 1:
            total += len(candidates)
            deltas.append(len(candidates))
            totals.append(total)
        prev = set(queue)
        queue = sorted(candidates)

    deltas1 = list(deltas[200 + 1 : 200 + 131 + 1])
    deltas2 = list(deltas[200 + 131 + 1 : 200 + 131 + 131 + 1])

    dds = [a - b for a, b in zip(deltas2, deltas1)]

    total = totals[200]
    deltaindex = 0
    for _ in range(200, 26501365 // 2):
        total += deltas1[deltaindex % 131]
        deltas1[deltaindex % 131] += dds[deltaindex % 131]
        deltaindex += 1

    print(total)


if __name__ == "__main__":
    p1()
    p2()
