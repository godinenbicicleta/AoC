import math
import operator
import re
from collections import deque


"""
2 * 3 + (4 * 5) becomes 26.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.


---part2---
1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
2 * 3 + (4 * 5) becomes 46.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
"""


def run(env):
    fname = "day18.txt" if env else "day18_test.txt"
    with open(fname) as f:
        data = [line.strip() for line in f]

    parsed = [parse(line.replace(" ", "")) for line in data]
    print(parsed)
    print(sum([i for k in parsed for i in k]))

    parsed2 = [parse2(line.replace(" ", "")) for line in data]
    print(parsed2)
    print(sum([i for k in parsed2 for i in k]))


def parse2(line):
    res = evaluate_brackets(line)
    return res


def evaluate_mult(line):
    nums = [int(i) for i in line if i != "*"]
    return [math.prod(nums)]


def evaluate_addition(line):
    if not re.findall(r"\+", ",".join([str(i) for i in line])):
        return evaluate_mult(line)
    else:
        s = [line[0]]
        l = deque(line[1:])
        while True:
            char = l.popleft()
            if char == "+":
                left = s.pop()
                right = l.popleft()
                s.append(operator.add(int(left), int(right)))
            else:
                s.append(char)
            if not l:
                break
    return evaluate_mult(s)


def evaluate_brackets(line_):

    if not re.findall(r"\(", ",".join([str(i) for i in line_])):
        return evaluate_addition(line_)

    s = []

    line = deque(list(line_))
    while line:
        char = line.popleft()
        if char != "(" and char != ")":
            s.append(char)
        elif char == "(":
            p = 0
            sub = []
            while line:
                c = line.popleft()
                if c == ")" and p == 0:
                    s.extend(parse2(sub))
                    break
                elif c == "(":
                    sub.append("(")
                    p += 1
                elif c == ")" and p:
                    sub.append(")")
                    p -= 1
                else:
                    sub.append(c)
    return evaluate_addition(s)


def parse(line):
    res = []
    for char in line:

        if char.isdigit():

            c = int(char)
            if not res:
                res.append(c)
            elif res[-1] == "(":
                res.append(c)
            elif res[-1] == "*":
                res.pop()
                left = res.pop()
                op = getattr(operator, "mul")
                res.append(op(left, c))
            elif res[-1] == "+":
                res.pop()
                left = res.pop()
                op = getattr(operator, "add")
                res.append(op(left, c))

        elif char == "*" or char == "+" or char == "(":
            res.append(char)
        elif char == ")":
            num = res.pop()
            res.pop()
            res.append(num)
        while True:
            if res and len(res) >= 3:
                if isinstance(res[-1], int) and (res[-2] == "*" or res[-2] == "+"):
                    print("op", res[-1])
                    o = "mul" if res[-2] == "*" else "add"
                    left = res.pop()
                    res.pop()
                    right = res.pop()
                    res.append(getattr(operator, o)(left, right))

                else:
                    break
            else:
                break
    return res


if __name__ == "__main__":
    run(0)
    run(1)
