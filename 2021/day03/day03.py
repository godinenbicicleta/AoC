with open("input03.txt") as f:
    data = [list(line.strip()) for line in f]

cols = {i: {"1": 0, "0": 0} for i in range(len(data[0]))}

for line in data:
    for col, value in enumerate(line):
        cols[col][value] += 1

gamma = "".join([str(max(d.items(), key=lambda x: x[1])[0]) for d in cols.values()])
epsilon = "".join([str(min(d.items(), key=lambda x: x[1])[0]) for d in cols.values()])

print(gamma)
print(epsilon)


print(int(gamma, 2) * int(epsilon, 2))

res = []
for cond in (1, 2):
    data2 = data[:]
    print(data2[0])
    index = 0
    while len(data2) > 1:
        print("cond:", cond, len(data2))
        cols = {i: {"1": 0, "0": 0} for i in range(len(data2[0]))}

        for line in data2:
            cols[index][line[index]] += 1

        value1 = cols[index]["1"]
        value0 = cols[index]["0"]
        if cond == 1:
            if value0 > value1:
                data2 = [d for d in data2 if d[index] == "0"]
            else:
                data2 = [d for d in data2 if d[index] == "1"]
        else:
            if value1 < value0:
                data2 = [d for d in data2 if d[index] == "1"]
            else:
                data2 = [d for d in data2 if d[index] == "0"]
        index += 1
    res.append("".join(data2[0]))

print(res)

print(int(res[0], 2) * int(res[1], 2))
