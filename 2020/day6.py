from functools import reduce

with open("day6.txt") as f:
    data = f.read()


groups = data.split("\n\n")

gd = {}

for ix, group in enumerate(groups):
    answers = []
    for line in group.split("\n"):
        answers.append(set(line))
    gd[ix] = reduce(lambda x, y: x | y, answers)

print(sum(map(lambda x: len(x), gd.values())))

for ix, group in enumerate(groups):
    answers = []
    for line in group.split("\n"):
        answers.append(set(line))
    gd[ix] = reduce(lambda x, y: x & y, answers)

print(sum(map(lambda x: len(x), gd.values())))
