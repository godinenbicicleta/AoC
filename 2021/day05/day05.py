import fileinput
from collections import defaultdict
from itertools import product

d1 = defaultdict(int)
d2 = defaultdict(int)


def delta(start, end):
    return 1 if end > start else -1


def parse(line):
    start, end = line.split(" -> ")
    start_x, start_y = [int(n) for n in start.split(",")]
    end_x, end_y = [int(n) for n in end.split(",")]
    return start_x, end_x, start_y, end_y


for line in fileinput.input():
    start_x, end_x, start_y, end_y = parse(line)
    deltax = delta(start_x, end_x)
    deltay = delta(start_y, end_y)
    x_range = range(start_x, end_x + deltax, deltax)
    y_range = range(start_y, end_y + deltay, deltay)
    diagonal = zip(x_range, y_range)
    vertical_horizontal = product(x_range, y_range)

    if start_x == end_x or start_y == end_y:
        for i, j in vertical_horizontal:
            d1[(j, i)] += 1
            d2[(j, i)] += 1
        continue
    for i, j in diagonal:
        d2[(j, i)] += 1

for d in (d1, d2):
    counter = 0

    for key, value in d.items():
        if value > 1:
            counter += 1
    print(counter)


# for j in range(0, 12):
#     for i in range(0, 12):
#         if d1[(j, i)] == 0:
#             print(".", end="")
#         else:
#             print(d1[(j, i)], end="")
#     print()

# for j in range(0, 10):
#     for i in range(0, 10):
#         if d1[(j, i)] == 0:
#             print(".", end="")
#         else:
#             print(d1[(j, i)], end="")
#     print()
