import fileinput

lines = [line.strip().split(" | ") for line in fileinput.input()]

# 1: 2, 4: 4, 7: 3, 8: 7
total = 0
for i, o in lines:
    outputs = o.split(" ")
    for o in outputs:
        if len(o) in {2, 4, 3, 7}:
            total += 1
print(total)

"""

     0:      1:      2:      3:      4:
    aaaa    ....    aaaa    aaaa    ....
   b    c  .    c  .    c  .    c  b    c
   b    c  .    c  .    c  .    c  b    c
    ....    ....    dddd    dddd    dddd
   e    f  .    f  e    .  .    f  .    f
   e    f  .    f  e    .  .    f  .    f
    gggg    ....    gggg    gggg    ....

     5:      6:      7:      8:      9:
    aaaa    aaaa    aaaa    aaaa    aaaa
   b    .  b    .  .    c  b    c  b    c
   b    .  b    .  .    c  b    c  b    c
    dddd    dddd    ....    dddd    dddd
   .    f  e    f  .    f  e    f  .    f
   .    f  e    f  .    f  e    f  .    f
    gggg    gggg    ....    gggg    gggg


 digit   num_signals

  0       6
  1       2
  2       5
  3       5
  4       4
  5       5
  6       6
  7       3
  8       7
  9       6

 num_signals | digits
  2            1
  3            7
  4            4
  5            2,3,5
  6            0,6,9
  7            8

     a | b | c | d | e | f | g
   +---+---+---+---+---+---+---+
 0 | X | X | X |   | X | X | X |
   +---+---+---+---+---+---+---+
 1 |   |   | X |   |   | X |   |
   +---+---+---+---+---+---+---+
 2 | X |   | X | X | X |   | X | ==>
   +---+---+---+---+---+---+---+
 3 | X |   | X | X |   | X | X | ==>
   +---+---+---+---+---+---+---+
 4 |   | X | X | X |   | X |   | ==>
   +---+---+---+---+---+---+---+
 5 | X | X |   | X |   | X | X |
   +---+---+---+---+---+---+---+
 6 | X | X |   | X | X | X | X |
   +---+---+---+---+---+---+---+
 7 | X |   | X |   |   | X |   | ==>
   +---+---+---+---+---+---+---+
 8 | X | X | X | X | X | X | X |
   +---+---+---+---+---+---+---+
 9 | X | X | X | X |   | X | X |
   +---+---+---+---+---+---+---+

2,4,3,7

4-3 = b
3-4-7 +1 = g
common(2,4,3,7) => c
4-2 = bf
1 = cf
7-1  = a

6-5 = e
8-9 = e
n-0 = d

"""


def decode(codes):
    # first pass, get 1,7,4 and 8:
    d = {i: None for i in range(10)}
    five_char = []
    six_char = []
    for code in codes:
        s = set(code)
        if len(code) == 2:
            d["1"] = s
        elif len(code) == 3:
            d["7"] = s
        elif len(code) == 4:
            d["4"] = s
        elif len(code) == 7:
            d["8"] = s
        elif len(code) == 6:
            six_char.append(s)
        elif len(code) == 5:
            five_char.append(s)
    new_five_char = []
    for elem in five_char:
        if (d["4"] - d["7"]).issubset(elem):
            d["5"] = elem
        else:
            new_five_char.append(elem)

    new_six_char = []
    for elem in six_char:
        if not d["1"].issubset(elem):
            d["6"] = elem
        else:
            new_six_char.append(elem)
    for elem in new_six_char:
        if not (d["8"] - d["5"]).issubset(elem):
            d["9"] = elem
        else:
            d["0"] = elem
    for elem in new_five_char:
        if not (d["8"] - d["5"]).issubset(elem):
            d["3"] = elem
        else:
            d["2"] = elem
    return d


total = 0
for i, o in lines:
    outputs = o.split(" ")
    inputs = i.split(" ")
    decode_map = decode(inputs)
    r = []
    for o in outputs:
        for key, s in decode_map.items():
            if set(o) == s:
                r.append(key)
                continue
    n = int("".join(r))
    total += n
print(total)
