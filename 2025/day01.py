import fileinput


lines = list(fileinput.input(encoding="utf-8"))

size = 100


def process_line(line, state):
    dir = line[0]
    num = int(line[1:])
    if dir == "L":
        state -= num
    else:
        state += num
    return state


def part1():
    res = 0
    state = 50
    for line in lines:
        state = process_line(line, state)
        state = state % 100
        if state == 0:
            res += 1
    return res


def part2():
    state0 = 50
    rotations = 0
    for line in lines:
        line = line.strip()
        num = int(line[1:])
        state1 = state0
        for _ in range(num):
            state1 = state1 - 1 if line[0] == "L" else state1 + 1
            if state1 == 0:
                rotations += 1
            elif state1 == size:
                rotations += 1
                state1 = 0
            elif state1 == -1:
                state1 = size - 1
        state0 = state1
    return rotations


print("part1: ", part1())
print("part2: ", part2())
