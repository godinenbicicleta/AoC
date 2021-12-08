import string
import sys
from collections import Counter
from dataclasses import dataclass


@dataclass
class Room:
    raw: str
    counter: Counter
    sectorID: int
    checksum: str
    letters: str

    def is_valid(self) -> bool:
        try:
            check = "".join(sorted(self.checksum, key=lambda x: (-self.counter[x], x)))
        except KeyError:
            return False

        return check == self.checksum

    @classmethod
    def from_str(cls, s: str):
        splitted = s.split("-")
        letters = "".join(splitted[:-1])
        counter = dict(
            sorted(Counter(letters).most_common(), key=lambda x: (-x[1], x[0]))[:5]
        )
        checksum = splitted[-1].split("[")[-1][:-1]
        sectorId = int(splitted[-1].split("[")[0])
        return cls(
            raw=s,
            counter=counter,
            sectorID=sectorId,
            checksum=checksum,
            letters=letters,
        )

    @property
    def name(self):
        if not self.is_valid():
            return ""

        letters = "-".join(self.raw.split("-")[:-1])

        def convert(s):
            if s == "-":
                return " "
            else:
                ix = string.ascii_lowercase.index(s)
                ix = (ix + self.sectorID) % len(string.ascii_lowercase)
                return string.ascii_lowercase[ix]

        name = "".join([convert(k) for k in letters])
        return name

    def __str__(self):
        return f"Room(raw={self.raw}, name={self.name})"


with open(sys.argv[1]) as f:
    rooms = [Room.from_str(line.strip()) for line in f]

total = 0
for room in rooms:
    if room.is_valid():
        total += room.sectorID

# 411182 high
print(total)

for r in rooms:
    if "north" in r.name:
        print(r)
