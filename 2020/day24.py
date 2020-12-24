import operator as op
import re
from collections import Counter, deque
from functools import reduce
from typing import NamedTuple


class Hex(NamedTuple):
    x: int
    y: int
    z: int


def move(h, direction):
    dx, dy, dz = (0, 0, 0)
    if direction == "ne":
        dx = 1
        dz = -1
    elif direction == "nw":
        dy = 1
        dz = -1
    elif direction == "w":
        dx = -1
        dy = 1
    elif direction == "sw":
        dx = -1
        dz = 1
    elif direction == "se":
        dz = 1
        dy = -1
    elif direction == "e":
        dx = 1
        dy = -1
    else:
        raise ValueError(f"Invalid direction {direction}")

    return h._replace(x=h.x + dx, z=h.z + dz, y=h.y + dy)


def neighbors(h):
    n = set()
    for direction in ("ne", "nw", "sw", "se", "e", "w"):
        n.add(move(h, direction))
    assert len(n) == 6
    return n


def read(env):
    if env == 1:
        fname = "day24.txt"
    elif env == 0:
        fname = "day24_test.txt"
    elif env == 2:
        fname = "dat24_test2.txt"
    else:
        raise FileNotFoundError

    with open(fname) as f:
        data = [parse(line.strip()) for line in f]
    return data


def flip(color):
    if color == "black":
        return "white"
    return "black"


def run(env):
    data = read(env)
    current_tile = Hex(0, 0, 0)
    tiles = {current_tile: "white"}
    for line in data:
        current_tile = Hex(0, 0, 0)
        for direction in line:
            current_tile = move(current_tile, direction)
        if current_tile in tiles:
            tiles[current_tile] = flip(tiles[current_tile])
        else:
            tiles[current_tile] = "black"
    blacks = 0
    for _, color in tiles.items():
        if color == "black":
            blacks += 1
    print("blacks:", blacks)
    # print(tiles)
    print(len(tiles))
    animate(tiles, 100)


def animate(tiles, days):
    for day in range(1, days + 1):
        new_tiles = {}
        total_tiles = {}
        for tile, color in tiles.items():
            total_tiles[tile] = color
        for tile, _ in tiles.items():
            for n in neighbors(tile):
                if n not in total_tiles:
                    total_tiles[n] = "white"
        for tile, tile_color in total_tiles.items():
            if tile_color == "black":
                black_ns = 0
                for n in neighbors(tile):
                    color = tiles.get(n, "white")
                    if color == "black":
                        black_ns += 1
                if black_ns == 0 or black_ns > 2:
                    new_tiles[tile] = "white"
                else:
                    new_tiles[tile] = "black"
            if tile_color == "white":
                black_ns = 0
                for n in neighbors(tile):
                    color = tiles.get(n, "white")
                    if color == "black":
                        black_ns += 1
                if black_ns == 2:
                    new_tiles[tile] = "black"
                else:
                    new_tiles[tile] = "white"

        blacks = 0
        for _, color in new_tiles.items():
            if color == "black":
                blacks += 1
        print("day: ", day, "blacks:", blacks)
        tiles = new_tiles
    return tiles


def parse(string):
    return re.findall(r"(nw|ne|sw|se|w|e)", string)


if __name__ == "__main__":
    run(2)
    run(1)
    run(0)
