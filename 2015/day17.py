containers = [11, 30, 47, 31, 32, 36, 3, 1, 5, 3, 32, 36, 15, 11, 46, 26, 28, 1, 19, 3]

containers = [20, 15, 10, 5, 5]
# containers = [10, 5, 5]


conts = [(i, c) for i, c in enumerate(containers)]

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
    elif liters > sum((v for k, v in conts)):
        res = []
    else:
        res = []
        possible_conts = [(k, v) for k, v in conts if v <= liters]
        for key, value in possible_conts:
            lv = liters - value
            rem = [(k, v) for k, v in possible_conts if key != k]
            if lv > 0:
                rem2 = [(k, v) for k, v in rem if v <= lv]
                if lv <= sum((v for k, v in rem2)):
                    for m in make(lv, rem2):
                        sol = [(key, value)] + m
                        res.append(sol)
            elif liters - value == 0:
                res.append([(key, value)])

            if liters <= sum((v for k, v in rem)):
                res.extend(make(liters, rem))

    res = list(dedup(res)) if res else res

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
m = make(25, conts)
# m = make(150, conts)
print(time.time() - t)
print(m)
print(len(m))
# print(results_map)
assert make(0, [(0, 1)]) == []
assert make(10, []) == []
assert make(10, [(0, 10)]) == [[(0, 10)]]
assert make(10, [(0, 10), (0, 15)]) == [[(0, 10)]]
