from heapq import heappop, heappush

input_grid = {
    (0, 0): ".",
    (1, 0): ".",
    (2, 0): ".",
    (3, 0): ".",
    (4, 0): ".",
    (5, 0): ".",
    (6, 0): ".",
    (7, 0): ".",
    (8, 0): ".",
    (9, 0): ".",
    (10, 0): ".",
    (2, 1): "B",
    (2, 2): "D",
    (4, 1): "A",
    (4, 2): "A",
    (6, 1): "B",
    (6, 2): "D",
    (8, 1): "C",
    (8, 2): "C",
}
test_grid = {
    (0, 0): ".",
    (1, 0): ".",
    (2, 0): ".",
    (3, 0): ".",
    (4, 0): ".",
    (5, 0): ".",
    (6, 0): ".",
    (7, 0): ".",
    (8, 0): ".",
    (9, 0): ".",
    (10, 0): ".",
    (2, 1): "B",
    (2, 2): "D",
    (2, 3): "D",
    (2, 4): "A",
    (4, 1): "C",
    (4, 2): "C",
    (4, 3): "B",
    (4, 4): "D",
    (6, 1): "B",
    (6, 2): "B",
    (6, 3): "A",
    (6, 4): "C",
    (8, 1): "D",
    (8, 2): "A",
    (8, 3): "C",
    (8, 4): "A",
}

pl = dict([("A", 2), ("B", 4), ("C", 6), ("D", 8)])


class Grid:
    def __init__(self, grid, energy=0, prev=None):
        self.grid = grid
        self.energy = energy
        self.prev = prev

    def __lt__(self, other):
        return self.energy + self.estimate < other.energy + other.estimate

    @staticmethod
    def get_real_distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        d = 0
        while y1 > 0:
            y1 -= 1
            d += 1
        return 2 * d + abs(x1 - x2)

    @property
    def estimate(self):
        total = 0
        for point in self.grid:
            if self.grid[point] not in "ABCD":
                continue
            letter = self.grid[point]
            x_goal = pl[letter]
            if point[0] == x_goal and point[1] > 0:
                continue
            goal = (x_goal, 1)
            total += Grid.get_real_distance(point, goal) * Grid.get_energy(letter)
        return total

    def get_letters_to_move(self):
        res = []
        grid = self.grid
        for point in self.grid:
            if grid[point] not in "ABCD":
                continue
            if point[0] == pl[grid[point]] and point[1] > 0:
                continue
            # position above is blocked
            points_above = [
                grid[(point[0], j)] != "." for j in range(point[1] - 1, -1, -1)
            ]
            if point[1] > 0 and any(points_above):
                continue
            # positions right or left are blocked
            if point[1] == 0 and (
                grid.get((point[0] + 1, 0), None) != "."
                and grid.get((point[0] - 1, 0), None) != "."
            ):
                continue
            # in hallway but dest room is not ready, then continue
            if point[1] == 0:
                if all(
                    grid[(pl[grid[point]], j)] in (grid[point], ".")
                    for j in (1, 2, 3, 4)
                ):
                    if self.path_clear(point, (2, 1)):
                        res.append(point)
                        continue
                    else:
                        continue
                else:
                    continue
            res.append(point)

        return sorted(res, key=lambda x: grid[x])

    def path_clear(self, point, goal):
        x, y = point
        gx, gy = goal
        grid = self.grid
        if grid[(gx, 0)] != ".":
            return False
        if x > gx:
            for c in range(gx, x, 1):
                if grid[c, 0] != ".":
                    return False
        if x < gx:
            for c in range(x + 1, gx + 1, 1):
                if grid[(c, 0)] != ".":
                    return False
        return True

    def solved(self):
        points = (
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
            (6, 1),
            (6, 2),
            (6, 3),
            (6, 4),
            (8, 1),
            (8, 2),
            (8, 3),
            (8, 4),
        )
        values = "AAAABBBBCCCCDDDD"
        return all(self.grid[p] == v for p, v in zip(points, values))

    def show(self):
        g = self.grid
        print(f"###-{self.energy}-###")
        print("#############")
        a = "".join(
            g[p]
            for p in (
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (4, 0),
                (5, 0),
                (6, 0),
                (7, 0),
                (8, 0),
                (9, 0),
                (10, 0),
            )
        )
        print(f"#{a}#")
        print(f"###{g[(2,1)]}#{g[4,1]}#{g[6,1]}#{g[8,1]}###")
        print(f"  #{g[(2,2)]}#{g[4,2]}#{g[6,2]}#{g[8,2]}#  ")
        print(f"  #{g[(2,3)]}#{g[4,3]}#{g[6,3]}#{g[8,3]}#  ")
        print(f"  #{g[(2,4)]}#{g[4,4]}#{g[6,4]}#{g[8,4]}#  ")
        print("  #########  ")

    def __str__(self):
        return "".join(map(str, sorted(self.grid.items())))

    def valid(self, point):
        return point in self.grid

    @staticmethod
    def can_stop(point):
        return point not in ((2, 0), (4, 0), (6, 0), (8, 0))

    @staticmethod
    def is_hallway(point):
        return point[0] == 0

    @staticmethod
    def is_room(point):
        return point[1] > 0

    @staticmethod
    def get_energy(letter):
        return {"A": 1, "B": 10, "C": 100, "D": 1000}[letter]

    @staticmethod
    def update(grid, updates):
        return {**grid, **updates}

    def get_left_right(self, point, current_energy, energy_delta):
        moves = 0
        x, y = point
        res = []
        while x > 0:
            x -= 1
            moves += 1
            if self.grid.get((x, y), None) != ".":
                break
            if self.can_stop((x, y)):
                res.append(((x, y), current_energy + energy_delta * moves))
        moves = 0
        x, y = point
        while x < 11:
            x += 1
            moves += 1
            if self.grid.get((x, y), None) != ".":
                break
            if self.can_stop((x, y)):
                res.append(((x, y), current_energy + energy_delta * moves))
        return res

    def move(self):
        energy = self.energy
        grid = self.grid.copy()
        for point in self.get_letters_to_move():
            letter = grid[point]
            point_energy = Grid.get_energy(letter)
            if Grid.is_room(point):
                new_energy = energy
                # move up to hallway
                x, y = point
                while y > 0:
                    y -= 1
                    new_energy += point_energy
                # move left or right
                for np, en in self.get_left_right((x, y), new_energy, point_energy):
                    yield Grid(
                        Grid.update(grid, {np: letter, point: "."}),
                        energy=en,
                        prev=self,
                    )
            else:
                # letter is in the hallway, needs to move to destination
                x_goal = pl[letter]
                for j in (4, 3, 2, 1):
                    if grid[(x_goal, j)] == ".":
                        goal = (x_goal, j)
                        break

                np = goal
                if grid[goal] != ".":
                    continue
                distance = abs(goal[0] - point[0]) + abs(goal[1] - point[1])
                yield Grid(
                    Grid.update(grid, {np: letter, point: "."}),
                    energy=energy + distance * point_energy,
                    prev=self,
                )


def run(g):
    gg = Grid(g)
    seen = {str(gg): gg.estimate}
    grids = [Grid(g)]
    i = 0
    dead = set()
    while grids:
        g = heappop(grids)
        print(g.energy + g.estimate)
        g.show()
        moves = [k for k in g.move() if str(k) not in dead]
        if not moves:
            dead.add(str(g))
        for new_g in moves:
            if new_g.solved():

                print(len(dead))
                print("------")
                return new_g
            # if str(new_g) in seen and seen[str(new_g)] < new_g.energy + new_g.estimate:
            #    continue
            # else:
            #    seen[str(new_g)] = new_g.energy + new_g.estimate
            heappush(grids, new_g)
        i += 1


if __name__ == "__main__":
    g = run(test_grid)
    # g = run(input_grid)
    res = [g]
    while g.prev is not None:
        res.append(g.prev)
        g = g.prev
    res = res[::-1]
    prev_energy = 0
    for r in res:
        print("energy delta", r.energy - prev_energy)
        r.show()
        prev_energy = r.energy
