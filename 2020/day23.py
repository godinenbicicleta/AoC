import time

TEST = "389125467"
PROD = "362981754"


class Node:
    __slots__ = ("element", "prev", "next")

    def __init__(self, element, predecessor, successor):
        self.element = element
        self.next = successor
        self.prev = predecessor

    def __repr__(self):
        return f"Node({self.element})"


class DoublyLinkedList:
    def __init__(self, nums, size=9):
        self.tail = None
        self._size = 0
        self.values = [None] * (size + 1)
        for num in nums:
            self.append(num)
        self.possible_max = tuple((size - x for x in range(0, 4)))
        self.possible_min = tuple((1 + x for x in range(0, 4)))

    @property
    def empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def __contains__(self, element):
        return self.values[element] is not None

    def find(self, element):
        return self.values[element]

    @property
    def max(self):
        for num in self.possible_max:
            if self.values[num] is not None:
                return num
        else:
            raise ValueError(self.possible_max, self.values)

    @property
    def min(self):
        for num in self.possible_min:
            if self.values[num] is not None:
                return num
        else:
            raise ValueError(self.possible_max, self.values)

    def first(self):
        if self.empty:
            raise ValueError("Empty")
        return self.tail.next

    def append(self, element):
        new_node = Node(element, None, None)
        if self.empty:
            new_node.next = new_node
            new_node.prev = new_node
            self.tail = new_node
        elif self._size == 1:
            old_tail = self.tail
            old_tail.next = new_node
            new_node.next = old_tail
            old_tail.prev = new_node
            new_node.prev = old_tail
            self.tail = new_node
        else:
            head = self.tail.next
            old_tail = self.tail
            new_node.next = head
            new_node.prev = old_tail

            head.prev = new_node
            old_tail.next = new_node
            self.tail = new_node

        self._size += 1
        self.values[element] = new_node
        return new_node

    def append_node(self, new_node):
        """Assuming list is not empty and has more than 1 element
        """
        head = self.tail.next
        old_tail = self.tail
        new_node.next = head
        new_node.prev = old_tail

        head.prev = new_node
        old_tail.next = new_node
        self.tail = new_node

        self._size += 1
        self.values[new_node.element] = new_node
        return new_node

    def append_after(self, element_node, node):
        if node == self.tail:
            return self.append_node(element_node)
        else:
            predecessor = node
            successor = node.next
            element_node.next = successor
            element_node.prev = predecessor
            predecessor.next = element_node
            successor.prev = element_node
            self._size += 1
            self.values[element_node.element] = element_node
            return element_node

    def append_left(self, element):
        new_node = Node(element, None, None)
        if self.empty:
            new_node.next = new_node
            new_node.prev = new_node
            self.tail = new_node
        else:
            old_head = self.tail.next
            new_node.next = old_head
            new_node.prev = self.tail
            self.tail.next = new_node
            old_head.prev = new_node
        self._size += 1
        self.values[element] = new_node
        return new_node

    def delete_node(self, node):
        if self.empty:
            raise ValueError("Empty")
        element = node.element
        self.values[element] = None
        self._size -= 1
        if self.empty:
            self._tail = None
        elif self.tail == node:
            head = self.tail.next
            new_tail = self.tail.prev
            new_tail.next = head
            self.tail = new_tail
            head.prev = self.tail
        else:
            prev = node.prev
            next_ = node.next
            prev.next = next_
            next_.prev = prev
        node.next = node.prev = None
        return node

    def pop_after(self, node, num):
        return [self.delete_node(node.next) for _ in range(num)]

    def pop(self):
        return self.delete_node(self.tail)

    def pop_left(self):
        return self.delete_node(self.tail.next)

    def __iter__(self):
        if self.empty:
            return iter([])
        header = self.tail.next
        for _ in range(len(self)):
            node = header.next
            yield node
            header = node

    def __repr__(self):
        return f'[ {" ".join(map(lambda x: str(x.element), iter(self)))} ]'


def find_destination_node(dl, destination_label):
    if destination_label < dl.min:
        destination_node = dl.find(dl.max)
    elif destination_label in dl:
        destination_node = dl.find(destination_label)
    else:
        while True:
            destination_label -= 1
            if destination_label in dl:
                return dl.find(destination_label)
    return destination_node


def run(nums, size, moves=3):
    cups = DoublyLinkedList(nums, size)
    # print(cups)
    current = cups.first()
    print("started")
    for move in range(1, moves + 1):
        # if moves < 10:
        #    print(f"--------- move {move} ---------")

        # if move % 100000 == 0:
        #    print(f"--------- move {move/moves} ---------")
        # print(f"--------- move {move} ---------")
        # print("cups: ", cups)
        # print("current: ", current)
        pick_up = cups.pop_after(current, 3)
        destination_label = current.element - 1
        destination_node = find_destination_node(cups, destination_label)
        after = destination_node
        for ix in range(3):
            after = cups.append_after(pick_up[ix], after)
        current = current.next
    if moves < 1000:
        print("----- final -----")
        print("cups: ", cups)
    else:
        one = cups.find(1)
        print(one.next)
        print(one.next.next)
        print(one.next.element * one.next.next.element)


def big_list(string):
    nums = list(map(int, string))
    print(nums)
    max_num = max(nums)
    next_num = max_num + 1
    for ix, num in enumerate(nums):
        yield num
    while next_num < 1_000_001:
        yield next_num
        next_num += 1


if __name__ == "__main__":
    one = list(map(int, TEST))
    run(one, len(one), 100)
    t0 = time.time()
    two = list(map(int, PROD))
    run(two, len(two), 101)
    print(time.time() - t0)
    t0 = time.time()
    run(big_list(TEST), 1_000_000, 10_000_000)
    print(time.time() - t0)
    t0 = time.time()
    run(big_list(PROD), 1_000_000, 10_000_000)
    print(time.time() - t0)
    # 12757828710
