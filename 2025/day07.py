from collections import deque
from functools import cache

with open(0) as f:
    data = f.read().strip()

start_pos = None
maxy = 0
maxx = 0
grid = {}
for y, row in enumerate(data.split("\n")):

    for x, c in enumerate(row):
        if c == "S":
            start_pos = (y, x)
        grid[(y, x)] = c
        maxx = x
    maxy = y


def p1(grid):
    grid = grid.copy()
    queue = deque([start_pos])
    splits = 0
    while queue:
        pos = queue.popleft()
        if pos[0] > maxy:
            continue
        c = grid[pos]
        if c == "." or c == "S":
            grid[pos] = "|"
            queue.append((pos[0] + 1, pos[1]))
            continue
        if c == "|":
            continue
        assert c == "^"
        splits += 1
        queue.append((pos[0], pos[1] + 1))
        queue.append((pos[0], pos[1] - 1))
    print(splits)


@cache
def timelines(pos):
    y, x = pos
    if y > maxy:
        return 1
    c = grid[pos]
    if grid[pos] == "." or c == "S":
        return timelines((y + 1, x))
    return timelines((y, x + 1)) + timelines((y, x - 1))


p1(grid)
print(timelines(start_pos))
