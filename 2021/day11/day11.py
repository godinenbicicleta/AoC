import fileinput


def show():
    print("-" * 10)
    print("\n".join("".join([str(k) for k in j]) for j in grid))
    print("-" * 10)


def ns(i, j):
    for x, y in [
        (i + 1, j),
        (i - 1, j),
        (i + 1, j + 1),
        (i - 1, j - 1),
        (i + 1, j - 1),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j + 1),
    ]:
        if x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid):
            yield x, y


def increase_energy():
    for j, row in enumerate(grid):
        for i, _ in enumerate(row):
            grid[j][i] += 1


class Finished(Exception):
    pass


def run():
    total = 0
    step = 0
    while True:
        increase_energy()
        glows = set()
        while True:
            size = len(glows)
            for j, row in enumerate(grid):
                for i, v in enumerate(row):
                    if (i, j) in glows:
                        continue
                    if v > 9:
                        glows.add((i, j))
                        for n in ns(i, j):
                            grid[n[1]][n[0]] += 1
            if len(glows) == 100:
                print("p2", step + 1)
                raise Finished
            if size == len(glows):
                total += size
                break
        for i, j in glows:
            grid[j][i] = 0
        if step == 99:
            print("p1", total)
        step += 1


if __name__ == "__main__":
    grid = [[int(i) for i in line.strip()] for line in fileinput.input()]
    show()
    try:
        run()
    except Finished:
        pass
