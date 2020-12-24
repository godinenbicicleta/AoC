TEST = "389125467"
PROD = "362981754"


class Node:
    __slots__ = ("_element", "prev", "next")

    def __init__(self, element, predecessor, successor):
        self._element = element
        self.next = successor
        self.prev = predecessor

    @property
    def element(self):
        return self._element

    def __repr__(self):
        return f"Node({self.element})"


class DoublyLinkedList:
    def __init__(self):
        self.tail = None
        self._size = 0
        self.values = set()

    @property
    def empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def __contains__(self, element):
        return element in self.values

    def find(self, element, start=None):
        if start is None:
            node = self.first()
        else:
            node = start.next
        while True:
            prev_node = node
            if node.element == element:
                return node
            node = node.next
            if node == prev_node:
                raise ValueError

    def max(self):
        return max(self.values)

    def min(self):
        return min(self.values)

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
        self.values.add(element)
        return new_node

    def append_after(self, element, node):
        if node == self.tail:
            return self.append(element)
        else:
            predecessor = node
            successor = node.next
            new_node = Node(element, predecessor, successor)
            predecessor.next = new_node
            successor.prev = new_node
            self._size += 1
            self.values.add(element)
            return new_node

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
        self.values.add(element)
        return new_node

    def delete_node(self, node):
        if self.empty:
            raise ValueError("Empty")
        element = node.element
        self._size -= 1
        self.values.remove(element)
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
        return element

    def pop_after(self, node, num):
        return [self.delete_node(node.next) for _ in range(num)]

    def pop(self):
        return self.delete_node(self.tail)

    def pop_left(self):
        return self.delete_node(self.tail.next)

    @classmethod
    def from_list(cls, nums):
        dl = cls()
        for num in nums:
            dl.append(num)
        return dl

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


def find_destination_node(dl, start, destination_label):
    if destination_label in dl:
        destination_node = dl.find(destination_label, start)
    elif destination_label < dl.min():
        # print("to_find: ", dl.max())
        destination_node = dl.find(dl.max(), start)
    else:
        return find_destination_node(dl, start, destination_label - 1)
    return destination_node


def run(nums, moves=3):
    cups = DoublyLinkedList.from_list(nums)
    # print(cups)
    current = cups.first()
    print("started")
    for move in range(1, moves + 1):
        if moves < 10:
            print(f"--------- move {move} ---------")

        if move % 100 == 0:
            print(f"--------- move {move/moves} ---------")
        # print(f"--------- move {move} ---------")
        # print("cups: ", cups)
        # print("current: ", current)
        # print("to_pick_up: =", current.next, current.next.next, current.next.next.next)
        pick_up = cups.pop_after(current, 3)
        # print("pick up: ", pick_up)
        destination_label = current.element - 1
        # print("destination_label: ", destination_label)
        destination_node = find_destination_node(cups, current, destination_label)
        # print("destination_label_found: ", destination_node.element)
        after = destination_node
        for ix in range(3):
            after = cups.append_after(pick_up[ix], after)
        current = current.next
    if moves < 1000:
        print("----- final -----")
        print("cups: ", cups)
    else:
        one = cups.find(cups.first(), 1)
        print(one.next)
        print(one.next.next)
        print(one.next * one.next.next)


def big_list(string):
    nums = list(map(int, string))
    print(nums)
    max_num = max(nums)
    next_num = max_num + 1
    big_nums = [None] * 1000000
    for ix, num in enumerate(nums):
        big_nums[ix] = num
    ix += 1
    while next_num < 1000001:
        big_nums[ix] = next_num
        next_num += 1
        ix += 1
    return big_nums


if __name__ == "__main__":
    run(list(map(int, TEST)), 100)
    run(list(map(int, PROD)), 100)
    run(big_list(TEST), 10000000)
