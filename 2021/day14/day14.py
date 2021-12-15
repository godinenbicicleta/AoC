import sys
from collections import Counter

with open(sys.argv[1]) as f:
    data = f.read().strip()


template, instructions = data.split("\n\n")
instructions = dict(tuple(k.split(" -> ")) for k in instructions.strip().split("\n"))
memo = {}


def process(m, turns):
    if (m, turns) in memo:
        return memo[(m, turns)]
    if turns == 0 or len(m) == 1:
        res = Counter(m)
    elif len(m) == 2:
        n = instructions[m]
        res = process(f"{m[0]}{n}{m[1]}", turns - 1)
    else:
        res = process(m[:2], turns) + process(m[1:], turns) - Counter(m[1])
    memo[(m, turns)] = res
    return res


for part, n in zip((1, 2), (10, 40)):
    counts = process(template, n)
    most_common = counts.most_common()
    print("part", part, most_common[0][1] - most_common[-1][1])
