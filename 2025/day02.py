data = "6161588270-6161664791,128091420-128157776,306-494,510-1079,10977-20613,64552-123011,33-46,28076-52796,371150-418737,691122-766624,115-221,7426210-7504719,819350-954677,7713444-7877541,63622006-63661895,1370-1981,538116-596342,5371-8580,8850407-8965070,156363-325896,47-86,452615-473272,2012-4265,73181182-73335464,1102265-1119187,3343315615-3343342551,8388258268-8388317065,632952-689504,3-22,988344-1007943"

data = list(
    map(lambda x: (int(x[0]), int(x[1])), map(lambda x: x.split("-"), data.split(",")))
)

p1 = 0
for lo, hi in data:
    for num in range(lo, hi + 1):
        strnum = str(num)
        size = len(strnum)
        if (size % 2) == 0:
            left = strnum[: len(strnum) // 2]
            right = strnum[len(strnum) // 2 :]
            if left == right:
                p1 += num

print("part1: ", p1)


def invalid(num):
    for size in range(1, len(num) // 2 + 1):
        if len(num) % size != 0:
            continue
        chunks = []
        for start in range(0, len(num), size):
            chunks.append(num[start : start + size])
        inv = True
        for chunk in chunks[1:]:
            if chunk != chunks[0]:
                inv = False
                break
        if inv:
            return True


p2 = 0
for lo, hi in data:
    for num in range(lo, hi + 1):
        if invalid(str(num)):
            p2 += num
        num += 1

print("part2: ", p2)


print(sum(num for lo, hi in data for num in range(lo, hi + 1) if invalid(str(num))))
