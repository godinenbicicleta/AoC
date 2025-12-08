import math

with open(0) as f:
    data = f.readlines()

data = [tuple(map(int, line.strip().split(","))) for line in data]


def distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


distances = []

for i, p in enumerate(data):
    for j, q in enumerate(data):
        if j <= i:
            continue
        d = distance(p, q)
        distances.append((d, (p, q)))

distances = sorted(distances, key=lambda x: x[0])


_, (fst_p, fst_q) = distances[0]

circuits = [{fst_q, fst_p}]


for d, (p, q) in distances[1:1000]:
    candidates = [(i, c) for i, c in enumerate(circuits) if p in c or q in c]
    if not candidates:
        circuits.append({p, q})
    elif len(candidates) == 2:
        to_remove = [i for i, _ in candidates]
        circuits = [c for i, c in enumerate(circuits) if i not in to_remove]
        merged = candidates[0][1] | candidates[1][1]
        circuits.append(merged)
    else:
        candidates[0][1].add(p)
        candidates[0][1].add(q)

res = sorted(circuits, key=lambda x: len(x), reverse=True)[:3]
print("p1:", len(res[0]) * len(res[1]) * len(res[2]))

circuits = [{fst_q, fst_p}]


for d, (p, q) in distances[1:]:
    candidates = [(i, c) for i, c in enumerate(circuits) if p in c or q in c]
    if not candidates:
        circuits.append({p, q})
    elif len(candidates) == 2:
        to_remove = [i for i, _ in candidates]
        circuits = [c for i, c in enumerate(circuits) if i not in to_remove]
        merged = candidates[0][1] | candidates[1][1]
        circuits.append(merged)
        if len(merged) == len(data):
            res = p[0] * q[0]
            break

    else:
        candidates[0][1].add(p)
        candidates[0][1].add(q)
        if len(candidates[0][1]) == len(data):
            res = p[0] * q[0]
            break

print("p2:", res)
