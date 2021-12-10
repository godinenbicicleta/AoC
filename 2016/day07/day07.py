import re
import sys

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f]


def abba(s):
    if len(s) < 4:
        return False
    if s[0] == s[3] and s[1] == s[2] and s[0] != s[1]:
        return True
    return abba(s[1:])


def valid(line):
    inside = re.findall(r"\[(\w+)\]", line)
    if any(abba(i) for i in inside):
        res = False
    elif abba(line):
        res = True
    else:
        res = False
    return res


print(len(tuple(l for l in lines if valid(l))))


def valid2(line):
    inside = re.findall(r"\[(\w+)\]", line)
    if any(abba(i) for i in inside):
        res = False
    elif abba(line):
        res = True
    else:
        res = False
    return res
