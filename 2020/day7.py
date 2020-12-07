with open("day7.txt") as f:
    data = [line.strip() for line in f]


def parse(line):
    [container, contains] = line.split(" contain ")
    container = container.replace(" bags", "")
    if "no other" in contains:
        return (container, None)
    res = (container, {})
    for bag_spec in contains.rstrip(".").split(","):
        [num, desc] = bag_spec.strip().split(" ", 1)
        num = int(num)
        desc = desc.replace("bags", "").replace("bag", "").strip()
        res[1][desc] = num
    return res


parsed = dict(parse(line) for line in data)


def contains(label, item, parsed):
    if parsed[label] is None:
        return False

    contained = parsed[label].items()
    for bag, num in contained:
        if bag == item:
            return True

    return any(contains(bag, item, parsed) for bag, num in contained)


sg = sum(contains(label, "shiny gold", parsed) for label in parsed)
print(sg)

# In [74]: parsed["shiny gold"]
# Out[74]: {'mirrored lavender': 5, 'shiny maroon': 4, 'striped yellow': 4}


with open("day7_test.txt") as f:
    example = dict(parse(d.strip()) for d in f)


def get_needed(label, parsed):
    if parsed[label] is None:
        return 0
    else:
        res = 0
        for bag, num in parsed[label].items():
            res += num * get_needed(bag, parsed) + num
        return res


print(get_needed("shiny gold", parsed))
print(get_needed("shiny gold", example))
print(get_needed("dark blue", example))
