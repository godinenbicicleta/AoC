NUM = 30000
with open("day3.txt") as f:
    lines = [row.strip() * 100 for row in f]

height_goal = len(lines)

height = 0

pos = (0, 0)
trees = 0

# part 1
while height < height_goal:
    pos = pos[0] + 3, pos[1] + 1
    height = pos[1]
    try:
        if lines[height][pos[0]] == "#":
            trees += 1
    except:
        break


print(trees)

# part 2
"""
Right 1, down 1.
Right 3, down 1. (This is the slope you already checked.)
Right 5, down 1.
Right 7, down 1.
Right 1, down 2.
"""


def get_trees(right, down):
    height = 0

    pos = (0, 0)
    trees = 0

    while height < height_goal:
        pos = pos[0] + right, pos[1] + down
        height = pos[1]
        try:
            if lines[height][pos[0]] == "#":
                trees += 1
        except:
            break
    return trees


print(
    (
        get_trees(1, 1)
        * get_trees(3, 1)
        * get_trees(5, 1)
        * get_trees(7, 1)
        * get_trees(1, 2)
    )
)
