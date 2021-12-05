import fileinput
from collections import defaultdict

d1 = defaultdict(lambda: 0)
part2 = []
for line in fileinput.input():
    in_d1 = True
    start, end = line.split(" -> ")
    start_x, start_y = [int(n) for n in start.split(",")]
    end_x, end_y = [int(n) for n in end.split(",")]
    if start_x != end_x and start_y != end_y:
        part2.append(((start_x, start_y), (end_x, end_y)))
        continue

    for i in range(min(start_x, end_x), max(start_x, end_x) + 1):
        for j in range(min(start_y, end_y), max(start_y, end_y) + 1):
            d1[(j, i)] += 1

# for j in range(0, 12):
#     for i in range(0, 12):
#         if d1[(j, i)] == 0:
#             print(".", end="")
#         else:
#             print(d1[(j, i)], end="")
#     print()

counter = 0

for key, value in d1.items():
    if value > 1:
        counter += 1
print(counter)

for (start_x, start_y), (end_x, end_y) in part2:
    if abs(end_x - start_x) != abs(end_y - start_y):
        continue

    deltax = 1 if end_x > start_x else -1
    deltay = 1 if end_y > start_y else -1
    for i, j in zip(
        range(start_x, end_x + deltax, deltax),
        range(start_y, end_y + deltay, deltay),
    ):
        d1[(j, i)] += 1


counter = 0
for key, value in d1.items():
    if value > 1:
        counter += 1
print(counter)

# for j in range(0, 10):
#     for i in range(0, 10):
#         if d1[(j, i)] == 0:
#             print(".", end="")
#         else:
#             print(d1[(j, i)], end="")
#     print()
