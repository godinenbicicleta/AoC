import sys

sys.setrecursionlimit(3500)
with open("data/day25.txt") as f:
    data = [line.strip().split(": ") for line in f]

g = {}
for key, vstr in data:
    vs = vstr.split()
    g[key] = g.get(key, []) + vs
    for v in vs:
        g[v] = g.get(v, []) + [key]


edges = []
nodes = tuple(g.keys())

for k, vs in g.items():
    for v in vs:
        if (k, v) in edges:
            continue
        if (v, k) in edges:
            continue
        edges.append((k, v))


def solve(g, path, unvisited, visited):
    if len(unvisited) == 0:
        return path
    current = path[-1]
    for n in g[current]:
        if n in visited:
            continue
        path.append(n)
        unvisited.remove(n)
        visited.add(n)
        newpath = solve(g, path, unvisited, visited)
        if newpath:
            return newpath
        path.pop()
        unvisited.add(n)
        visited.remove(n)
    return None


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


def fromxn(s, n):
    if len(s) < n:
        return
    elif len(s) == n:
        yield s
    elif n == 0:
        yield []
    else:
        for k in fromxn(s[1:], n):
            yield k
        for m in fromxn(s[1:], n - 1):
            yield [s[0]] + m


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


def get_all_candidates():
    for i in range(len(nodes)):
        tree = getTree(i)
        start = nodes[i]
        maxv = 0
        for k, v in tree.items():
            if k != start and len(v) > maxv:
                maxv = len(v)
        for left, right in tree.items():
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
                    minNum = len(rem)
                    print(rem, end="\t")
                    for r in rem:
                        if len(set(g[r]) & set(cs)) == 1:
                            ps += [r]
                        else:
                            cs += [r]

                    return (left, candidate, i, minNum, len(cs), len(ps), len(cs) * len(ps))


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


def main():
    print(get_all_candidates())


if __name__ == "__main__":
    main()
