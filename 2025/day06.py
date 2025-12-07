import fileinput
import re
import functools
import operator


func_op = {"+": operator.add, "*": operator.mul}


def reduce(data):
    res = 0
    for i, nums in enumerate(data):
        nums = map(int, nums)
        res += functools.reduce(func_op[ops[i]], nums)
    return res


data = list(fileinput.input(encoding="utf-8"))
data1 = list(map(lambda x: re.split("\s+", x.strip()), data))

ops = data1.pop()
data.pop()
p1 = reduce(zip(*data1))

print(p1)

blocks = []
block = []
for col in zip(*data):
    if all(c in ("\n", " ") for c in col):
        blocks.append(block)
        block = []
        continue
    col = (c.strip() for c in col)

    block.append("".join(col))
p2 = reduce(blocks)
print(p2)
