import fileinput
from functools import cache


intLines = []
strLines = []
for line in fileinput.input(encoding="utf-8"):
    strLines.append(line.strip())
    intLines.append(list(map(int, line.strip())))


def joltage(line):
    maxN = 0
    pos = []
    for i, num in enumerate(line[:-1]):
        if num > maxN:
            maxN = num
            pos = [i]
        elif num == maxN:
            pos.append(i)
    maxJ = 0
    for p in pos:
        js = maxN * 10 + max(line[p + 1 :])
        if js > maxJ:
            maxJ = js
    return maxJ


print("part1: ", sum(map(joltage, intLines)))


@cache
def joltage2(line, num=12):
    if num == 0:
        return 0
    if len(line) < num:
        return 0
    if len(line) == num:
        return int(line)
    left = int(line[0]) * (10 ** (num - 1)) + joltage2(line[1:], num - 1)
    right = joltage2(line[1:], num)
    return max(left, right)


print("part2: ", sum(map(joltage2, strLines)))
