import fileinput
import re
from collections import defaultdict, deque


class Bot:
    def __init__(self, name: int):
        self.nums = []
        self.name = name

    def add(self, num):
        self.nums.append(num)
        self.nums.sort()
        if self.nums == [17, 61]:
            print(self.name)

    @property
    def low(self):
        return self.nums[0]

    @property
    def high(self):
        return self.nums[1]

    @property
    def ready(self):
        return len(self.nums) == 2

    def move(self):
        nums = self.nums
        self.nums = []
        return nums

    def __repr__(self):
        return f"Bot<id={self.name}>({self.nums})"


bots = {}
lines = deque()

outputs = defaultdict(list)
for line in fileinput.input():
    if line.startswith("value"):
        value, bot = re.match(r"value (\d+) goes to bot (\d+)", line).groups()
        value = int(value)
        bot = int(bot)
        if bot not in bots:
            bots[bot] = Bot(bot)
        bots[bot].add(value)
    else:
        lines.append(line.strip())


while lines:
    line = lines.popleft()
    bot_id, bot_or_output1, id1, bot_or_output2, id2 = re.match(
        r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)",
        line,
    ).groups()
    bot_id = int(bot_id)
    id1 = int(id1)
    id2 = int(id2)
    if bot_id not in bots or not bots[bot_id].ready:
        lines.append(line)
        continue
    low, high = bots[bot_id].move()
    if bot_or_output1 == "output":
        outputs[id1].append(low)
    if bot_or_output2 == "output":
        outputs[id2].append(high)
    if bot_or_output1 == "bot":
        if id1 not in bots:
            bots[id1] = Bot(id1)
        bots[id1].add(low)
    if bot_or_output2 == "bot":
        if id2 not in bots:
            bots[id2] = Bot(id2)
        bots[id2].add(high)
print(outputs[0][0] * outputs[1][0] * outputs[2][0])
