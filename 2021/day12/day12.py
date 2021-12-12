import fileinput
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Set


class Size(str, Enum):
    SMALL = "SMALL"
    BIG = "BIG"


@dataclass(frozen=True)
class Node:
    v: str

    @property
    def size(self) -> Size:
        if self.v.lower() == self.v:
            return Size.SMALL
        return Size.BIG

    @property
    def small(self):
        return self.size == Size.SMALL


@dataclass
class Graph:
    nodes: Set[Node]
    edges: Dict[Node, Set[Node]]

    def ns(self, n: Node) -> Set[Node]:
        return self.edges[n]

    @property
    def start(self):
        return next(n for n in self.nodes if n.v == "start")

    @property
    def end(self):
        return next(n for n in self.nodes if n.v == "end")


nodes = set()
edges = defaultdict(set)
for line in fileinput.input():
    a, b = line.strip().split("-")
    a = Node(a)
    b = Node(b)
    nodes.add(a)
    nodes.add(b)
    edges[a].add(b)
    edges[b].add(a)

g = Graph(nodes=nodes, edges=edges)


# 36, 103 3509


def valid1(node, path) -> bool:

    if node.small and node in path:
        return False
    return True


def has_dup(path) -> bool:
    small_path = [n for n in path if n.small]
    counter = Counter(small_path).most_common(1)
    counts = counter[0][1]

    return counts > 1


def valid2(node, path) -> bool:
    res = True
    if node.small and node in path:
        if node.v in ("start", "end"):
            res = False
        if has_dup(path):
            res = False
    return res


def all_paths(current_paths, valid_func):
    if not current_paths:
        return set()
    done_paths = set()
    new_paths = set()
    for path in current_paths:
        current_node = path[-1]
        if current_node == g.end:
            done_paths.add(path)
            continue
        for next_node in g.ns(current_node):
            if not valid_func(next_node, path):
                continue
            new_path = path + (next_node,)
            if new_path not in new_paths:
                new_paths.add(new_path)

    return done_paths | all_paths(new_paths, valid_func)


print(len(all_paths({(g.start,)}, valid1)))


def print_paths(paths):
    for path in sorted(paths, key=len):
        print(", ".join(node.v for node in path))


# 363611 too low
# 36, 103 3509
# print_paths(all_paths({(g.start,)}, valid2))
print(len(all_paths({(g.start,)}, valid2)))
