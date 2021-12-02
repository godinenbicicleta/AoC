with open("input02.txt") as f:
    d = [line.strip() for line in f]

x, y = 0, 0
for line in d:
    if line.startswith("forward "):
        x += int(line.replace("forward ", ""))
    elif line.startswith("down "):
        y += int(line.replace("down ", ""))
    elif line.startswith("up "):
        y -= int(line.replace("up ", ""))
    else:
        raise ValueError("Unknown")

print(x * y)

x, y, aim = 0, 0, 0
for line in d:
    if line.startswith("forward "):
        x += int(line.replace("forward ", ""))
        y += aim * int(line.replace("forward ", ""))
    elif line.startswith("down "):
        aim += int(line.replace("down ", ""))
    elif line.startswith("up "):
        aim -= int(line.replace("up ", ""))
    else:
        raise ValueError("Unknown")

print(x * y)
