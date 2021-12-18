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


def aba(s, res=None):
    res = res or []
    if len(s) < 3:
        return res
    if s[0] == s[2] and s[0] != s[1]:
        res.append(s[0:3])
    return aba(s[1:], res)


def valid2(line):
    inside = re.findall(r"\[(\w+)\]", line)
    outside = [
        k.replace("[", "").replace("]", "")
        for k in re.findall(r"(\][\w]+|[\w]+\[)", line)
    ]
    abas = []
    for i in outside:
        for r in aba(i):
            abas.append(r)
    if not abas:
        return False
    try:
        for a in abas:
            one, two, three = list(a)
            for k in inside:
                if f"{two}{one}{two}" in k:
                    raise ValueError("valid")
    except ValueError as e:
        if "valid" in str(e):
            return True
    return False


print(len(tuple(l for l in lines if valid2(l))))
