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
	x     int
	y     int
	size  int
	used  int
	avail int
}

// Grid is a grid
type Grid struct {
	arr   []Node
	steps int
}

// Hash hashes a grid
func Hash(g Grid) string {
	var b strings.Builder
	for _, n := range g.arr {
		fmt.Fprintf(&b, "(%d)(%d)(%d)(%d)", n.x, n.y, n.used, n.avail)
	}
	return b.String()
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	grid := Grid{}
	var x, y, size, used, avail, usep int
	var maxX, maxY int
	var goal Node
	for scanner.Scan() {
		// Filesystem              Size  Used  Avail  Use%

		line := scanner.Text()
		_, err := fmt.Sscanf(line, "/dev/grid/node-x%d-y%d     %dT   %dT    %dT   %d%%", &x, &y, &size, &used, &avail, &usep)
		if err != nil {
			log.Fatal("Couldn't parse", line)
		}
		if x > maxX {
			maxX = x
			goal = Node{x, y, size, used, avail}
		}
		if y > maxY {
			maxY = y
		}

		grid.arr = append(grid.arr, Node{x, y, size, used, avail})
	}

	done := func(g Grid) bool {
		return g.arr[0] == goal
	}

	viable := 0
	for i, n := range grid.arr {
		for j, m := range grid.arr {
			if j == i {
				continue
			}
			if n.used == 0 {
				continue
			}
			if n.used <= m.avail {
				viable++
			}
		}
	}

	grids := make([]Grid, 1, 100000)
	grids[0] = grid
	seen := map[string]bool{}

	for len(grids) > 0 {
		current := grids[0]
		grids = grids[1:]
		seen[Hash(current)] = true
		if done(current) {

		}
	}

}
