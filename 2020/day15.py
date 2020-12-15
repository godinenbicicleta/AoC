from collections import defaultdict, deque
from functools import partial


def run(limit):
    num_turn = defaultdict(partial(deque, maxlen=2))
    # data = [int(k) for k in "0,3,6".split(",")]
    data = [int(k) for k in "1,0,16,5,17,4".split(",")]
    print(data)
    current = None
    prev = None
    for turn in range(1, limit):
        prev = current
        if data:
            num = data.pop(0)
            num_turn[num].append(turn)
            current = num

        else:
            num = prev
            try:
                prev_turn, last_turn = num_turn[num]
                new_num = last_turn - prev_turn
            except ValueError:
                new_num = 0
            num_turn[new_num].append(turn)
            current = new_num

    print(current)


if __name__ == "__main__":
    import time

    t0 = time.time()
    # run(2021)
    run(30000001)
    print(time.time() - t0)
