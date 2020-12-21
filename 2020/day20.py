import re
from collections import deque
from copy import deepcopy
from functools import partial

with open("day20.txt") as f:
    data = f.read().split("\n\n")


def pprint(tile):
    print()
    print(rep(tile))
    print()


def rep(tile):
    joined = "\n".join("".join(c) for c in tile)
    return joined


def trim(tile):
    new_tile = [None for _ in range(len(tile) - 2)]
    for j, row in enumerate(tile[1:-1]):
        new_tile[j] = row[1:-1]
    return new_tile


td = {}
for raw_tile in data:
    name, *tiles = raw_tile.strip().split("\n")
    tile_id = int(re.findall(r"\d+", name)[0])
    td[tile_id] = [list(row) for row in tiles]

# print("tids: ", td.keys())

# pprint(td[2311])


def rotate(tile, num):
    tile = deepcopy(tile)

    if num == 2:
        new_tile = [None for _ in tile]
        for i, line in enumerate(tile[::-1]):
            new_tile[i] = line[::-1]
        return new_tile

    elif num == 1:
        new_tile = [[None for _ in tile[0]] for _ in tile]
        cols = tile[::-1]
        for i, y in enumerate(tile):
            for j, _ in enumerate(y):
                new_tile[i][j] = cols[j][i]
        return new_tile
    elif num == 3:
        new_tile = [[None for _ in tile[0]] for _ in tile]
        for y, row in enumerate(tile):
            for x, col in enumerate(row):
                new_tile[x][y] = tile[y][x]
        new_tile = new_tile[::-1]
        return new_tile
    else:
        raise ValueError

    return new_tile


def flip_vertical(tile):
    new_tile = [None for _ in tile]
    for i, line in enumerate(tile):
        new_tile[i] = line[::-1]
    return new_tile


def flip_horizontal(tile):
    new_tile = [None for _ in tile]
    for i, line in enumerate(tile[::-1]):
        new_tile[i] = line
    return new_tile


# pprint(rotate(td[1549]))

# pprint(flip_vertical(td[1549]))

# pprint(flip_horizontal(td[1549]))


def top(tile):
    return "".join(tile[0])


def bottom(tile):
    return "".join(tile[-1])


def left(tile):
    return "".join(r[0] for r in tile)


def right(tile):
    return "".join(r[-1] for r in tile)


rotations = [
    partial(rotate, num=1),
    partial(rotate, num=2),
    partial(rotate, num=3),
]

flips = [flip_vertical, flip_horizontal]


cache_compares = {}


def get_compares(id_, tile_):
    if id_ in cache_compares:
        return cache_compares[id_]
    compares = [tile_]
    for rot in rotations:
        compares.append(rot(tile_))
        for flip in flips:
            compares.append(flip(rot(tile_)))
            compares.append(flip(tile_))
            compares.append(rot(flip(tile_)))
            for flip2 in flips:
                if flip != flip2:
                    compares.append(flip(flip2(tile_)))
                    compares.append(rot(flip(flip2(tile_))))
                    compares.append(flip2(flip(tile_)))
                    compares.append(rot(flip2(flip(tile_))))
                    compares.append(flip2(rot(flip(tile_))))
                    compares.append(flip(rot(flip2(tile_))))
    cache_compares[id_] = compares
    return compares


def matches(id_, tile_, tiles, ms):
    ms[id_] = set()

    for tile in [tile_]:
        for i, match_ in tiles:
            for match in get_compares(i, match_):
                if top(tile) == bottom(match):
                    ms[id_].add(i)
                    continue

                if left(tile) == right(match):
                    ms[id_].add(i)
                    continue

                if right(tile) == left(match):
                    ms[id_].add(i)
                    continue
                if bottom(tile) == top(match):
                    ms[id_].add(i)
                    continue

    return matches


def get_match(tile, id2):
    tile2 = td[id2]
    for match in get_compares(id2, tile2):
        if top(tile) == bottom(match):
            return "tb", match
        if left(tile) == right(match):
            return "lr", match
        if right(tile) == left(match):
            return "rl", match
        if bottom(tile) == top(match):
            return "bt", match


product = 1
ms = {}
corners = []
for tile_id in td:
    matches(
        tile_id,
        td[tile_id],
        [(tid, tile) for tid, tile in td.items() if tid != tile_id],
        ms,
    )
    if len(ms[tile_id]) == 2:
        product *= tile_id
        corners.append(tile_id)

print(corners)


def solve(corner, start_tile):
    # place corner in (0,0)
    # build from there
    # if solution: return
    # else try with same corner reflected/rotated
    positions = {(0, 0): (corner, start_tile)}
    next_pos = deque([(0, 0)])
    while next_pos:
        # print(next_pos)
        current_position = next_pos.popleft()
        current_id = positions[current_position][0]
        current_tile = positions[current_position][1]
        neighbors = ms[current_id]
        for neighbor in neighbors:
            # tb, lr, rl, bt
            location, matched_tile = get_match(current_tile, neighbor)
            if location == "tb":
                new_pos = (current_position[0], current_position[1] + 1)
            elif location == "lr":
                new_pos = (current_position[0] - 1, current_position[1])
            elif location == "rl":
                new_pos = (current_position[0] + 1, current_position[1])
            elif location == "bt":
                new_pos = (current_position[0], current_position[1] - 1)
            else:
                raise ValueError

            if new_pos in positions and positions[new_pos][0] != neighbor:
                # print(f"new_pos {new_pos} exists in positions, {positions.keys()}")
                # print(
                #    f"positions[new_pos][0] = {positions[new_pos][0]} and not {neighbor}"
                # )
                raise StopIteration
            elif new_pos in positions:
                continue
            else:
                positions[new_pos] = (neighbor, matched_tile)
                next_pos.append(new_pos)
    return positions

    # tp, lr, rl, bt


"""
1951    2311    3079
2729    1427    2473
2971    1489    1171
"""
print(product)


def get_solution():
    for compare in cache_compares[corners[0]]:
        # print("trying with")
        # pprint(compare)
        try:
            return solve(corners[0], compare)
        except StopIteration:
            pass


def trim_sol(sol):
    parsed = dict()
    min_x = min(sol.keys(), key=lambda x: x[0])[0]
    #    min_y = min(sol.keys(), key=lambda x: x[1])[1]

    min_x = abs(min_x) if min_x <= 0 else min_x
    #   min_y = abs(min_y) if min_y <= 0 else min_y
    for pos, id_tile in sol.items():
        id, tile = id_tile
        parsed[(pos[0] + min_x, abs(pos[1]))] = (id, trim(tile))
    return parsed


def join_sol(sol):
    max_x = max(sol.keys(), key=lambda x: x[0])[0]
    max_y = max(sol.keys(), key=lambda x: x[1])[1]
    size = len(sol[(0, 0)][1])
    joined = [
        [None for _ in range((max_x + 1) * size)] for _ in range((max_y + 1) * size)
    ]

    for key, value in parsed_sol.items():
        x, y = key
        id, val = value
        for j, row in enumerate(val):
            for i, col in enumerate(row):
                joined[j + size * (max_y - y)][i + size * x] = col
    return joined


sol = get_solution()

parsed_sol = trim_sol(sol)

full_sol = join_sol(parsed_sol)
"""
01234567890123456789
00000000001111111111
..................#.
#....##....##....###
.#..#..#..#..#..#...
"""


def find_sea_monsters(tile):
    sea_monsters = 0
    size = len(tile)
    for i, row in enumerate(tile[:-2]):
        start = 0
        while start + 19 < size:
            if row[start + 18] == "#":
                row_below = tile[i + 1]
                if all(
                    row_below[start + c] == "#" for c in (0, 5, 6, 11, 12, 17, 18, 19)
                ):
                    row_below2 = tile[i + 2]
                    if all(row_below2[start + c] == "#" for c in (1, 4, 7, 10, 13, 16)):
                        sea_monsters += 1
            start += 1

    return sea_monsters


def get_sea_monsters(sol):
    sols = []

    for compare in get_compares(-1, sol):
        correct_sol = rep(compare)
        sea_monsters = find_sea_monsters(compare)
        if sea_monsters:
            print(f"found {sea_monsters} sea_monsters")
            sol = correct_sol.count("#") - sea_monsters * 15
            print("sol: ", sol)

            sols.append(sol)

    return sols


counted = get_sea_monsters(full_sol)
# 2194 too high
