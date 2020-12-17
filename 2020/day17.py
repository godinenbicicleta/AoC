from dataclasses import dataclass


def get_layer1(data):
    layer = dict()
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            layer[(x, y, 0)] = col
    return layer


def get_layer2(data):
    layer = dict()
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            layer[(x, y, 0, 0)] = col
    return layer


def run(env):
    fname = "day17.txt" if env else "day17_test.txt"
    with open(fname) as f:
        data = [line.strip() for line in f]

    print("neighbors (0,0,0): ", len(neighbors1(*(0, 0, 0))))

    l = cycle(get_layer1(data), 6, neighbors1)
    print("===")
    for y in range(-3, 5):
        for x in range(-3, 5):
            print(l[(x, y, 0)], end="")
        print()
    total = 0
    for point, value in l.items():
        if value == "#":
            total += 1
    print(total)

    l = cycle(get_layer2(data), 6, neighbors2)
    print("===")
    for y in range(-3, 5):
        for x in range(-3, 5):
            print(l[(x, y, 0, 0)], end="")
        print()
    total = 0
    for point, value in l.items():
        if value == "#":
            total += 1
    print(total)


def cycle(layer, num, neighbors):
    """
    During a cycle, all cubes simultaneously change their state according to the following rules:

    - If a cube is active and exactly 2 or 3 of its neighbors are also active,
    the cube remains active. Otherwise, the cube becomes inactive.

    - If a cube is inactive but exactly 3 of its neighbors are active,
    the cube becomes active. Otherwise, the cube remains inactive.

    """
    # for y in range(0, 3):
    #    for x in range(0, 3):
    #        print(layer[(x, y, 0)], end="")
    #    print()

    for turn in range(num):
        print("turn: ", turn)
        points = layer.copy()
        for _ in range(1):
            lp = list(points.keys())
            for p in lp:
                ns = set(neighbors(*p))
                for ne in ns:
                    if ne not in points:
                        points[ne] = "."
        active = set(k for k, v in points.items() if v == "#")
        inactive = set(k for k, v in points.items() if v == ".")
        # print("active: ", active)
        nl = dict(points)
        for point, value in points.items():
            ns = set(neighbors(*point))
            if len(ns & active) in (2, 3) and value == "#":
                nl[point] = "#"
            elif value == "#":
                nl[point] = "."
            elif len(ns & active) == 3 and value == ".":
                nl[point] = "#"
            elif value == ".":
                nl[point] = "."
            else:
                raise ValueError
        layer = nl.copy()
        # print(f"============= turn {turn + 1}  ============")
        # for y in range(-3, 5):
        #    for x in range(-3, 5):
        #        print(layer[(x, y, 0)], end="")
        #    print()

    return layer


def neighbors1(x, y, z):
    n = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if any((dx, dy, dz)):
                    n.append((x + dx, y + dy, z + dz))
    return n


def neighbors2(x, y, z, w):
    n = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dw in (-1, 0, 1):
                    if any((dx, dy, dz, dw)):
                        n.append((x + dx, y + dy, z + dz, w + dw))
    return n


if __name__ == "__main__":
    # run(0)
    import time

    t0 = time.time()
    run(1)
    print("time: ", time.time() - t0)
