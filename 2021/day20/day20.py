import sys

with open(sys.argv[1]) as f:
    data = f.read().strip()

raw_algo, raw_img = data.split("\n\n")
algo = raw_algo.strip()
raw_img = [k.strip() for k in raw_img.strip().split("\n")]

assert len(raw_algo) == 512

img = {}

for y, row in enumerate(raw_img):
    for x, val in enumerate(row):
        img[(x, y)] = val


def rep(x):
    if x == ".":
        return "0"
    if x == "#":
        return "1"


def upd(p, img, algo, default="."):
    x, y = p
    points = (
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    )
    s = "".join(rep(img.get(p, default)) for p in points)
    k = int(s, 2)
    res = algo[k]
    return res


def run(img, algo, times):
    for t in range(times):
        print(t)
        new_img = {}
        if t % 2 == 0:
            default = "."
        else:
            default = "#"
        keys = list(img.keys())
        sx = sorted(keys, key=lambda x: x[0])
        sy = sorted(keys, key=lambda x: x[1])
        minx, maxx = sx[0][0], sx[-1][0]
        miny, maxy = sy[0][1], sy[-1][1]
        for x in range(minx - 4, maxx + 5):
            for y in range(miny - 4, maxy + 4):
                p = (x, y)
                res = upd(p, img, algo, default)
                new_img[p] = res
        img = new_img
    return img


new_img = run(img, algo, 2)
print(len([k for k in new_img.values() if k == "#"]))

new_img = run(img, algo, 50)
print(len([k for k in new_img.values() if k == "#"]))
