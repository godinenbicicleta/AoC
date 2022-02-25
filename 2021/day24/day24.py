from collections import defaultdict

# In [63]: inps = [Inp([w], 0) for w in range(1,10, 1)]
#    ...: while inps:
#    ...:     inp = heappop(inps)
#    ...:     #print(inp)
#    ...:     #print('no\t',inp.num)
#    ...:     if len(inp.ws) == 14 and new_z == 0:
#    ...:         print(inp.num)
#    ...:         continue
#    ...:
#    ...:
#    ...:     new_z = run(inp.ws[-1], len(inp.ws)-1, inp.current_z)
#    ...:     for w in range(1, 10, 1):
#    ...:         new_inp = Inp(inp.ws + [w], new_z)
#    ...:         if len(new_inp.ws) == 14 and new_z != 0:
#    ...:             continue
#    ...:         heappush(inps, new_inp)
#    ...:

d = """
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 2
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -7
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 16
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -4
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
"""


t0 = time.time()


def run():
    arr = []
    current = []
    for line in d.strip().split("\n"):
        line = line.strip().split(" ")
        if len(line) == 2:
            if current:
                arr.append(current)
            current = [line]
        else:
            current.append(line)
    arr.append(current)
    parsed = []
    for seq in arr:
        parsed.append(parse(seq))

    return parsed


def parse_int(i, d):
    try:
        return int(i)
    except ValueError:
        return d[i]


ops = {
    "mul": lambda x, y: x * y,
    "add": lambda x, y: x + y,
    "div": lambda x, y: x // y,
    "mod": lambda x, y: x % y,
    "eql": lambda x, y: int(x == y),
}


def parse(s):
    def p(w, z):
        d = {"x": 0, "y": 0, "z": z, "w": w}
        for elem in s:
            if elem[0] == "inp":
                d["w"] = w
                continue
            left = d[elem[1]]
            right = parse_int(elem[2], d)
            op = ops[elem[0]]
            d[elem[1]] = op(left, right)
        return d

    return p


mini = 13

runs = run()
zs = defaultdict(set)
zs[0] = {0}
zs[13] = set(range(30))
zs[12] = set(range(1000))
for i in range(1, 12):
    print(i)
    for w in range(1, 10):
        for z in zs[i - 1]:
            res = runs[i - 1](w, z)["z"]
            zs[i].add((res))


goals = defaultdict(set)
goals[13] = {0}
ws = defaultdict(set)
for i in range(13, -1, -1):
    print(i)
    for w in range(1, 10):
        for z in zs[i]:
            res = runs[i](w, z)["z"]
            if res in goals[i]:
                ws[i].add(w)
                goals[i - 1].add(z)

solutions = set()


def solves(i=13, goal=0, ww=None):
    if ww is None:
        ww = ()
    prog = runs[i]
    for w in ws[i]:
        for z in goals[i - 1]:
            res = prog(w, z)
            if res["z"] == goal:
                if i == 0:
                    solutions.add(int("".join(map(str, (w,) + ww))))
                else:
                    solves(i - 1, z, (w,) + ww)


if __name__ == "__main__":
    import time

    solves()
    sorted_sols = sorted(solutions)
    print(sorted_sols[-1], sorted_sols[0])
    print(time.time() - t0)
