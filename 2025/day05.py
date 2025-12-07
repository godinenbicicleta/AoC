from typing import NamedTuple


class Interval(NamedTuple):
    min: int
    max: int


with open(0) as f:
    data = f.read()

intervals, ingredients = data.split("\n\n")


intervals = map(lambda x: tuple(map(int, x.split("-"))), intervals.strip().split("\n"))
intervals = sorted(Interval(min=x, max=y) for x, y in intervals)
ingredients = map(int, ingredients.strip().split("\n"))


fresh = 0
for i in ingredients:
    for left, right in intervals:
        if i > right or i < left:
            continue
        fresh += 1
        break
print(fresh)


total = 0
prev_min, prev_max = intervals[0]

for left, right in intervals[1:]:
    if left > prev_max:
        total += prev_max - prev_min + 1
        prev_min, prev_max = left, right
        continue
    prev_max = max(right, prev_max)

total += prev_max - prev_min + 1
print(total)
