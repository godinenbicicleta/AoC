import math
import sys
import time
from collections import defaultdict
from enum import Enum
from functools import partial
from itertools import chain
from typing import NamedTuple

t0 = time.time()


class Axis(Enum):
    x = "x"
    y = "y"
    z = "z"


def rotate(p, angle, axis):
    cos = int(math.cos(angle))
    sin = int(math.sin(angle))
    if axis == Axis.z:
        x = int(p.x * cos - p.y * sin)
        y = int(p.x * sin + p.y * cos)
        z = p.z
    elif axis == Axis.y:
        x = int(p.x * cos + p.z * sin)
        y = p.y
        z = int(-p.x * sin + p.z * cos)
    elif axis == Axis.x:
        x = p.x
        y = int(p.y * cos - p.z * sin)
        z = int(p.y * sin + p.z * cos)

    else:
        raise ValueError(f"Invalid axis {axis}")

    return Point(x, y, z)


def combs(x):
    if len(x) == 1:
        yield [x[0]]
        yield [-x[0]]
    else:
        for i in range(len(x)):
            for c in combs([k for j, k in enumerate(x) if j != i]):
                yield [x[i]] + c
                yield [-x[i]] + c


def comb_take(x, n):
    if n == 0:
        yield []
    elif len(x) == 1:
        for elem in x:
            yield [elem]
    else:
        for i in range(len(x)):
            for c in comb_take(x, n - 1):
                yield [x[i]] + c


def _rotations(p):
    ops_used = []
    k = p
    seen = {p}
    ops = [partial(rotate, angle=math.pi / 2, axis=k) for k in Axis]
    for oplist in chain(
        comb_take(ops, 1), comb_take(ops, 2), comb_take(ops, 3), comb_take(ops, 4)
    ):
        oplist = list(oplist)
        k = p
        for op in oplist:
            k = op(k)
        if len(seen) >= 24:
            break
        if k not in seen:
            ops_used.append(oplist)
            seen.add(k)
    return ops_used


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z

        return Point(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Point(x, y, z)

    def vars(self):
        for r, p in zip(reference, rotations(self)):
            yield (tuple(r), p)


ops_used = _rotations(Point(1, 2, 3))
assert len(ops_used) == 23


def rotations(p):
    yield p
    for oplist in ops_used:
        k = p
        for op in oplist:
            k = op(k)
        yield k


reference = list(rotations(Point(1, 2, 3)))
assert len(reference) == 24
assert len(set(reference)) == 24

assert Point(0, 0, 0) + Point(0, 1, 0) == Point(0, 1, 0)

assert Point(0, 0, 0) - Point(1, 0, -1) == Point(-1, 0, 1)

with open(sys.argv[1]) as f:
    data = f.read().strip().split("\n")

scanners = []
for i in range(len(data)):
    line = data[i].strip()
    if not line:
        continue
    if line.startswith("--"):
        scanners.append([])
    else:
        x, y, z = list(map(int, line.split(",")))
        scanners[-1].append(Point(x, y, z))


positions = {0: Point(0, 0, 0)}


def match2(l1, l2):
    v2 = l2.vars()
    seen = set()
    a = l1
    for ref, b in v2:
        c = a - b
        if c not in seen:
            seen.add(c)
            yield c, ref


def match(i, j):
    s1 = scanners[i]
    s2 = scanners[j]
    counts = defaultdict(set)
    refs = defaultdict(set)
    for ix, l1 in enumerate(s1):
        seen = set()
        for l2 in s2:
            v2 = l2.vars()
            for ref, b in v2:
                c = l1 - b
                if c not in seen:
                    seen.add(c)
                    counts[c].add((l1, l2))
                    refs[c].add(ref)

    s = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    s = [m for m in s if len(m[1]) >= 12]
    if s:
        point = s[0][0]
        ref = refs[point].pop()
        return point, ref

    return None


def convert(point, source, source_frame):
    x_pos = abs(source_frame[0]) - 1
    y_pos = abs(source_frame[1]) - 1
    z_pos = abs(source_frame[2]) - 1

    x_sign = +1 if source_frame[0] > 0 else -1
    y_sign = +1 if source_frame[1] > 0 else -1
    z_sign = +1 if source_frame[2] > 0 else -1

    p = [point.x, point.y, point.z]
    sx, sy, sz = source.x, source.y, source.z
    new_x = sx + x_sign * p[x_pos]
    new_y = sy + y_sign * p[y_pos]
    new_z = sz + z_sign * p[z_pos]
    res = Point(new_x, new_y, new_z)
    return res


def is_inside_match(p, m):
    for elem, ref in m:
        if p == elem:
            return True
    return False


def run(scanners):
    seen = set()
    positions = defaultdict(list)
    positions[0] = [(Point(0, 0, 0), (1, 2, 3), 0)]
    paths = [None for _ in scanners]
    paths[0] = [(Point(0, 0, 0), (1, 2, 3), 0)]

    i = 0
    while len(positions) != len(scanners):
        for j in range(1, len(scanners)):

            if i == j or (i, j) in seen:
                continue
            seen.add((i, j))
            p = match(i, j)
            if p is None:
                continue
            p, ref = p
            positions[j].append((p, ref, i))
        i += 1
        positions[j] = sorted(positions[j], key=lambda x: x[2])

    new_positions = {0: Point(0, 0, 0)}
    while not len(new_positions) == len(positions):
        for k, references in positions.items():
            if k in new_positions:
                continue
            solved_refs = []
            for v in references:
                point, frame, respect_to = v
                if respect_to not in new_positions:
                    continue
                solved_refs.append(v)
            if not solved_refs:
                continue

            point, res_path = solve(solved_refs, new_positions, positions)
            new_positions[k] = point
            paths[k] = res_path
    return positions, new_positions, paths


def solve(arr, new_positions, positions):
    paths = [[i] for i in arr]
    resPath = None
    while True:
        path = paths.pop()
        to_explore = path[-1]
        point, frame, respect_to = to_explore
        if respect_to == 0:
            resPath = path
            break
        for ref_point, ref_frame, ref_ref in positions[respect_to]:
            if ref_ref not in new_positions:
                continue
            if (ref_point, ref_frame, ref_ref) not in path:
                paths.append(path + [(ref_point, ref_frame, ref_ref)])
    point, _, _ = resPath[0]
    for ref_point, ref_frame, ref_ref in resPath[1:]:
        new_point = convert(point, ref_point, ref_frame)
        point = new_point
    return point, resPath


totalPoints = set()
positions, new_positions, paths = run(scanners)
for ix, s in enumerate(scanners):
    for point in s:
        if ix == 0:
            totalPoints.add(point)
            continue
        for ref_point, ref_frame, ref_ref in paths[ix]:
            new_point = convert(point, ref_point, ref_frame)
            point = new_point
        totalPoints.add(point)
print(len(totalPoints))

maxDistance = 0


def distance(a, b):
    p1 = new_positions[a]
    p2 = new_positions[b]
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)


for ix, scanner in enumerate(scanners):
    for jx, scanner2 in enumerate(scanners):

        d = distance(ix, jx)
        if d > maxDistance:
            maxDistance = d
print(maxDistance)
print(time.time() - t0)
