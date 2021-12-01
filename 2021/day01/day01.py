with open("input01.txt") as f:
    data = [int(k) for k in f]


def window1():
    inc = 0
    prev = data[0]
    for num in data[1:]:
        if num > prev:
            inc += 1
        prev = num
    print(inc)


def window3(data):
    prev = sum(data[:3])
    inc = 0
    index = 1
    while True:
        if index >= len(data):
            break
        current = data[index : index + 3]
        if len(current) < 3:
            break
        c = sum(current)
        if c > prev:
            inc += 1
        prev = c
        index += 1
    print(inc)


if __name__ == "__main__":
    window1()
    window3(data[:])
