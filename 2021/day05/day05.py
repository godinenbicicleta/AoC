import fileinput
from collections import defaultdict

d1 = defaultdict(int)
d2 = defaultdict(int)
for line in fileinput.input():
    in_d1 = True
    start, end = line.split(" -> ")
    start_x, start_y = [int(n) for n in start.split(",")]
    end_x, end_y = [int(n) for n in end.split(",")]
    deltax = 1 if end_x > start_x else -1
    deltay = 1 if end_y > start_y else -1
    if start_x != end_x and start_y != end_y:
        for i, j in zip(
            range(start_x, end_x + deltax, deltax),
            range(start_y, end_y + deltay, deltay),
        ):
            d2[(j, i)] += 1

    else:
        for i in range(start_x, end_x + deltax, deltax):
            for j in range(start_y, end_y + deltay, deltay):
                d1[(j, i)] += 1
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
