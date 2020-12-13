from collections import deque


def gen(x):
    pos = 0
    while True:
        yield pos
        pos = x + pos


def solve(timestamp, busses):
    queue = deque(list(zip(busses, map(gen, busses))))
    num = None
    bus = None
    res = []
    while queue:
        bus, g = queue.popleft()
        num = next(g)
        if num >= timestamp:
            res.append((num, bus))
        else:
            queue.append((bus, g))

    res.sort()
    num, bus = res[0]
    print(res)
    print("num: ", num)
    print("bus: ", bus)
    print(bus * (num - timestamp))


# 7,13,x,x,59,x,31,19
solve(939, [7, 13, 59, 31, 19])


data = "17,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,439,x,29,x,x,x,x,x,x,x,x,x,x,13,x,x,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,787,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,19"
busses = [int(d) for d in data.split(",") if d != "x"]
solve(1000067, busses)


# part 2
d = data.split(",")
offsets = [d.index(str(bus)) for bus in busses]

ix = 1
prod = 1
for bus, offset in zip(busses, offsets):
    while True:
        if (ix + offset) % bus == 0:
            prod *= bus
            break
        else:
            ix += prod
print(ix)
