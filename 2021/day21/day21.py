from collections import Counter, defaultdict
from functools import lru_cache


def dice():
    j = 1
    while True:
        for i in range(1, 101):
            yield i, j
            j += 1


def part1():
    s1 = 0
    s2 = 0
    p1 = 3
    p2 = 10
    roll = dice()
    while True:
        for _ in range(3):
            r, num = next(roll)
            p1 += r
        p1 = p1 % 10
        p1 = p1 or 10
        s1 += p1
        if s1 >= 1000:
            print(s2 * num)
            break

        for _ in range(3):
            r, num = next(roll)
            p2 += r
        p2 = p2 % 10
        p2 = p2 or 10
        s2 += p2
        if s2 >= 1000:
            print(s1 * num)
            break


part1()


def dice2():
    while True:
        yield 1, 2, 3


memo = {}


def play(games_counter):
    turns = 0
    done_games = defaultdict(int)
    while games_counter:
        turns += 1
        print(turns)
        new_games = defaultdict(int)
        for game, count in games_counter.items():
            gs, done = play_one(game, count)
            for g, c in gs.items():
                new_games[g] += c
            for g, c in done.items():
                done_games[g] += c

        games_counter = new_games
        current, d = sum(games_counter.values()), sum(done_games.values())
        print("games: ", current, d, current + d)
    return done_games


def comb_take(x, n):
    if n == 0:
        yield []
    elif len(x) == 1:
        for elem in x:
            yield [elem]
    else:
        for i in range(len(x)):
            for c in comb_take(x, n - 1):
                yield [x[i]] + c


dice_rolls = list(comb_take([1, 2, 3], 3))


def wrap(x):
    k = x % 10
    return k or 10


def play_one(game, count):
    games = [game]
    new_games = defaultdict(int)
    done_games = defaultdict(int)
    for dr in dice_rolls:
        for s1, s2, p1, p2 in games:
            r = wrap(p1 + sum(dr))
            s = s1 + r
            if s >= 21:
                done_games[(s, s2, r, p2)] += count
            else:
                new_games[(s, s2, r, p2)] += count
    new_games2 = defaultdict(int)
    for dr in dice_rolls:
        for (s1, s2, p1, p2), c in new_games.items():
            r = wrap(p2 + sum(dr))
            s = s2 + r
            if s >= 21:
                done_games[(s1, s, p1, r)] += c

            else:
                new_games2[(s1, s, p1, r)] += c

    return new_games2, done_games


done_games = play({(0, 0, 3, 10): 1})
# done_games = play({(0, 0, 4, 8): 1})

score = {2: 0, 1: 0}
for g, c in done_games.items():
    if g[0] >= 21:
        score[1] += c
    else:
        score[2] += c
print(score)
