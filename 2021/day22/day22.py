import fileinput
import re

data = {}
parsed = []
for i, line in enumerate(fileinput.input()):
    line = line.strip()
    if line.startswith("on "):
        p = 1
        xmin, xmax, ymin, ymax, zmin, zmax = tuple(
            map(
                int,
                re.match(
                    "on x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line
                ).groups(),
            )
        )
    else:
        p = 0
        xmin, xmax, ymin, ymax, zmin, zmax = tuple(
            map(
                int,
                re.match(
                    "off x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line
                ).groups(),
            )
        )
    parsed.append(((xmin, xmax, ymin, ymax, zmin, zmax), p))
    if not all(abs(k) <= 50 for k in (xmin, xmax, ymin, ymax, zmin, zmax)):
        continue
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            for z in range(zmin, zmax + 1):
                data[(x, y, z)] = p


print(sum(data.values()))


def intersection(p1, p2):
    (xmin, xmax, ymin, ymax, zmin, zmax) = p1
    (xmin_, xmax_, ymin_, ymax_, zmin_, zmax_) = p2
    if xmax < xmin_ or ymax < ymin_ or zmax < zmin_:
        return None
    if xmax_ < xmin or ymax_ < ymin or zmax_ < zmin:
        return None
    return (
        max(xmin, xmin_),
        min(xmax, xmax_),
        max(ymin, ymin_),
        min(ymax, ymax_),
        max(zmin, zmin_),
        min(zmax, zmax_),
    )


def vals(a, b):
    return b - a + 1


def complement_(p):
    (xmin_, xmax_, ymin_, ymax_, zmin_, zmax_) = p
    dc1 = (
        float("-inf"),
        xmin_ - 1,
        float("-inf"),
        float("inf"),
        float("-inf"),
        float("inf"),
    )
    dc2 = (
        xmax_ + 1,
        float("inf"),
        float("-inf"),
        float("inf"),
        float("-inf"),
        float("inf"),
    )
    dc3 = (
        float("-inf"),
        float("inf"),
        float("-inf"),
        ymin_ - 1,
        float("-inf"),
        float("inf"),
    )
    dc4 = (
        float("-inf"),
        float("inf"),
        ymax_ + 1,
        float("inf"),
        float("-inf"),
        float("inf"),
    )
    dc5 = (
        float("-inf"),
        float("inf"),
        float("-inf"),
        float("inf"),
        float("-inf"),
        zmin_ - 1,
    )
    dc6 = (
        float("-inf"),
        float("inf"),
        float("-inf"),
        float("inf"),
        zmax_ + 1,
        float("inf"),
    )
    return (dc1, dc2, dc3, dc4, dc5, dc6)


def complement(point, d):
    dc1, dc2, dc3, dc4, dc5, dc6 = complement_(d)

    intersections = [intersection(point, k) for k in (dc1, dc2, dc3, dc4, dc5, dc6)]
    return [i for i in intersections if i is not None]


def union(sets):
    res = []
    for s in sets:
        if not res:
            res.append(s)
            continue
        if not any(intersection(s, r) for r in res):
            res.append(s)
            continue
        parts = [s]
        for i in range(len(res)):
            r = res[i]
            new_parts = []
            for j in range(len(parts)):
                part = parts[j]
                if not intersection(part, r):
                    new_parts.append(part)
                elif intersection(part, r) == part:
                    continue
                elif intersection(part, r) == r:
                    res[i] = part
                    new_parts.extend(parts[j + 1 :])
                    break
                else:
                    for p in complement_(intersection(part, r)):
                        if intersection(part, p):
                            new_parts.append(intersection(part, p))
            parts = new_parts
        res.extend(union(parts))

    return res


def size(p):
    (xmin, xmax, ymin, ymax, zmin, zmax) = p
    res = vals(xmin, xmax) * vals(ymin, ymax) * vals(zmin, zmax)
    return res


def total_size(arr):
    total = 0
    for i in union(arr):
        total += size(i)
    return total


current = []
for i, (p, v) in enumerate(parsed):
    if not current:
        current = [p]
        continue
    if v:
        current = union(current + [p])
        continue
    current = union(
        [
            intersection(c, k)
            for c in current
            for k in complement_(p)
            if intersection(c, k)
        ]
    )

print(total_size(current))
