import fileinput
import math
from copy import deepcopy
from functools import reduce


class Tree:
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return f"T({self.root})"

    @property
    def magnitude(self):
        return self.root.magnitude

    def __add__(self, other):
        left = deepcopy(self.root)
        right = deepcopy(other.root)

        for node in left.nodes():
            node.depth += 1
        for node in right.nodes():
            node.depth += 1

        root = Node(value=None, depth=0, left=left, right=right)
        root.left.parent = root
        root.right.parent = root
        res = Tree(root)
        res = res.red()
        return res

    def next_right(self, node):
        root = self.root
        inorder1 = list(root.inorder())
        inorder2 = list(root.inorder())
        for curr, right in zip(inorder1, inorder2[1:]):
            if curr == node:
                return right
        return None

    def prev_left(self, node):
        root = self.root
        inorder1 = list(root.inorder())
        inorder2 = list(root.inorder())
        for prev, curr in zip(inorder1, inorder2[1:]):
            if curr == node:
                return prev
        return None

    def red(self):
        finished = False
        while not finished:
            finished = True
            while True:
                breakWhile = True
                for node in self.root.leafs:
                    if node.depth > 4:
                        self.explode(node)
                        finished = False
                        breakWhile = False
                        break
                if breakWhile:
                    break
            for node in self.root.leafs:
                if node.value > 9:
                    self.split_node(node)
                    finished = False
                    break
        return self

    @property
    def max_depth(self):
        return max(k.depth for k in self.root.leafs)

    def explode(self, node):
        parent = node.parent

        parent.value = 0
        left_n = self.prev_left(parent)
        right_n = self.next_right(parent)
        if left_n is not None:
            left = parent.left.value
            left_n.value += left
        if right_n is not None:
            right = parent.right.value
            right_n.value += right

        parent.left = None
        parent.right = None

    def split_node(self, node):
        assert node.is_leaf
        is_left = node.parent.left == node
        parent = node.parent
        value = node.value
        depth = node.depth
        value_left = value // 2
        value_right = int(math.ceil(value / 2))
        local_parent = Node(parent=parent, value=None, depth=depth)
        local_parent.left = Node(value=value_left, depth=depth + 1, parent=local_parent)
        local_parent.right = Node(
            value=value_right, depth=depth + 1, parent=local_parent
        )
        if is_left:
            parent.left = local_parent
        else:
            parent.right = local_parent


def flatten(x):
    def _flatten(lol):
        for elem in lol:
            if isinstance(elem, list):
                yield from _flatten(elem)
            else:
                yield elem

    return list(_flatten(x))


class Node:
    def __init__(self, value=None, left=None, right=None, depth=0, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.depth = depth
        self.parent = parent

    @property
    def magnitude(self):
        if self.is_leaf:
            return self.value
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    @property
    def is_leaf(self):
        return self.value is not None

    @property
    def leafs(self):
        if self.is_leaf:
            return [self]
        else:
            return flatten([self.left.leafs, self.right.leafs])

    def __str__(self):
        if self.value is not None:
            return f"{self.value}"
            # return f"{self.value}"
        return f"[{self.left}, {self.right}]"

    def nodes(self):
        yield self
        if self.is_leaf:
            return
        left, right = self.left, self.right
        yield from left.nodes()
        yield from right.nodes()

    def inorder(self):
        if self.is_leaf:
            yield self
        else:
            yield from self.left.inorder()
            yield from self.right.inorder()


def parse(x, depth=0, parent=None):
    if isinstance(x, int):
        return Node(x, depth=depth, parent=parent)
    left, right = x
    res = Node(value=None, depth=depth, parent=parent)
    res.left = parse(left, depth=depth + 1, parent=res)
    res.right = parse(right, depth=depth + 1, parent=res)
    return res


def p1(trees):
    res = reduce(lambda x, y: x + y, trees)
    return res


# part 1
trees = [Tree(parse(eval(line))) for line in fileinput.input()]
res = p1(trees)
print(res.magnitude)

# part 2
m_max = 0
for i in range(len(trees)):
    for j in range(len(trees)):
        if i == j:
            continue
        m = (trees[i] + trees[j]).magnitude
        if m > m_max:
            m_max = m
print(m_max)
