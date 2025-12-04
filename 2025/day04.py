import fileinput

grid = set()

for y, line in enumerate(fileinput.input(encoding="utf-8")):
    for x, c in enumerate(line):
        if c == "@":
            grid.add((x, y))


def count(grid, seen=None):
    res = 0
    _seen = seen or ()
    for x, y in grid:
        if (x, y) in _seen:
            continue
        candidates = (
            (x + 1, y + 1),
            (x, y + 1),
            (x - 1, y + 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
        )
        num = sum(1 for p in candidates if p in grid and p not in _seen)
        if num < 4:
            res += 1
            if seen is not None:
                seen.add((x, y))
    return res


p1 = count(grid, None)
print(p1)


res = 0
seen = set()
while True:
    num = count(grid, seen)
    if num == 0:
        break
    res += num

print(res)
