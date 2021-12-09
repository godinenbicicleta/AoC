import fileinput
from math import prod
from operator import itemgetter

grid = [list(map(int, line.strip())) for line in fileinput.input()]

first = itemgetter(0)
second = itemgetter(1)


def neighbors(x, y):
    candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    for i, j in candidates:
        if i < 0 or j < 0:
            continue
        if i >= len(grid[0]) or j >= len(grid):
            continue
        yield grid[j][i], (i, j)


def is_low_point(x, y):
    return all(first(p) > grid[y][x] for p in neighbors(x, y))


# print("\n".join("".join(map(str, l)) for l in grid))
low_points = []
risk = 0
for y, row in enumerate(grid):
    for x, elem in enumerate(row):
        if is_low_point(x, y):
            risk += 1 + grid[y][x]
            low_points.append((x, y))
print(risk)

basins = {p: set() for p in low_points}

for x, y in low_points:
    candidates = list(second(p) for p in neighbors(x, y)) + [(x, y)]
    seen = set()
    while candidates:
        i, j = candidates.pop()
        if (i, j) in seen:
            continue
        else:
            seen.add((i, j))
        if grid[j][i] != 9:
            basins[(x, y)].add((i, j))
            candidates.extend(second(p) for p in neighbors(i, j))


def key(x):
    return len(second(x))


sorted_basins = sorted(basins.items(), key=key, reverse=True)
prod_top3_lengths = prod(map(key, sorted_basins[:3]))

print(prod_top3_lengths)
