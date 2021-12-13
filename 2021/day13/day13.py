import sys
from collections import defaultdict
from typing import NamedTuple

with open(sys.argv[1]) as f:
    data = f.read()


def min_max(grid):
    sortedx = sorted((p[0] for p, v in grid.items() if v == "#"))
    sortedy = sorted((p[1] for p, v in grid.items() if v == "#"))
    minx, maxx = sortedx[0], sortedx[-1]
    miny, maxy = sortedy[0], sortedy[-1]
    return (minx, maxx), (miny, maxy)


def print_grid(grid):
    (minx, maxx), (miny, maxy) = min_max(grid)
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print(grid[(x, y)], end="")
        print()
    print()


raw_dots, raw_folds = data.strip().split("\n\n")
grid = defaultdict(lambda: " ")
folds = []

for dot_line in raw_dots.strip().split("\n"):
    x, y = dot_line.split(",")
    x, y = int(x), int(y)
    grid[(x, y)] = "#"


class Fold(NamedTuple):
    axis: str
    value: int


for fold in raw_folds.strip().split("\n"):
    axis = "y" if "y" in fold else "x"
    value = int(fold.split(f"{axis}=")[-1])

    folds.append(Fold(axis=axis, value=value))


def apply(fold, grid):
    (minx, maxx), (miny, maxy) = min_max(grid)
    if fold.axis == "y":
        for j, y in enumerate(range(fold.value + 1, maxy + 1)):
            for x in range(minx, maxx + 1):
                if grid[(x, y)] == " ":
                    continue
                grid[(x, fold.value - j - 1)] = grid[(x, y)]
                grid[(x, y)] = " "

    elif fold.axis == "x":
        for i, x in enumerate(range(fold.value + 1, maxx + 1)):
            for y in range(miny, maxy + 1):
                if grid[(x, y)] == " ":
                    continue
                grid[(fold.value - i - 1), y] = grid[(x, y)]
                grid[(x, y)] = " "


def count(grid):
    return sum(1 for v in grid.values() if v == "#")


def p1(grid):
    grid = grid.copy()
    for fold in folds[:1]:
        apply(fold, grid)
    print(count(grid))


def p2(grid):
    grid = grid.copy()
    for fold in folds:
        apply(fold, grid)
    return grid


p1(grid)
print_grid(p2(grid))
