package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

// Position represents a position
type Position struct {
	x int
	y int
}

// Value represents a value
type Value string

// Maze represents a maze
type Maze struct {
	m       map[Position]Value
	targets map[Value]Position
	maxX    int
	maxY    int
	start   Position
}

// Value represents a value
func read() Maze {
	scanner := bufio.NewScanner(os.Stdin)
	y := 0
	maze := Maze{m: map[Position]Value{}, targets: map[Value]Position{}}
	var x int
	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), "")
		for x, c := range parts {
			p := Position{x: x, y: y}
			maze.m[p] = Value(c)
			if i, err := strconv.Atoi(c); err == nil {
				if i > 0 {
					maze.targets[Value(c)] = p
				} else {
					maze.start = p
				}
			}
		}
		y++
		x = len(parts)
	}
	maze.maxX = x
	maze.maxY = y
	return maze
}

func (m Maze) String() string {
	var b strings.Builder
	for y := 0; y <= m.maxY; y++ {
		for x := 0; x <= m.maxX; x++ {
			p := Position{x: x, y: y}
			fmt.Fprintf(&b, "%s", m.m[p])
		}
		fmt.Fprintf(&b, "\n")
	}
	return b.String()
}

// Node represents a Node
type Node struct {
	position Position
	visited  map[Value]bool
	steps    int
}

func getMissing(m Maze, n Node) []Value {
	res := []Value{}
	for target := range m.targets {
		if n.visited[target] {
			continue
		}
		res = append(res, target)
	}
	if len(res) == 0 {
		return []Value{"0"}
	}
	return res
}

type ps struct {
	p Position
	s int
}

func vs(m Maze, p Position) []Position {
	x := p.x
	y := p.y
	v := []Position{}
	v1 := Position{x + 1, y}
	v2 := Position{x - 1, y}
	v3 := Position{x, y + 1}
	v4 := Position{x, y - 1}
	candidates := []Position{v1, v2, v3, v4}
	for _, c := range candidates {
		if c.x >= 0 && c.x <= m.maxX && c.y >= 0 && c.y <= m.maxY && m.m[c] != "#" {
			v = append(v, c)
		}
	}
	return v
}

func getShortestPath(m Maze, start Position, goal Position) int {
	seen := map[Position]bool{start: true}
	queue := []ps{{start, 0}}
	for len(queue) > 0 {
		p := queue[0]
		queue = queue[1:]
		if p.p == goal {
			return p.s
		}
		for _, v := range vs(m, p.p) {
			if seen[v] {
				continue
			}
			seen[v] = true
			queue = append(queue, ps{p: v, s: p.s + 1})

		}

	}

	os.Exit(1)
	return 0
}
func main() {
	m := read()
	fmt.Print(m)
	fmt.Println(m.targets)

	initial := Node{position: m.start, visited: map[Value]bool{}}
	queue := []Node{initial}

	for len(queue) > 0 {
		sort.Slice(queue, func(i, j int) bool {
			return queue[i].steps < queue[j].steps
		})
		n := queue[0]
		queue = queue[1:]
		if len(n.visited) == len(m.targets)+1 {
			fmt.Println(n.steps)
			os.Exit(0)
		}
		for _, missingTarget := range getMissing(m, n) {

			targetPos, ok := m.targets[missingTarget]
			if !ok {
				targetPos = m.start
			}
			delta := getShortestPath(m, n.position, targetPos)
			newVisited := map[Value]bool{}
			for k, v := range n.visited {
				newVisited[k] = v
			}
			newVisited[missingTarget] = true
			newNode := Node{position: targetPos, visited: newVisited, steps: n.steps + delta}
			queue = append(queue, newNode)
		}

	}
}
