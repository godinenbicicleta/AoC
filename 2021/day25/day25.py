import fileinput
from typing import NamedTuple

fig = []
for line in fileinput.input():
    fig.append(list(line.strip()))


def h(f):
    return "".join("".join(k) for k in fig)


class Dimensions(NamedTuple):
    x: int
    y: int


dimensions = Dimensions(x=len(fig[0]), y=len(fig))


def next_pos_east(x, y):
    if x + 1 == dimensions.x:
        return (0, y)
    return (x + 1, y)


def next_pos_south(x, y):
    if y + 1 == dimensions.y:
        return (x, 0)
    return (x, y + 1)


def show(f):
    s = "\n".join("".join(k for k in m) for m in f)
    print(s)
    print()


def move_east(f):
    res = [[None for _ in range(dimensions.x)] for _ in range(dimensions.y)]
    overrides = []
    for y, row in enumerate(f):
        for x, value in enumerate(row):
            res[y][x] = value
            if value == "." or value == "v":
                continue
            new_x, new_y = next_pos_east(x, y)
            if f[new_y][new_x] == ".":
                overrides.append((x, y, "."))
                overrides.append((new_x, new_y, ">"))
    for x, y, v in overrides:
        res[y][x] = v
    return res


def move_south(f):
    res = [[None for _ in range(dimensions.x)] for _ in range(dimensions.y)]
    overrides = []
    for y, row in enumerate(f):
        for x, value in enumerate(row):
            res[y][x] = value
            if value == "." or value == ">":
                continue
            new_x, new_y = next_pos_south(x, y)
            if f[new_y][new_x] == ".":
                overrides.append((x, y, "."))
                overrides.append((new_x, new_y, "v"))
    for x, y, v in overrides:
        res[y][x] = v
    return res


prev = h(fig)
steps = 0

show(fig)
while True:
    steps += 1
    #    print(steps)
    fig = move_east(fig)
    fig = move_south(fig)
    #    show(fig)
    if h(fig) == prev:
        print(steps)
        break
    prev = h(fig)
