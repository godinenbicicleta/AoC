from functools import reduce

with open("input01.txt") as f:
    data = f.read().strip().split(", ")


def get_new_p(current, new):
    if current == "N":
        if new == "L":
            return "W"
        elif new == "R":
            return "E"
    if current == "S":
        if new == "L":
            return "E"
        if new == "R":
            return "W"
    if current == "E":
        if new == "L":
            return "N"
        if new == "R":
            return "S"
    if current == "W":
        if new == "L":
            return "S"
        return "N"


def reducer(acc, elem):
    x, y, p = acc
    new_p = get_new_p(p, elem[0])
    steps = int(elem[1:])
    for _ in range(steps):
        if new_p == "N":
            x, y = x, y + 1
        elif new_p == "S":
            x, y = x, y - 1
        elif new_p == "E":
            x, y = x + 1, y
        elif new_p == "W":
            x, y = x - 1, y
        else:
            raise ValueError("Unknown p")
        if (x, y) in seen:
            print("seen", (x, y), abs(x) + abs(y))
        else:
            seen.add((x, y))
    return (x, y, new_p)


# for i in (["R2", "L3"], ["R2", "R2", "R2"], ["R5", "L5", "R5", "R3"], data):
seen = {(0, 0)}
res = reduce(reducer, data, (0, 0, "N"))
print(res)
print(abs(res[0]) + abs(res[1]))
