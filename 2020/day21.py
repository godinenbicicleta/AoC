import re
from collections import Counter, deque

with open("day21_test.txt") as f:
    data = [line.strip() for line in f]


def parse(data):
    a = dict()
    all_ingredients = set()

    for line in data:
        ingredients, allergens = line.split(" (contains ")
        ingredients = set(ingredients.split())
        all_ingredients.update(ingredients)
        allergens = re.findall(r"\w+", allergens)
        for allergen in allergens:
            if allergen in a:
                a[allergen] = a[allergen] & ingredients
            else:
                a[allergen] = ingredients
    return a, all_ingredients


a, all_ingredients = parse(data)


def solve(a):
    solved = dict()
    seen = set()
    sorted_keys = deque([k for k in sorted(a, key=lambda x: len(a[x]))])
    while sorted_keys:
        key = sorted_keys.popleft()
        if len(a[key]) == 1:
            solved[key] = set(a[key])
            seen.add(list(a[key])[0])
        elif key in solved and len(solved[key]) == 1:
            seen.add(list(solved[key])[0])
        else:
            if key in solved:
                solved[key] = solved[key] - seen
            else:
                solved[key] = a[key] - seen
            sorted_keys.append(key)
    return {k: v.pop() for k, v in solved.items()}


solved = solve(a)

contain = set(solved.values())

counts = Counter(re.findall("\w+", "".join(data)))
print(counts)

total = 0
for ingredient in all_ingredients:
    if ingredient not in contain:
        total += counts[ingredient]

print("total: ", total)

keys_in_order = sorted(solved.keys())

canonical = ",".join([solved[k] for k in keys_in_order])
print(canonical)
