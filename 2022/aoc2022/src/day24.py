from collections import deque
from collections import defaultdict
sample = """#E######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".strip().split("\n")

with open("data/day24.txt") as f:
    real = f.read().strip().split("\n")

data = sample
data = real

g = {}
maxx = 0
maxy = 0
minx = 0
miny = 0
for y, line in enumerate(data):
    for (x, c) in enumerate(line):
        maxx = x
        maxy = y
        if c in ('>', '<', '^', 'v'):
            g[(x, y)] = [c]

start = (1, 0)
goal = (maxx-1, maxy)


cache = {0: g}


def grid_at(t):
    if t in cache:
        return cache[t]
    if t > (maxy-miny-1) * (maxx-minx-1):
        return grid_at(t % ((maxy-miny-1) * (maxx-minx-1)))
    new_g = defaultdict(list)
    for ((x, y), cs) in grid_at(t-1).items():
        for c in cs:
            newx = x
            newy = y
            if c == ">":
                newx = x+1
                if newx == maxx:
                    newx = minx+1
            if c == "<":
                newx = x-1
                if newx == minx:
                    newx = maxx-1
            if c == "^":
                newy = y-1
                if newy == miny:
                    newy = maxy-1
            if c == "v":
                newy = y+1
                if newy == maxy:
                    newy = miny+1
            new_g[(newx, newy)].append(c)
    cache[t] = new_g
    return new_g


print(g)
print(minx, maxx, miny, maxy)


def print_g(g, current):
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x, y) in g:
                if len(g[(x, y)]) == 1:
                    print(g[(x, y)][0], end='')
                else:
                    print(len(g[(x, y)]), end='')
            elif (x, y) == current:
                print("E", end="")
            elif x == maxx or y == maxy:
                print("#", end="")
            elif x == minx or y == miny:
                print("#", end="")
            else:
                print(".", end="")
        print()


print_g(grid_at(0), start)


def solve(start, goal, t):
    seen = {start: [t]}

    queue = deque([(start, t, [start])])
    while queue:
        current, t, path = queue.popleft()

        if current == goal:
            print_g(grid_at(t), current)
            print(t)
            return t
        grid = grid_at(t+1)
        x, y = current
        candidates = ((x+1, y), (x-1, y), (x, y+1), (x, y-1), (x, y))
        for candidate in candidates:
            if candidate in grid:
                continue
            if candidate[0] == maxx or candidate[0] == minx:
                continue
            if candidate[1] == miny and candidate != start and candidate != goal:
                continue
            if candidate[1] >= maxy and candidate != goal and candidate != start:
                continue
            if candidate in seen:
                seen_ts = seen[candidate]
                if t+1 in seen_ts:
                    continue
                if any((st > t+1 and (st-t-1) % ((maxy-miny-1) * (maxx-minx-1)) == 0) for st in seen_ts):
                    continue
            else:
                seen[candidate] = []
            new_path = list(path)
            new_path.append(candidate)
            queue.append((candidate, t+1, new_path))
            seen[candidate].append(t+1)


t0 = solve(start, goal, 0)
t1 = solve(goal, start, t0)
t1 = solve(start, goal, t1)
