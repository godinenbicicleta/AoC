import json


def sum_(data):
    global total
    if isinstance(data, dict):
        if any((v == "red" for v in data.values())):
            return
        for key, value in data.items():
            sum_(value)
    elif isinstance(data, list):
        for d in data:
            sum_(d)
    elif isinstance(data, (int, float)):
        total += data
    else:
        return


if __name__ == "__main__":

    with open("day12.txt", "r") as f:
        data = json.load(f)

    total = 0
    sum_(data)
    print("total: %d" % total)
