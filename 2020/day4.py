"""
byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
"""
import re

with open("day4.txt") as f:
    data = f.read()

lines = data.split("\n\n")

conditions = set("byr iyr eyr hgt hcl ecl pid".split(" "))


def valid(parts):
    keys = {k.split(":")[0] for k in parts}
    if all(c in keys for c in conditions):
        return True
    else:
        return False


v = 0
for line in lines:
    parts = re.split(r"\s", line)
    if valid(parts):
        v += 1

print(v)

"""
byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not
"""


def apply_condition(key, value):
    if key == "byr":
        res = int(value) >= 1920 and int(value) <= 2002
    if key == "iyr":
        res = int(value) >= 2010 and int(value) <= 2020
    if key == "eyr":
        res = int(value) >= 2020 and int(value) <= 2030
    if key == "hgt":
        num, in_or_cm = re.findall(r"^(\d+)(cm|in)$", value)[0]
        if in_or_cm == "in":
            res = int(num) >= 59 and int(num) <= 76
        elif in_or_cm == "cm":
            res = int(num) >= 150 and int(num) <= 193
        else:
            res = False
    if key == "hcl":
        res = bool(re.match(r"^#[0-9a-f]{6}$", value))
    if key == "ecl":
        res = value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    if key == "pid":
        res = bool(re.match(r"^[0-9]{9}$", value))
    if key == "cid":
        res = True
    return res


def valid(parts):
    conds = {k.split(":")[0]: k.split(":")[1] for k in parts if k}
    if not all(c in conds for c in conditions):
        return False
    try:
        res = [apply_condition(key, value) for key, value in conds.items()]
        return all(res)

    except:
        return False


v = 0
for line in lines:
    parts = re.split(r"\s", line)
    if valid(parts):
        v += 1

print(v)
