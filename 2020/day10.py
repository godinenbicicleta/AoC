from collections import deque
from collections import Counter
import functools
import itertools

with open("day10.txt") as f:
    data = [int(line.strip()) for line in f]

chain = [0]


def run():
    sd = [0] + sorted(data)
    max_adapter = sd[-1] + 3
    diffs = []
    for i in range(len(sd) - 1):
        diffs.append(sd[i + 1] - sd[i])
    diffs.append(max_adapter - sd[-1])
    c = Counter(diffs)
    print(c)
    print(sd)
    print(c[3] * c[1])


def run2():
    sd = sorted(data)
    total_data = set([0] + sd + [sd[-1] + 3])

    to_remove = set()
    for elem in sd:
        if can_remove(elem, total_data):
            to_remove.add(elem)

    chunks = to_chunks(sorted(to_remove))
    sols = 1
    for chunk in chunks:
        l = len(find_solutions(total_data, set(chunk), set()))
        sols *= l
    print(sols)


def to_chunks(data):
    chunks = []
    current_chunk = []
    for i in range(len(data)):
        if not current_chunk:
            current_chunk.append(data[i])

        elif data[i] - current_chunk[-1] <= 3:
            current_chunk.append(data[i])
        else:
            chunks.append(current_chunk)
            current_chunk = [data[i]]
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def find_solutions(data, to_remove, removed):
    if not to_remove:
        return [removed]
    elem = to_remove.pop()
    res = []
    if can_remove(elem, data):

        for sol in find_solutions(data - {elem}, to_remove - {elem}, removed | {elem}):
            res.append(sol)
    for sol in find_solutions(data, to_remove - {elem}, removed):
        res.append(sol)
    return res


def can_remove(elem, data):

    if elem - 1 in data and elem + 1 in data:
        return True
    if elem - 1 in data and elem + 2 in data:
        return True
    if elem - 2 in data and elem + 1 in data:
        return True

    return False


def is_valid(sol):
    solution = tuple(sorted(sol))

    res = True
    for i in range(1, len(solution)):
        if solution[i] - solution[i - 1] > 3:
            res = False
            break
    return res


if __name__ == "__main__":
    import time

    run()
    time0 = time.time()
    run2()
    print("run in %s", time.time() - time0)
