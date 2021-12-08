import sys
from collections import defaultdict

with open(sys.argv[1], "r") as f:
    lines = [line.strip() for line in f]

cols = [defaultdict(int) for _ in lines[0]]

for line in lines:
    for ix, letter in enumerate(line):
        cols[ix][letter] += 1

print()
for col in cols:
    print(sorted(col.items(), key=lambda x: x[1], reverse=True)[0][0], end="")
print()
for col in cols:
    print(sorted(col.items(), key=lambda x: x[1])[0][0], end="")
print()
