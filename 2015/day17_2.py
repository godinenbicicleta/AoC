containers = [11, 30, 47, 31, 32, 36, 3, 1, 5, 3, 32, 36, 15, 11, 46, 26, 28, 1, 19, 3]

# containers = [20, 15, 10, 5, 5]
# containers = [10, 5, 5]


results_map = {}


def make(liters, conts):
    sorted_conts = tuple(sorted(conts))
    if (liters, sorted_conts) in results_map:
        return results_map[(liters, sorted_conts)]

    if liters == 0:
        res = []
    elif not conts:
        res = []
    elif liters < 0:
        res = []
    elif liters > sum(conts):
        res = []
    else:
        res = []
        possible_conts = [v for v in conts if v <= liters]
        seen = set()
        for key, value in enumerate(possible_conts):
            lv = liters - value
            rem = []
            for k, v in enumerate(possible_conts):
                if key == k:
                    continue
                if (key, k) in seen:
                    continue
                seen.add((k, key))
                seen.add((key, k))
                rem.append(v)
            if lv > 0:
                rem2 = [v for v in rem if v <= lv]
                if lv <= sum(rem2) and rem2:
                    for m in make(lv, rem2):
                        sol = [value] + m
                        res.append(sol)
            elif liters - value == 0:
                res.append([value])

    results_map[(liters, sorted_conts)] = res
    return res


def dedup(res):
    seen = set()
    for r in res:
        sorted_r = tuple(sorted(r))
        if sorted_r in seen:
            continue
        else:
            seen.add(sorted_r)
            yield list(sorted_r)


import time

t = time.time()
# m = make(25, containers)
m = make(150, containers)
print(time.time() - t)
# print(m)
print(len(m))
print(min(len(k) for k in m))
print(len([k for k in m if len(k) == 4]))
# print(results_map)
assert make(0, [1]) == []
assert make(10, []) == []
assert make(10, [10, 10]) == [[10], [10]]
assert make(10, [10, 15]) == [[10]]
