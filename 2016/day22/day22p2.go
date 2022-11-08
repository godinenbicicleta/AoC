package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

// Node is a node
type Node struct {
	size int
	data Data
}

func (n Node) String() string {
	return fmt.Sprintf("Node(size: %d, data: %v)", n.size, n.data)
}

func (n Node) used() int {
	return n.data.size
}

func (n Node) avail() int {
	return n.size - n.used()
}

// Data represents data
type Data struct {
	id   int
	size int
}

func (d Data) String() string {
	return fmt.Sprintf("Data(id: %d, size: %d)", d.id, d.size)
}

// Position is a Position in a Grid
type Position struct {
	x int
	y int
}

func (p Position) String() string {
	return fmt.Sprintf("(x=%d,y=%d)", p.x, p.y)
}

// Grid is a grid
type Grid struct {
	grids map[Position]Node
	steps int
	holeP Position
	goalP Position
}

func (g Grid) String() string {
	var b strings.Builder
	fmt.Fprint(&b, "------------\n")
	for y := 0; y <= maxY; y++ {
		for x := 0; x <= maxX; x++ {
			p := Position{x: x, y: y}
			if x == 0 && y == 0 {
				fmt.Fprint(&b, "(")
			} else {
				fmt.Fprint(&b, " ")
			}
			if g.goalP == p {
				fmt.Fprint(&b, "G")
			} else if g.holeP == p {
				fmt.Fprint(&b, "-")
			} else {
				fmt.Fprint(&b, ".")
			}
			if x == 0 && y == 0 {
				fmt.Fprint(&b, ")")
			} else {
				fmt.Fprint(&b, " ")
			}
		}
		if y == 0 {
			fmt.Fprintf(&b, "\tsteps: %d", g.steps)
		}
		fmt.Fprint(&b, "\n")
	}

	return b.String()
}

var maxX int
var maxY int

// New creates a new Grid as copy of an old one
func New(old Grid) Grid {
	steps := old.steps
	newGrids := map[Position]Node{}
	var holeP Position
	var goalP Position
	for position, node := range old.grids {
		newGrids[position] = Node{size: node.size, data: node.data}
		if node.data.size == 0 {
			holeP = position
		}
		if node.data.id == goalID {
			goalP = position
		}
	}
	return Grid{steps: steps, grids: newGrids, holeP: holeP, goalP: goalP}
}

func abs(i int) int {
	if i < 0 {
		return -1 * i
	}
	return i
}

func vs(p Position) []Position {
	vs := []Position{}
	x := p.x
	y := p.y
	if x+1 <= maxX {
		vs = append(vs, Position{x: x + 1, y: y})
	}
	if x-1 >= 0 {
		vs = append(vs, Position{x: x - 1, y: y})
	}
	if y+1 <= maxY {
		vs = append(vs, Position{y: y + 1, x: x})
	}
	if y-1 >= 0 {
		vs = append(vs, Position{y: y - 1, x: x})
	}

	return vs

}

func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func max(x, y int) int {
	if x > y {
		return x
	}
	return y
}

var goalID int

type gp struct {
	p    Position
	path []Position
}

func getShortestPath(g Grid, start Position, goal Position) []Position {
	queue := make([]gp, 1, 100)
	queue[0] = gp{p: start, path: []Position{}}
	seen := map[Position]bool{}
	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]
		seen[current.p] = true
		if current.p == goal {
			return current.path
		}
		for _, np := range vs(current.p) {
			if g.grids[g.goalP].used() > g.grids[np].size || seen[np] {
				continue
			}
			seen[np] = true
			newPath := make([]Position, len(current.path))
			copy(newPath, current.path)
			newPath = append(newPath, np)
			queue = append(queue, gp{p: np, path: newPath})
		}

	}
	os.Exit(1)
	return []Position{}
}

func moveHole(g Grid, dest Position) (newG Grid, delta int) {
	done := func(g Grid) bool {
		return g.holeP == dest
	}
	g = New(g)
	g.steps = 0

	queue := make([]Grid, 1, 1000000)
	queue[0] = g
	seen := map[Position]bool{}
	seen[g.holeP] = true
	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]
		if done(current) {
			return current, current.steps
		}

		holePosition := current.holeP
		holeNode := current.grids[holePosition]

		for _, positionB := range vs(holePosition) {
			nodeB := current.grids[positionB]
			if nodeB.used() > current.grids[holePosition].avail() {
				continue
			}
			newNodeH := Node{size: holeNode.size, data: nodeB.data}
			newNodeB := Node{size: nodeB.size, data: holeNode.data}
			newGrid := New(current)
			newGrid.grids[holePosition] = newNodeH
			newGrid.grids[positionB] = newNodeB
			if nodeB.data.id == goalID {
				continue
			}
			newGrid.steps++
			newGrid.holeP = positionB
			if seen[positionB] {
				continue
			}
			seen[positionB] = true
			queue = append(queue, newGrid)
		}
	}

	os.Exit(1)

	return g, 0
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	grid := Grid{grids: map[Position]Node{}, steps: 0}
	var x, y, size, used, avail, usep int
	id := 0
	for scanner.Scan() {
		// Filesystem              Size  Used  Avail  Use%
		line := scanner.Text()
		_, err := fmt.Sscanf(line, "/dev/grid/node-x%d-y%d     %dT   %dT    %dT   %d%%", &x, &y, &size, &used, &avail, &usep)
		if err != nil {
			log.Fatal("Couldn't parse", line)
		}
		position := Position{x: x, y: y}
		if x > maxX {
			maxX = x
			goalID = id
			grid.goalP = position
		}
		if y > maxY {
			maxY = y
		}

		if used == 0 {
			grid.holeP = position
		}

		grid.grids[position] = Node{size: size, data: Data{id: id, size: used}}
		id++
	}

	shortest := getShortestPath(grid, grid.goalP, Position{0, 0})
	res := 0
	testGrid := New(grid)
	delta := 0
	for len(shortest) > 0 {
		pos := shortest[0]
		shortest = shortest[1:]
		res++
		testGrid, delta = moveHole(testGrid, pos)
		holePosition := testGrid.holeP
		positionB := testGrid.goalP
		// exchange goal and hole
		holeNode := testGrid.grids[testGrid.holeP]
		nodeB := testGrid.grids[testGrid.goalP]
		newNodeH := Node{size: holeNode.size, data: nodeB.data}
		newNodeB := Node{size: nodeB.size, data: holeNode.data}
		newGrid := New(testGrid)
		newGrid.grids[holePosition] = newNodeH
		newGrid.grids[positionB] = newNodeB
		newGrid.goalP = holePosition
		newGrid.holeP = positionB
		testGrid = newGrid
		res += delta
	}
	fmt.Println(res)
}
