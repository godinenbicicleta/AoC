import fileinput
from collections import defaultdict

fish_array = [int(k) for line in fileinput.input() for k in line.strip().split(",")]

fish = defaultdict(int)

for f in fish_array:
    fish[f] += 1


def run(fish, days):
    for day in range(days):
        new_counter = defaultdict(int)
        for num in range(1, 9):
            new_counter[num - 1] = fish[num]
        new_counter[8] += fish[0]
        new_counter[6] += fish[0]
        fish = new_counter

    return fish


print(sum(run(fish, 256).values()))
