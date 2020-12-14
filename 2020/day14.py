import re
from collections import defaultdict

with open("day14.txt") as f:
    data = [line.strip() for line in f]

mem = [0] * 100000


def to_binary(num):
    binary = [0] * 36
    if num == 0:
        return binary
    for ix, i in enumerate(range(35, -1, -1)):
        if num // (2 ** i) > 0:
            binary[ix] = 1
            num -= 2 ** i
        else:
            binary[ix] = 0
    return binary


def match(mask, val):
    res = []
    for m, v in zip(mask, val):
        if m == "X":
            res.append(v)
        else:
            res.append(int(m))
    return res


def to_decimal(arr):
    res = 0
    for ix, i in enumerate(range(35, -1, -1)):
        res += arr[ix] * (2 ** i)
    return res


for num, line in enumerate(data):
    if num == 0 or line.startswith("mask"):
        mask = list(line.split(" = ")[1])
    if line.startswith("mem"):
        key = int(re.search(r"mem\[(\d+)\]", line).groups()[0])
        val = to_binary(int(line.split(" = ")[1]))
        mem[key] = to_decimal(match(mask, val))

print(sum(mem))


def transform(key, mask):
    modif = []
    for ix, value in enumerate(mask):
        if value == "1":
            key[ix] = 1
        elif value == "0":
            continue
        else:
            modif.append(ix)

    keys = [key]
    if not modif:
        return keys
    for ix in modif:
        new_keys = []
        for k in keys:
            new_key1, new_key2 = k[:], k[:]
            new_key1[ix] = 0
            new_key2[ix] = 1
            new_keys.append(new_key1)
            new_keys.append(new_key2)
        keys = new_keys
    return keys


mem = defaultdict()
for num, line in enumerate(data):
    if num == 0 or line.startswith("mask"):
        mask = list(line.split(" = ")[1])
    if line.startswith("mem"):
        key = int(re.search(r"mem\[(\d+)\]", line).groups()[0])
        val = int(line.split(" = ")[1])
        keys = transform(to_binary(key), mask)
        for key in keys:
            mem[to_decimal(key)] = val


print(sum(mem.values()))
