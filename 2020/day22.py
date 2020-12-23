from collections import defaultdict, deque

with open("day22.txt") as f:
    data = f.read()
    player1, player2 = data.split("\n\n")
    player1 = deque(map(int, (player1.strip().split("\n")[1:])))
    player2 = deque(map(int, (player2.strip().split("\n")[1:])))

print(player1)
print(player2)


def play(player1, player2):
    round_ = 1
    while True:
        print(f"====== {round_} =====")
        print("player 1's deck: %s" % player1)
        print("player 2's deck: %s" % player2)
        p1 = player1.popleft()
        p2 = player2.popleft()
        print("player 1 plays %s" % p1)
        print("player 2 plays %s" % p2)
        if p1 > p2:
            print(f"player 1 wins round {round_}")
            player1.extend([p1, p2])
        else:
            print(f"player 2 wins round {round_}")
            player2.extend([p2, p1])
        round_ += 1
        if not player1:
            print("player 2 wins the game")
            break
        elif not player2:
            print("player 1 wins the game")
            break
        else:
            continue
    return player1 or player2


winner = play(player1.copy(), player2.copy())

total = 0
i = 1
while winner:
    total += i * winner.pop()
    i += 1

print(total)

games = defaultdict(set)


def play2(player1, player2, game=1):
    round_ = 1
    while True:
        game_tuple = (tuple(player1), tuple(player2))
        if game_tuple in games[game]:
            return (player1, "1")
        else:
            games[game].add(game_tuple)

        # print(f"====== Round: {round_} Game: {game}=====")
        # print("player 1's deck: %s" % player1)
        # print("player 2's deck: %s" % player2)
        p1 = player1.popleft()
        p2 = player2.popleft()
        # print("player 1 plays %s" % p1)
        # print("player 2 plays %s" % p2)
        if p1 <= len(player1) and p2 <= len(player2):
            p1_copy = deque(list(player1)[:p1])
            p2_copy = deque(list(player2)[:p2])
            _, winner = play2(p1_copy, p2_copy, max(games) + 1)
        else:
            if p1 > p2:
                winner = "1"
            else:
                winner = "2"

        if winner == "1":
            # print(f"player 1 wins round {round_}")
            player1.extend([p1, p2])
        else:
            # print(f"player 2 wins round {round_}")
            player2.extend([p2, p1])

        round_ += 1

        if not player1:
            # print("player 2 wins the game")
            return (player2, "2")
        if not player2:
            # print("player 1 wins the game")
            return (player1, "1")


winner, _ = play2(player1.copy(), player2.copy())
total = 0
i = 1
print(winner)
while winner:
    total += i * winner.pop()
    i += 1

print(total)
# 5615 too low
# 7862 too low
