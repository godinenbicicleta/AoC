import fileinput

nums = sorted(int(k) for k in next(fileinput.input()).strip().split(","))


def nsum(num, target):
    n = dif(num, target)
    return n * (n + 1) // 2


def dif(num, target):
    return abs(num - target)


def run(func):
    targets = range(nums[0], nums[-1] + 1)
    min_fuel = min(sum(func(t, n) for n in nums) for t in targets)
    print(min_fuel)


# part 1
run(dif)

# part 2
run(nsum)
