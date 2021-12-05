import fileinput

data = [int(k) for k in fileinput.input()]


def window1():
    inc = 0
    for prev, current in zip(data, data[1:]):
        if current > prev:
            inc += 1
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
    window1()  # 1400
    window3(data[:])  # 1429
