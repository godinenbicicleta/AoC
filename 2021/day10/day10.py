import fileinput

scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
scores2 = {")": 1, "]": 2, "}": 3, ">": 4}

open_close = {"(": ")", "[": "]", "{": "}", "<": ">"}

incomplete = []


def add(elem):
    global incomplete
    if elem:
        incomplete.append(elem)


total = 0
for line in fileinput.input():
    stack = [line[0]]
    for elem in line[1:-1]:
        if elem in open_close:
            stack.append(elem)
            continue
        if elem != open_close[stack[-1]]:
            total += scores[elem]
            break
        stack.pop()
    else:
        total_score = 0
        while stack:
            total_score *= 5
            closing = open_close[stack.pop()]
            total_score += scores2[closing]
        add(total_score)


print(total)
incomplete.sort()
print(incomplete[len(incomplete) // 2])
