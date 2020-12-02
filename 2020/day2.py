import re
from collections import Counter

with open("day2.txt") as f:
    data = [i.strip() for i in f]


rex = r"(\d+)-(\d+)\s(\w):\s(\w+)"

parsed = [re.findall(rex, d) for d in data]

valid = 0

for elem in parsed:
    (min_, max_, char, password) = elem[0]
    counter = Counter(password)
    if counter[char] >= int(min_) and counter[char] <= int(max_):
        valid += 1

print(valid)

valid = 0

for elem in parsed:
    (one, two, char, password) = elem[0]
    if password[int(one) - 1] != char and password[int(two) - 1] == char:
        valid += 1
    elif password[int(one) - 1] == char and password[int(two) - 1] != char:
        valid += 1

print(valid)
