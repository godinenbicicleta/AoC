from typing import Any
import fileinput
import re
from typing import NamedTuple
from collections import defaultdict, Counter


class Blueprint(NamedTuple):
    id: int
    ore: dict
    clay: dict
    obsidian: dict
    geode: dict


blueprints = []
pattern = r"Each (ore|clay|obsidian|geode) robot costs (\d+) (ore|clay|obsidian|geode)\.?( and (\d+) (ore|clay|obsidian|geode)\.?)?"
for line in fileinput.input(files=('data/day19_test.txt',)):
    matches = [[k for k in i if k] for i in re.findall(pattern, line)]
    ore = {}
    clay = {}
    obsidian = {}
    geode = {}
    for m in matches:
        for d, k in zip((ore, clay, obsidian, geode), ('ore', 'clay', 'obsidian', 'geode')):
            if m[0] == k:
                d[m[2]] = int(m[1])
                if len(m) > 3:
                    d[m[-1]] = int(m[-2])

    bid = re.match(r"Blueprint (\d+):", line).groups()[0]
    blueprints.append(Blueprint(id=int(bid), ore=ore,
                      obsidian=obsidian, geode=geode, clay=clay))

cache = {}


def _get_options(b, resources):
    ckey = (b.id, tuple(sorted(resources.items())))
    if ckey in cache:
        return cache[ckey]
    res = set([()])
    for key, value in b._asdict().items():
        if key == "id":
            continue
        valid = True
        new_resources = resources.copy()
        for k, v in value.items():
            if resources.get(k, 0) < v:
                valid = False
                break
            new_resources[k] -= v
        if valid:
            for option in get_options(b, new_resources):
                new_local = tuple(sorted([*option, key]))
                res.add(new_local)
    res = [dict(Counter(o)) for o in res]
    geodes = [i for i in res if 'geode' in res]
    if geodes:
        if any(i['geode'] > 1 for i in geodes):
            return None
        res = [('geode',)]
        cache[ckey] = res
        return res
    obsidians = [i for i in res if 'obsidian' in res]
    if obsidians:
        if any(i['obsidian'] > 1 for i in obsidians):
            return None
        res = [('obsidian',)]
        cache[ckey] = res
        return res

    return res


def get_options(b, resources):
    res = [()]
    for key, value in b._asdict().items():
        if key == "id":
            continue
        valid = True
        for k, v in value.items():
            if resources.get(k, 0) < v:
                valid = False
                break
        if valid:
            res.append((key,))
    for elem in res:
        if elem == ('geode',):
            return [('geode',)]
    for elem in res:
        if elem == ('obsidian', ):
            return [('obsidian', )]
    return res


class State(NamedTuple):
    time: int
    robots: dict
    resources: dict
    parent: Any

    @property
    def key(self) -> tuple:
        elements = [tuple(sorted(self.robots.items())), "", tuple(
            sorted(self.resources.items()))]
        return tuple(elements)

    @property
    def score(self) -> int:
        return self.resources.get('geode', 0)

    @property
    def robot_score(self) -> int:
        return self.robots.get('geode', 0)

    @property
    def sort_keys(self) -> int:
        return (self.resources.get('geode', 0), self.robots.get('geode', 0),
                self.resources.get(
                    'obsidian', 0), self.robots.get('obsidian', 0),
                self.resources.get('clay', 0), self.robots.get('clay', 0)
                )


def too_many_resources(resources: dict, b: Blueprint, robots: dict) -> bool:
    resources = resources.copy()
    costs = [getattr(b, k)for k in ('ore', 'clay', 'obsidian', 'geode')]
    if robots.get('clay', 0) > max(costs, key=lambda x: x.get('clay', 0))['clay']:
        return True

    if robots.get('ore', 0) > max(costs, key=lambda x: x.get('ore', 0))['ore']:
        return True
    if robots.get('obsidian', 0) > max(costs, key=lambda x: x.get('obsidian', 0))['obsidian']:
        return True
    return False


def get_score(b: Blueprint, maxT: int) -> int:
    start_state = State(time=0, robots={"ore": 1}, resources={}, parent=None)
    states = [start_state]
    maxScore = 0
    seen = {}
    seen_t = {}
    maxState = start_state
    while states:
        states.sort(key=lambda x: x.sort_keys)
        state = states.pop()
        if too_many_resources({}, b, state.robots):
            pass
        t = state.time + 1
        if state.score > maxScore:
            maxScore = state.score
            maxState = state
            print(maxScore)
        else:
            pass
        if t == maxT:
            continue

        # spend if possible
        options = get_options(b, state.resources)
        if options is None:
            continue

        # generate resources
        generated_resources = state.robots.copy()

        # compute new states
        for new_robots in options:
            new_state_robots = defaultdict(int)
            new_resources = defaultdict(int)
            for key, value in state.resources.items():
                new_resources[key] += value
            for robot_type in new_robots:
                new_state_robots[robot_type] += 1
                cost_dict = getattr(b, robot_type)
                for key, value in cost_dict.items():
                    new_resources[key] -= value
            if too_many_resources(new_resources, b, state.robots):
                pass
            for key, value in generated_resources.items():
                new_resources[key] += value
                new_state_robots[key] += value
            new_state = State(time=t, robots=new_state_robots,
                              resources=new_resources, parent=state)
            # check if we have seen this state at a previous time
            if new_state.key in seen and seen[new_state.key] <= t:
                pass
#            if seen_t.get(t, 0) > state.score:
#                continue  # continue
            seen_t[t] = state.score
            seen[new_state.key] = t
            states.append(new_state)
    return maxState


#total = 0
maxStates = {}
# for (i, blueprint) in enumerate(blueprints, start=1):
#    print("RUNNING FOR ", i)
#    maxStates[i] = get_score(blueprint, 25)
#    score = maxStates[i].score
#    print(score)
#    total += i * score
#
#print("== ", total, "==")
#
total = 1
maxStates = {}
for (i, blueprint) in enumerate(blueprints, start=1):
    print("RUNNING FOR ", i)
    maxStates[i] = get_score(blueprint, 33)
    score = maxStates[i].score
    print(i, "=>", score)
    total *= score
    break

print("== ", total, "==")
