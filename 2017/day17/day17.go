package main

import "fmt"

func run(s int, size int) (int, []int) {
	b := make([]int, 1, size+1)
	b[0] = 0
	steps := s
	ix := 0
	for i := 1; i <= size; i++ {
		ix = ((ix + steps) % len(b))
		b = append(b, i)
		ix = (ix + 1) % len(b)
		copy(b[ix+1:], b[ix:])
		b[ix] = i
	}
	return ix, b
}

// Node represents a node
type Node struct {
	value int
	next  *Node
	prev  *Node
}

func main() {
	ix, b := run(366, 2017)
	ix = (ix + 1) % len(b)
	fmt.Println(b[ix])

	n := &Node{}
	n.prev = n
	n.next = n
	current := n
	for i := 1; i <= 50000000; i++ {
		for j := 0; j < 366; j++ {
			current = current.next
		}
		newNode := &Node{i, current.next, current}
		current.next.prev = newNode
		current.next = newNode
		current = newNode
	}
	fmt.Println(n.next)
}
