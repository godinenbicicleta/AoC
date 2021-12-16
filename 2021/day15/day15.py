import dataclasses
import fileinput
import time
from heapq import heappop, heappush
from typing import List, Tuple

grid = []
for line in fileinput.input():
    grid.append(list(map(int, list(line.strip()))))


def print_grid():
    for row in grid:
        print("".join(map(str, row)))


print_grid()


def finished(x, y):
    return x == len(grid[0]) - 1 and y == len(grid) - 1


def risk(x, y):
    return grid[y][x]


def ns(x, y):
    for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if i >= 0 and i < len(grid[0]) and j >= 0 and j < len(grid):
            yield i, j


def print_path(path):
    print()
    for j, row in enumerate(grid):
        for i, v in enumerate(row):
            if (i, j) in path.path:
                print(v, end="")
            else:
                print(".", end="")
        print()


@dataclasses.dataclass
class Path:
    risk: int
    path: List[Tuple[int, int]]

    def __lt__(self, other):
        return self.risk < other.risk


# risk, x, y
@dataclasses.dataclass
class Node:
    p: Tuple[int, int]
    r: int

    def __eq__(self, other):
        return self.p == other.p

    def __hash__(self):
        return hash(self.p)

    def __lt__(self, other):
        return self.r < other.r


def run2():
    dist = {}
    seen = set()
    nodes = [Node((0, 0), 0)]
    while nodes:
        node = heappop(nodes)
        seen.add(node)
        x, y = node.p
        if finished(x, y):
            return node

        for i, j in ns(x, y):
            r = risk(i, j)
            n = Node((i, j), r + node.r)
            if n in seen:
                continue
            if n not in dist:
                dist[n] = n.r
            elif n in dist and dist[n] <= n.r:
                continue
            else:
                dist[n] = n.r
            heappush(nodes, n)


def run():
    seen = set()
    paths = [Path(0, [(0, 0)])]
    lowPath = None

    while True:
        path = heappop(paths)
        x, y = path.path[-1]
        if finished(x, y):
            lowPath = path
            break
        for i, j in ns(x, y):
            p = (i, j)
            r = risk(i, j)
            if p in seen:
                continue
            seen.add(p)
            newPath = Path(path.risk + r, path.path + [(i, j)])
            heappush(paths, newPath)
    return lowPath


t0 = time.time()
p1 = run()
print(time.time() - t0)
print(p1.risk)
t0 = time.time()
print(run2())
print(time.time() - t0)

print_path(p1)
bigGrid = [[None for _ in range(len(grid[0]) * 5)] for _ in range(len(grid) * 5)]
dimX = len(grid[0]) - 1
dimY = len(grid) - 1
for j, row in enumerate(bigGrid):
    for i, _ in enumerate(row):
        x, y = i, j
        if j <= dimY and i <= dimX:
            bigGrid[j][i] = grid[j][i]
            continue
        if j > dimY and i <= dimX:
            y = j - dimY - 1
        if i > dimX:
            x = i - dimX - 1

        val = bigGrid[y][x] + 1
        val = val if val < 10 else 1
        bigGrid[j][i] = val
grid = bigGrid
t0 = time.time()
p2 = run()
print(p2.risk)
print(time.time() - t0)
t0 = time.time()
print(run2())
print(time.time() - t0)
