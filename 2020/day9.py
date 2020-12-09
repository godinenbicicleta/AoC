from collections import deque

with open("day9.txt") as f:
    data = [int(line) for line in f]


class TotalQueue:
    def __init__(self):
        self._q = deque()
        self._total = 0

    @property
    def total(self):
        return self._total

    def append(self, num):
        self._q.append(num)
        self._total += num

    def popleft(self):
        self._total -= self._q.popleft()

    def __iter__(self):
        return iter(self._q)


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
    deq = TotalQueue()
    for num in data:
        deq.append(num)
        if deq.total == target:
            return list(deq)
        while deq.total > target:
            deq.popleft()


if __name__ == "__main__":
    target = run()
    print(target)
    loc = sorted(locate(target))
    print(loc[0] + loc[-1])
