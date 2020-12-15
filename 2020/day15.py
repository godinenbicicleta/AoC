from collections import defaultdict, deque
from functools import partial


def run(limit):
    num_turn = defaultdict(partial(deque, maxlen=2))
    nums = [None] * (limit + 1)
    # data = [int(k) for k in "0,3,6".split(",")]
    data = [int(k) for k in "1,0,16,5,17,4".split(",")]
    print(data)
    for turn in range(1, limit):
        if data:
            num = data.pop(0)
            num_turn[num].append(turn)
            nums[turn] = num

        else:
            num = nums[turn - 1]
            try:
                prev_turn, last_turn = num_turn[num]
                new_num = last_turn - prev_turn
            except ValueError:
                new_num = 0
            num_turn[new_num].append(turn)
            nums[turn] = new_num

    print(nums[limit - 1])


if __name__ == "__main__":
    import time

    t0 = time.time()
    # run(2021)
    run(30000001)
    print(time.time() - t0)
