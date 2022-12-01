def solve():
    with open("input.txt", "r") as f:
        lines = [int(x.strip()) for x in f]
        total = sum(lines)
        print(total)
        cache = set()
        acc = 0
        i = 0
        while True:
            acc += lines[i]
            if acc in cache:
                print(acc)
                break
            cache.add(acc)
            i = (i + 1) % len(lines)


if __name__ == "__main__":
    solve()
