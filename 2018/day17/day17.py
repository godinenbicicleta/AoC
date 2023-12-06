import fileinput
from collections import deque
import math
import re

grid = {}
lines = []
for line in fileinput.input():
    line = line.strip()
    lines.append(line)


for line in lines:
    if line.startswith("x="):
        (x,) = re.match(r"x=(\d+),", line).groups()
        y1, y2 = line.split("y=")[1].split("..")
        y1 = int(y1)
        y2 = int(y2)
        x = int(x)
        for y in range(y1, y2 + 1):
            grid[(x, y)] = "#"
    elif line.startswith("y"):
        (y,) = re.match(r"y=(\d+),", line).groups()
        y = int(y)
        x1, x2 = line.split("x=")[1].split("..")
        x1 = int(x1)
        x2 = int(x2)
        for x in range(x1, x2 + 1):
            grid[(x, y)] = "#"

minx = math.inf
maxx = -math.inf
miny = math.inf
maxy = -math.inf
for x, y in grid.keys():
    if x < minx:
        minx = x
    if y < miny:
        miny = y
    if x > maxx:
        maxx = x
    if y > maxy:
        maxy = y


def print_grid(g):
    for y in range(0, int(maxy) + 2):
        for x in range(int(minx) - 1, int(maxx) + 2):
            if y == 0 and x == 500:
                print("+", end="")

            elif (x, y) not in g:
                print(".", end="")
            else:
                print(g[(x, y)], end="")
        print()


def escapes(p: tuple[int, int]) -> bool:
    stack = [p]
    seen = set()
    goaly = p[1] + 1
    while stack:
        current = stack.pop()
        seen.add(current)
        x, y = current
        if y >= goaly:
            return True
        # try down
        down = (x, y + 1)
        if down[1] > maxy:
            continue

        if grid.get(down, ".") == "." or grid.get(down, ".") == "|":
            stack.append(down)
            continue
        right = (x + 1, y)
        if grid.get(right, ".") in (".", "|"):
            if right not in seen:
                stack.append(right)
        left = (x - 1, y)
        if grid.get(left, ".") in (".", "|"):
            if left not in seen:
                stack.append(left)
    return False


m = 0
changed = True

while changed:
    m += 1
    current = (500, 1)
    queue = deque([current])
    seen = set()
    changed = False
    while queue:
        current = queue.popleft()
        x, y = current
        seen.add(current)
        current_val = grid.get(current)

        # try down
        down = (x, y + 1)
        if down[1] > maxy:
            if current_val != "|":
                changed = True
            grid[current] = "|"
            continue

        if grid.get(down, ".") == "." or grid.get(down, ".") == "|":
            queue.append(down)
        else:
            right = (x + 1, y)
            if grid.get(right, ".") in (".", "|"):
                if right not in seen:
                    queue.append(right)
            left = (x - 1, y)
            if grid.get(left, ".") in (".", "|"):
                if left not in seen:
                    queue.append(left)

        if not escapes(current):
            if current_val != "~":
                changed = True
            grid[current] = "~"
        else:
            if current_val != "|":
                changed = True
            grid[current] = "|"

    if not changed:
        break

total = 0
retained = 0
for k, v in grid.items():
    x, y = k
    if y >= miny and y <= maxy:
        if v == "|" or v == "~":
            total += 1
    if v == "~":
        retained += 1
print(total, retained)
