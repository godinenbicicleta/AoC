from typing import NamedTuple, Optional, Tuple

with open("data/day24_test.txt") as f:
    data = [
        list(map(lambda x: list(map(lambda y: int(y.strip()), x.split(", "))), line.strip().split(" @ "))) for line in f
    ]


class Position(NamedTuple):
    x: int
    y: int
    z: int


class Velocity(NamedTuple):
    vx: int
    vy: int
    vz: int


class Point(NamedTuple):
    p: Position
    v: Velocity

    @property
    def x(self):
        return self.p.x

    @property
    def y(self):
        return self.p.y

    @property
    def z(self):
        return self.p.z

    @property
    def vx(self):
        return self.v.vx

    @property
    def vy(self):
        return self.v.vy

    @property
    def vz(self):
        return self.v.vz

    def at(self, t):
        p = Position(x=self.x + t * self.vx, y=self.y +
                     t * self.vy, z=self.z + t * self.vz)
        v = self.v
        return Point(p=p, v=v)

    @property
    def m(self) -> Optional[float]:
        x1 = self.x
        x2 = self.x + self.vx
        y1 = self.y
        y2 = self.y + self.vy
        if self.vx == 0:
            return None
        m = (y2 - y1) / (x2 - x1)
        return m

    @property
    def b(self) -> Optional[float]:
        x1 = self.x
        x2 = self.x + self.vx
        y1 = self.y
        y2 = self.y + self.vy
        if x2 == x1:
            return None
        return y1 - (y2 - y1) * x1 / (x2 - x1)

    def vfor(self, p: Position) -> Velocity:
        return Velocity(vx=p.x - self.x, vy=p.y - self.y, vz=p.z - self.z)


points = []

for x, v in data:
    p = Position(x=x[0], y=x[1], z=x[2])
    v = Velocity(vx=v[0], vy=v[1], vz=v[2])
    point = Point(p=p, v=v)
    points.append(point)


def intersects3D(p1: Point, p2: Point) -> Position:
    xy = intersects2D(p1, p2)
    if not xy:
        return None
    p1 = Point(
        p=Position(x=p1.y, y=p1.z, z=-1),
        v=Velocity(vx=p1.vy, vy=p1.vz, vz=-1)
    )
    p2 = Point(
        p=Position(x=p2.y, y=p2.z, z=-1),
        v=Velocity(vx=p2.vy, vy=p2.vz, vz=-1)
    )
    yz = intersects2D(p1, p2)
    if not yz:
        return None
    x, y = xy
    y_, z = yz
    assert abs(y - y_)/abs(y) < .0000001, f"{y}, {y_}"
    return Position(x=x, y=y, z=z)


def intersects2D(p1: Point, p2: Point) -> Optional[Tuple[float, float]]:
    m1 = p1.m
    m2 = p2.m
    b1 = p1.b
    b2 = p2.b
    if m1 == m2:
        if b1 == b2:
            t = (-p1.x + p2.x) / (p1.vx - p2.vx)
            return (p1.x + t * p1.vx, p1.y + t * p1.vy)
        return None
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return (x, y)


def intersections_in(points, minv, maxv):
    total = 0
    for i, p1 in enumerate(points):
        for p2 in points[i + 1:]:
            inter = intersects2D(p1, p2)
            if inter is None:
                continue
            x, y = inter
            if x < minv or x > maxv or y < minv or y > maxv:
                continue
            v1 = p1.vfor(Position(x=x, y=y, z=-1))
            v2 = p2.vfor(Position(x=x, y=y, z=-1))
            if v1.vx * p1.vx >= 0 and v1.vy * p1.vy >= 0 and v2.vx * p2.vx >= 0 and v2.vy * p2.vy >= 0:
                total += 1

    return total


print(intersections_in(points, 7, 27))
