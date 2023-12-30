with open("data/day25.txt") as f:
    data = [line.strip().split(": ") for line in f]

g = {}
for key, vstr in data:
    vs = vstr.split()
    g[key] = g.get(key, []) + vs
    for v in vs:
        g[v] = g.get(v, []) + [key]


nodes = list(g.keys())


def run(i, removed):
    start = nodes[i]
    seen = set([start])
    queue = [start]
    res = {start: None}  # node: prev
    while queue:
        current = queue.pop()
        for n in g[current]:
            if n in seen:
                continue
            if (current, n) in removed or (n, current) in removed:
                continue
            seen.add(n)
            queue.append(n)
            res[n] = current
    return res


def getTree(i):
    res = run(i, ())
    tree = {}
    for k, v in res.items():
        if v is None:
            continue
        if v not in tree:
            tree[v] = []
        tree[v].append(k)
    return tree


def main():
    for i in range(len(nodes)):
        tree = getTree(i)
        for right in tree.values():
            for candidate in right:
                if len(tree.get(candidate, [])) == 0:
                    continue
                cs = childsof(tree, candidate) + [candidate]
                ps = parentsof(tree, candidate)
                rem = [i for i in nodes if i not in ps and i not in cs]
                for r in rem:
                    if len(set(g[r]) & set(cs)) == 0:
                        ps += [r]
                    elif len(set(g[r]) & set(ps)) == 0:
                        cs += [r]
                rem = [i for i in nodes if i not in ps and i not in cs]
                if len(rem) == 2:
                    for r in rem:
                        if len(set(g[r]) & set(cs)) == 1:
                            ps += [r]
                        else:
                            cs += [r]

                    return len(cs) * len(ps)


def childsof(tree, node):
    res = list(tree.get(node, []))
    for cs in tree.get(node, []):
        res += childsof(tree, cs)
    return res


def parentsof(tree, node):
    for k, vs in tree.items():
        if node in vs:
            return [k] + parentsof(tree, k)
    return []


if __name__ == "__main__":
    print(main())
