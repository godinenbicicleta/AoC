import re

with open("day20_test.txt") as f:
    data = f.read().split("\n\n")


def pprint(tile):
    joined = "\n".join("".join(c) for c in tile)
    print()
    print(joined)
    print()


td = {}
for raw_tile in data:
    name, *tiles = raw_tile.strip().split("\n")
    tile_id = int(re.findall(r"\d+", name)[0])
    td[tile_id] = [list(row) for row in tiles]

# print("tids: ", td.keys())

# pprint(td[2311])


def rotate(tile):
    new_tile = [None for _ in tile]
    for i, line in enumerate(tile[::-1]):
        new_tile[i] = line[::-1]
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


def matches(tile_, tiles):
    total_tiles = [(i, rotate(t)) for i, t in tiles]
    total_tiles += [(i, flip_vertical(t)) for i, t in tiles]
    total_tiles += [(i, flip_horizontal(t)) for i, t in tiles]

    matches = set()

    for tile in [tile_, rotate(tile_), flip_vertical(tile_), flip_horizontal(tile_)]:
        for i, match in total_tiles:
            if (
                top(tile) == bottom(match)
                or top(tile)[::-1] == bottom(match)
                or top(tile) == top(match)
                or top(tile)[::-1] == top(match)
                or left(tile) == left(match)
                or left(tile)[::-1] == left(match)
                or left(tile) == right(match)
                or left(tile)[::-1] == right(match)
                or right(tile) == left(match)
                or right(tile)[::-1] == left(match)
                or right(tile) == right(match)
                or right(tile)[::-1] == right(match)
                or bottom(tile) == top(match)
                or bottom(tile)[::-1] == top(match)
                or bottom(tile) == bottom(match)
                or bottom(tile)[::-1] == bottom(match)
            ):
                matches.add(i)

    return matches


product = 1
for tile_id in td:
    ms = matches(
        td[tile_id], [(tid, tile) for tid, tile in td.items() if tid != tile_id]
    )
    print(tile_id, ms)
    if len(ms) == 2:
        product *= tile_id

"""
1951    2311    3079
2729    1427    2473
2971    1489    1171
"""

print(product)
