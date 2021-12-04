import sys

with open(sys.argv[1], "r") as f:
    text_blocks = f.read().strip().split("\n\n")


class Bingo:
    def __init__(self, nums):
        self.rows = {k: set(v) for k, v in zip(range(5), nums)}
        self.cols = {k: set() for k in range(5)}
        for row in nums:
            for col, num in enumerate(row):
                self.cols[col].add(num)
        self.nums = nums

    def finished(self, nums):
        for elem in (self.rows, self.cols):
            for row in elem.values():
                if row.issubset(nums):
                    return True
        return False

    def __str__(self):
        return "\n".join(" ".join(map(str, r)) for r in self.nums)


nums = [int(k) for k in text_blocks[0].strip().split(",")]
bingos = [t.split("\n") for t in text_blocks[1:]]
bingos = list(map(lambda x: [[int(m) for m in y.split(" ") if m] for y in x], bingos))

bingos = [Bingo(nums) for nums in bingos]

print("nums: ", nums)
print("bingos: \n")
print(bingos[0])
print(len(bingos))


won = set()


def play():
    i = 1
    while i <= len(nums):
        current = set(nums[:i])
        for ix, bingo in enumerate(bingos):
            if ix in won:
                continue

            if bingo.finished(current):
                won.add(ix)
                sum_unmarked = sum(
                    [i for k in bingo.nums for i in k if i not in current]
                )
                if len(won) == 1 or len(won) == len(bingos):
                    print(sum_unmarked * nums[i - 1])
        i += 1


play()
