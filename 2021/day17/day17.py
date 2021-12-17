from dataclasses import dataclass


@dataclass
class P:
    x: int
    y: int
    vx: int
    vy: int


def movex(x, vx):
    x = x + vx

    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1
    else:
        pass
    return x, vx


def move(p):
    x = p.x + p.vx
    vx = p.vx
    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1
    else:
        pass
    y = p.y + p.vy
    vy = p.vy - 1
    res = P(x=x, y=y, vx=vx, vy=vy)
    return res


@dataclass
class T:
    minx: int
    maxx: int
    miny: int
    maxy: int


def solve(target):
    solvesx = set()
    solves = set()
    for v0x in range(1, target.maxx * 2):
        x, vx = 0, v0x
        t = 0
        while vx != 0 and x < target.maxx:
            t += 1
            x, vx = movex(x, vx)
            if x >= target.minx and x <= target.maxx:
                solvesx.add(v0x)
                break
    ts = {}
    for v0x in solvesx:
        for v0y in range(-abs(target.miny * 2), abs(target.miny * 2)):
            y, vy = 0, v0y
            x, vx = 0, v0x
            p = P(x, y, vx, vy)
            t = 0
            trajectory = [p]
            while True:
                if p.y <= target.miny:
                    break
                if p.x >= target.maxx:
                    break
                if p.vx == 0 and (p.x < target.minx or p.x > target.maxx):
                    break
                t += 1
                p = move(p)
                trajectory.append(p)
                if (
                    p.x <= target.maxx
                    and p.x >= target.minx
                    and p.y >= target.miny
                    and p.y <= target.maxy
                ):
                    if (v0x, v0y) not in ts:
                        ts[(v0x, v0y)] = []
                    solves.add((v0x, v0y))
                    ts[(v0x, v0y)].append(trajectory)
                    trajectory = trajectory[:]
    return solves, ts


def run(minx, maxx, miny, maxyy):
    solves, ts = solve(T(minx, maxx, miny, maxyy))
    maxY = 0
    maxv = None
    for (v0x, v0y), trs in ts.items():
        for t in trs:
            for p in t:
                if p.y > maxY:
                    maxY = p.y
                    maxv = (v0x, v0y)
    print(len(solves))
    print(maxY, maxv)


run(20, 30, -10, -5)
run(70, 96, -179, -124)
