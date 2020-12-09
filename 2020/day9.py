from collections import deque


with open("day9.txt") as f:
    data = [int(line) for line in f]


def run():
    for ix, num in enumerate(data[25:]):
        broke = False
        prevd = data[ix : ix + 25]
        for prev1 in prevd:
            for prev2 in prevd:
                if prev2 != prev1 and prev1 + prev2 == num:
                    broke = True
                    break
            if broke:
                break
        else:
            return num


def locate(target):
    deq = deque()
    for num in data:
        deq.append(num)
        if sum(deq) == target:
            return list(deq)
        while sum(deq) > target:
            deq.popleft()


if __name__ == "__main__":
    target = run()
    print(target)
    loc = sorted(locate(target))
    print(loc[0] + loc[-1])
