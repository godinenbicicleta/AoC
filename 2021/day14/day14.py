import sys
from collections import Counter, defaultdict

sys.setrecursionlimit(10 ** 6)

with open(sys.argv[1]) as f:
    data = f.read().strip()


def s_pair(s):
    return f"{s[0]}{s[1]}"


memo = {}


def expand(s):
    if s in memo:
        return memo[s]
    if len(s) == 1:
        res = s
    elif len(s) == 2:
        res = f"{s[0]}{instructions[s]}{s[1]}"

    elif len(s) == 3:
        res = f"{s[0]}{instructions[s[:2]]}{s[1]}{instructions[s[1:]]}{s[2]}"
    else:
        mid = len(s) // 2
        m1 = expand(s[:mid])
        m2 = expand(s[mid - 1 :])[1:]
        res = f"{m1}{m2}"
    memo[s] = res
    return res


template, instructions = data.split("\n\n")
instructions = dict(tuple(k.split(" -> ")) for k in instructions.strip().split("\n"))
s = template
for step in range(10):
    s = expand(s)
counts = Counter(s)
print(counts)
most_common = counts.most_common()
print(most_common[0][1] - most_common[-1][1])

s = template

memo2 = {}


def process(m, turns):
    if (m, turns) in memo2:
        return memo2[(m, turns)]
    if turns == 0:
        res = Counter(m)
    elif len(m) == 1:
        res = Counter(m)
    elif len(m) == 2:
        n = instructions[m]
        res = process(f"{m[0]}{n}{m[1]}", turns - 1)
    else:
        res = process(m[:2], turns) + process(m[1:], turns) - Counter(m[1])
    memo2[(m, turns)] = res
    return res


counts = process(s, 40)
most_common = counts.most_common()
print(most_common[0][1] - most_common[-1][1])
