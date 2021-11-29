import math


def to_key(nums, res, size, goal):
    nums = tuple(sorted(nums))
    res = tuple(tuple(sorted(r)) for r in res)
    return (nums, res, size, goal)


memory = {}


def _combs(nums, res, size, goal):
    key = to_key(nums, res, size, goal)
    if key in memory:
        return memory[key]
    if not nums:
        return res
    new_res = res[:]

    rest = nums[1:]
    # with

    csa = _combs(rest, res, size=size - 1, goal=goal - nums[0])
    a = [c + [nums[0]] for c in csa]

    new_res += [m for m in a if len(m) <= size]

    # without
    if rest:
        b = _combs(rest, res, size=size, goal=goal)
        new_res += [k for k in b if len(k) == size and k not in new_res]
    memory[key] = [m for m in new_res if len(m) == size and sum(m) == goal] or [[]]
    return memory[key]


def combs(nums, size=None, goal=0):
    res = _combs(nums, [[]], size=size or len(nums), goal=goal)
    if size and goal:
        return [c for c in res if len(c) == size and sum(c) == goal]
    return res


weights = [
    1,
    3,
    5,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
]

for i in range(1, 10):
    res = combs(weights, i, sum(weights) // 3)
    if res:
        g = min(res, key=lambda x: math.prod(x))
        print(g)
        print(math.prod(g))
        break

for i in range(1, 10):
    res = combs(weights, i, sum(weights) // 4)
    if res:
        g = min(res, key=lambda x: math.prod(x))
        print(g)
        print(math.prod(g))

        break
