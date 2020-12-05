from typing import NamedTuple

with open("day5.txt") as f:
    data = [line.strip() for line in f]

"""
So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.

Here are some other boarding passes:

BFFFBBFRRR: row 70, column 7, seat ID 567.
FFFBBBFRRR: row 14, column 7, seat ID 119.
BBFFBBFRLL: row 102, column 4, seat ID 820.
"""


class Seat(NamedTuple):
    row: int
    col: int

    @property
    def id(self):
        return self.row * 8 + self.col


ROWS = 128
COLUMNS = 8


def dcd(code):
    rows = list(range(ROWS))
    cols = list(range(COLUMNS))

    for ix, letter in enumerate(code):
        if ix <= 6:
            rows = move(rows, letter)
        else:
            cols = move(cols, letter)

    return Seat(rows[0], cols[0])


def move(l, char):
    if char == "F" or char == "L":
        return l[: len(l) // 2]
    else:
        return l[len(l) // 2 :]


assert dcd("FBFBBFFRLR") == Seat(44, 5)
assert dcd("BFFFBBFRRR") == Seat(70, 7)
assert dcd("FFFBBBFRRR") == Seat(14, 7)
assert dcd("BBFFBBFRLL") == Seat(102, 4)

print(max([dcd(code).id for code in data]))

seats = {dcd(code) for code in data}
ids = {dcd(code).id for code in data}

for row in range(ROWS):
    for col in range(COLUMNS):
        seat = Seat(row, col)
        if all([seat not in seats, seat.id + 1 in ids, seat.id - 1 in ids]):
            print(seat.id)
            break
