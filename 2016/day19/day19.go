package main

import (
	"fmt"
)

func run1() {
	size := 3012210
	//  1 2 3 4 5
	// [0 1 2 3 4]

	elfs := make([]int, size, size)
	for i := 0; i < size; i++ {
		elfs[i] = 1
	}
	var np int
	pos := 0
Loop:
	for {
		for np = (pos + 1) % (size); ; np = (np + 1) % (size) {
			if elfs[np] != 0 {
				elfs[pos] += elfs[np]
				if elfs[pos] >= len(elfs) {
					fmt.Println(pos + 1)
					break Loop
				}
				elfs[np] = 0
				break
			}
		}

		for pos = (pos + 1) % size; elfs[pos] == 0; pos = (pos + 1) % size {
		}
	}

}

// Elf represents an elf
type Elf struct {
	id   int
	val  int
	next *Elf
	prev *Elf
}

func find(from *Elf, p int) *Elf {
	res := from
	for i := 0; i < p; i++ {
		res = res.next
	}
	return res
}

func run2() {
	size := 3012210
	head := &Elf{id: 1, val: 1, next: nil, prev: nil}
	var prev *Elf = nil
	current := head
	for i := 1; i < size; i++ {
		prev = current
		current = &Elf{id: i + 1, val: 1, next: nil, prev: prev}
		prev.next = current
	}
	current.next = head
	head.prev = current
	step := func() int {
		return size / 2
	}
	var np int
	pos := 0
	current = head
	var next *Elf
	for {
		np = (pos + step()) % (size)
		next = find(current, np)
		current.val += next.val
		left := next.prev
		right := next.next
		left.next = right
		right.prev = left
		next.prev = nil
		next.next = nil
		size--
		if size == 1 {
			fmt.Printf("Elf{ id: %d, val: %d}\n", current.id, current.val)
			break
		}
		current = current.next
	}
}

func main() {
	run1()
	run2()
}
