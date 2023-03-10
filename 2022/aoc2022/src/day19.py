from typing import NamedTuple


class Resources(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


class Robots(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


class Cost(NamedTuple):
    ore: Resources = Resources(ore=4)
    clay: Resources = Resources(ore=2)
    obsidian: Resources = Resources(ore=3, clay=14)
    geode: Resources = Resources(ore=2, obsidian=7)


class Round(NamedTuple):
    i: int = 0
    resources: Resources = Resources()
    robots: Robots = Robots(ore=1)


def can_buy(resources: Resources, cost: Resources) -> bool:
    for field in Resources._fields:
        if getattr(resources, field) < getattr(cost, field):
            return False
    return True


def minus_cost(resources: Resources, cost: Resources) -> Resources:
    data = {}
    for field in Resources._fields:
        data[field] = getattr(resources, field) - getattr(cost, field)
    nr = Resources(**data)
    return nr


def add_robot(robots: Robots, robot: str) -> Robots:
    rs = robots._asdict()
    rs[robot] += 1
    return Robots(**rs)


def add_resources(left: Resources, right: Robots) -> Resources:
    left = left._asdict()
    right = right._asdict()
    res = {}
    for key in left:
        res[key] = left[key] + right[key]
    return Resources(**res)


def run(cost: Cost) -> int:

    cutoff = 32
    res = 0
    seen = {}
    states = [Round()]
    while states:
        state = states.pop()
        if state.i not in seen:
            seen[state.i] = (state.resources.geode, state.robots.geode)
        else:
            seen_geode_re, seen_geode_ro = seen[state.i]
            if seen_geode_re > state.resources.geode and seen_geode_ro > state.robots.geode:
                continue
            if state.resources.geode > seen_geode_re and state.robots.geode > seen_geode_ro:
                seen[state.i] = (state.resources.geode, state.robots.geode)
        round_no = state.i + 1
        if round_no > cutoff:
            if state.resources.geode > res:
                res = state.resources.geode
            continue

        # spend resources
        resources = state.resources
        robots = state.robots

        # 1. do nothing
        new_resources = [resources]
        new_robots = [robots]

        # 2. try to buy geode
        for field in ("geode", "obsidian", "clay", "ore"):
            if can_buy(resources, getattr(cost, field)):
                new_resources.append(minus_cost(
                    resources, getattr(cost, field)))
                new_robots.append(add_robot(robots, field))
                if field == "geode":  # or field == "obsidian":
                    new_resources.pop(0)
                    new_robots.pop(0)
                    break
                last_robots = new_robots[-1]
                if field == "clay" and all(
                   last_robots.clay > c for c in (cost.geode.clay, cost.obsidian.clay, cost.ore.clay, cost.clay.clay)
                   ):
                    new_robots.pop()
                    new_resources.pop()
                if field == "ore" and all(
                            last_robots.ore > c for c in (cost.geode.ore, cost.obsidian.ore, cost.ore.ore, cost.clay.ore)
                ):
                    new_robots.pop()
                    new_resources.pop()
                if field == "obsidian" and all(
                            last_robots.obsidian > c for c in (cost.geode.obsidian, cost.obsidian.obsidian, cost.ore.obsidian, cost.clay.obsidian)
                ):
                    new_robots.pop()
                    new_resources.pop()

                    # collect resources
        new_resources = [add_resources(r, robots) for r in new_resources]

        for resource, robot in zip(new_resources, new_robots):
            states.append(Round(round_no, resources=resource, robots=robot))
    return res


# Blueprint 2:
#  Each ore robot costs 2 ore.
#  Each clay robot costs 3 ore.
#  Each obsidian robot costs 3 ore and 8 clay.
#   Each geode robot costs 3 ore and 12 obsidian.
# Blueprint 2: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 20 clay. Each geode robot costs 2 ore and 20 obsidian.
# Blueprint 3: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 16 clay. Each geode robot costs 3 ore and 9 obsidian.
if __name__ == "__main__":
    res = 1
    costs = [
        Cost(ore=Resources(ore=2), clay=Resources(ore=4), obsidian=Resources(
            ore=4, clay=20), geode=Resources(ore=3, obsidian=14)),
        Cost(ore=Resources(ore=3), clay=Resources(ore=3), obsidian=Resources(
            ore=2, clay=20), geode=Resources(ore=2, obsidian=20)),
        Cost(ore=Resources(ore=3), clay=Resources(ore=3), obsidian=Resources(
            ore=3, clay=16), geode=Resources(ore=3, obsidian=9)),
    ]
    for cost in costs:
        print(cost)
        res *= run(cost)
    print(res)
