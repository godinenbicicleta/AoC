with open("day11.txt") as f:
    data = [list(l.strip()) for l in f]


WIDTH = len(data[0])
HEIGHT = len(data)


def rep(data):
    print("\n".join("".join(d) for d in data))


def neighbors(p):
    y, x = p
    all_neighbors = [
        (y - 1, x),
        (y - 1, x - 1),
        (y - 1, x + 1),
        (y + 1, x),
        (y + 1, x - 1),
        (y + 1, x + 1),
        (y, x - 1),
        (y, x + 1),
    ]
    return [(y, x) for (y, x) in all_neighbors if 0 <= y < HEIGHT and 0 <= x < WIDTH]


def count(d):
    seats = 0
    for row in d:
        for col in row:
            if col == "#":
                seats += 1
    return seats


def move(d):
    new = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for y, row in enumerate(d):
        for x, col in enumerate(row):
            ns = neighbors([y, x])
            if col == ".":
                new[y][x] = col
            elif col == "L" and all(d[i][j] != "#" for i, j in ns):
                new[y][x] = "#"
            elif col == "#" and sum(1 for i, j in ns if d[i][j] == "#") >= 4:
                new[y][x] = "L"
            else:
                new[y][x] = col
    return new


def move2(d):
    new = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for y, row in enumerate(d):
        for x, col in enumerate(row):
            seats = find_seats([y, x], d)
            if col == ".":
                new[y][x] = col
            elif col == "L" and all(s != "#" for s in seats):
                new[y][x] = "#"
            elif col == "#" and sum(1 for s in seats if s == "#") >= 5:
                new[y][x] = "L"
            else:
                new[y][x] = col
    return new


def run(d):
    while True:
        # rep(d)
        print()
        prv = count(d)
        d = move(d)
        nw = count(d)
        if nw == prv:
            print(nw)
            break


def run2(d):
    while True:
        # rep(d)
        print()
        prv = count(d)
        d = move2(d)
        nw = count(d)
        if nw == prv:
            print(nw)
            break


def find_seats(p, data):
    y, x = p

    x1 = x - 1
    seats = []
    while x1 >= 0:
        if data[y][x1] in ("#", "L"):
            seats.append(data[y][x1])

            break
        x1 -= 1

    x2 = x + 1
    while x2 < WIDTH:
        if data[y][x2] in ("#", "L"):
            seats.append(data[y][x2])

            break
        x2 += 1

    y1 = y + 1
    while y1 < HEIGHT:
        if data[y1][x] in ("#", "L"):
            seats.append(data[y1][x])

            break
        y1 += 1

    y2 = y - 1
    while y2 >= 0:
        if data[y2][x] in ("#", "L"):
            seats.append(data[y2][x])

            break
        y2 -= 1

    xb, yb = x - 1, y - 1
    while xb >= 0 and yb >= 0:
        if data[yb][xb] in ("#", "L"):
            seats.append(data[yb][xb])

            break
        xb, yb = xb - 1, yb - 1

    xl, yu = x - 1, y + 1
    while xl >= 0 and yu < HEIGHT:
        if data[yu][xl] in ("#", "L"):
            seats.append(data[yu][xl])

            break
        xl, yu = xl - 1, yu + 1

    xa, ya = x + 1, y + 1
    while xa < WIDTH and ya < HEIGHT:
        if data[ya][xa] in ("#", "L"):
            seats.append(data[ya][xa])
            break
        xa, ya = xa + 1, ya + 1

    xu, yl = x + 1, y - 1
    while xu < WIDTH and yl >= 0:
        if data[yl][xu] in ("#", "L"):
            seats.append(data[yl][xu])
            break
        xu, yl = xu + 1, yl - 1

    return seats


print(count(data))
run(data)
run2(data)
