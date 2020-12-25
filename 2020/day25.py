from typing import NamedTuple


class Key(NamedTuple):
    card: int
    door: int


def run_loop(goal):
    subject = 7
    REM = 20201227
    num = 1
    loop_size = 0
    while num != goal:
        loop_size += 1
        num = (num * subject) % REM
    return loop_size


def get_encryption(subject, loop_size):
    REM = 20201227
    num = 1
    for _ in range(loop_size):
        num = (num * subject) % REM
    return num


def run(env):
    key = Key(3248366, 4738476) if env else Key(5764801, 17807724)
    print(key)
    card_loop = run_loop(key.card)
    print("card loop: ", card_loop)
    door_loop = run_loop(key.door)
    print("door loop: ", door_loop)
    enc1 = get_encryption(key.card, door_loop)
    enc2 = get_encryption(key.door, card_loop)
    assert enc1 == enc2, f"{enc1} != {enc2}"
    print(enc1)


if __name__ == "__main__":
    run(0)
    run(1)
