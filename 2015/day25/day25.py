r, c = 2947, 3029
# r, c = 2, 1
seen = set()
# res = [[None for _ in range(r * c)] for _ in range(r * c)]
num = 20151125
# too low 5062733
# too high 23784142
try:
    for row in range(0, r * c):
        #    print(row, end=" ")
        for j in range(0, row + 1):
            i = row - j
            if (i, j) in seen:
                continue
            seen.add((i, j))
            if j == c - 1 and i == r - 1:
                print(num)
                raise ValueError(f"{num}")
            #          res[i][j] = num
            num = (num * 252533) % 33554393
except:
    pass


def printRes(res):
    print("\n".join(" ".join(map(lambda x: str(x) if x else " ", r)) for r in res))


# printRes(res)
# print(res[r - 1][c - 1])
