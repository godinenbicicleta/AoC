"""
Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
"""

from typing import NamedTuple
import math


class Position(NamedTuple):
    x: int = 0
    y: int = 0
    facing: str = "E"


with open("day12.txt") as f:
    data = [(int(l[1:]), l[0]) for l in f]


def move(pos, instruction):
    steps, i = instruction
    dx = 0
    dy = 0
    facing = pos.facing
    if i == "F":
        if facing == "E":
            dx = steps
        elif facing == "N":
            dy = steps
        elif facing == "S":
            dy = -1 * steps
        elif facing == "W":
            dx = -1 * steps
        return Position(pos.x + dx, pos.y + dy, pos.facing)
    if i == "N":
        return Position(pos.x, pos.y + steps, pos.facing)
    if i == "S":
        return Position(pos.x, pos.y - steps, pos.facing)
    if i == "E":
        return Position(pos.x + steps, pos.y, pos.facing)
    if i == "W":
        return Position(pos.x - steps, pos.y, pos.facing)
    if i == "L":
        return Position(pos.x, pos.y, turn(pos.facing, 360 - steps))
    if i == "R":
        return Position(pos.x, pos.y, turn(pos.facing, steps))


def turn(f, deg):
    deg = deg % 360
    d = {"N": 0, "S": 180, "E": 90, "W": 270}
    g = {v: k for k, v in d.items()}

    return g[(d[f] + deg) % 360]


def run():
    pos = Position()
    for instruction in data:
        pos = move(pos, instruction)
        print(pos)
    print("p1: ", abs(pos.x) + abs(pos.y))


def move2(s, w, instruction):
    steps, i = instruction
    if i == "N":
        return s, Position(w.x, w.y + steps)
    if i == "S":
        return s, Position(w.x, w.y - steps)
    if i == "E":
        return s, Position(w.x + steps, w.y)
    if i == "W":
        return s, Position(w.x - steps, w.y)
    if i == "R":
        theta = math.atan2(w.y, w.x)
        r = math.hypot(w.x, w.y)
        steps = theta - math.radians(steps)
        new_x = int(round(r * math.cos(steps)))
        new_y = int(round(r * math.sin(steps)))
        return s, Position(new_x, new_y)
    if i == "L":
        theta = math.atan2(w.y, w.x)
        r = math.hypot(w.x, w.y)
        steps = math.radians(steps) + theta
        new_x = int(round(r * math.cos(steps)))
        new_y = int(round(r * math.sin(steps)))
        return s, Position(new_x, new_y)
    if i == "F":
        return Position(s.x + steps * w.x, s.y + w.y * steps), w


def run2():
    ship = Position()
    wp = Position(x=10, y=1)
    print(ship, " ", wp)
    for instruction in data:
        ship, wp = move2(ship, wp, instruction)
        print(instruction, " => ", ship, " ", wp)
    print("p2: ", abs(ship.x) + abs(ship.y))


if __name__ == "__main__":
    run()
    run2()
