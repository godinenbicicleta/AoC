package main

import (
	"bufio"
	"fmt"
	"os"
	"runtime/debug"
)

func main() {
	grid := readGrid("data/day21.txt")
	dimx := len(grid[0])
	dimy := len(grid)

	rescale_func := rescale(dimx, dimy)

	total := run_for_steps(26501365, grid, rescale_func)
	fmt.Println("Total: ", total)

}

type Point struct {
	x int
	y int
}

type Key struct {
	Point
	steps int
}

func abs(x int) int {
	if x >= 0 {
		return x
	}
	return -x
}

func run_for_steps(maxsteps int, grid [][]byte, rescale_func func(int, int) (int, int)) int {
	var start Point
	for y, row := range grid {
		for x, b := range row {
			if b == 'S' {
				start = Point{x: x, y: y}
			}
		}
	}
	queue := []Key{{Point: start, steps: 0}}
	seen := make(map[Point]struct{})
	total := 0
	prev_steps := 1
	var seen_new map[Point]struct{}
	nextPrint := 1000
	for {
		current := queue[0]
		queue = queue[1:]
		x := current.x
		y := current.y
		steps := current.steps
		if steps == nextPrint {
			fmt.Println(steps)
			nextPrint += 1000
		}
		if steps == prev_steps+1000 {
			seen_new = make(map[Point]struct{})
			for k := range seen {
				if abs(k.x-start.x)+abs(k.y-start.y) < prev_steps+990 {
					continue
				}
				seen_new[k] = struct{}{}
			}
			seen = seen_new
			debug.FreeOSMemory()
			prev_steps = steps
		}
		if steps == maxsteps {
			return total
		}
		new_steps := steps + 1
		for _, p := range []Point{{x: x + 1, y: y}, {x: x - 1, y: y}, {x: x, y: y + 1}, {x: x, y: y - 1}} {
			newx, newy := rescale_func(p.x, p.y)
			if grid[newy][newx] == '#' {
				continue
			}
			if _, ok := seen[p]; ok {
				continue
			}
			seen[p] = struct{}{}
			if new_steps%2 == 1 {
				total += 1
			}
			queue = append(queue, Key{Point: p, steps: new_steps})
		}

	}
}

func readGrid(fname string) [][]byte {
	f, err := os.Open(fname)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)
	var grid [][]byte
	for scanner.Scan() {
		line := scanner.Text()
		row := make([]byte, len(line))
		for x := 0; x < len(line); x++ {
			row[x] = line[x]
		}
		grid = append(grid, row)
	}

	return grid

}

func rescale(dimx int, dimy int) func(int, int) (int, int) {
	return func(i, j int) (int, int) {
		var newx, newy int
		if i >= 0 {
			newx = i % dimx
		} else {
			newx = dimx - ((-1 * i) % dimx)
			newx = newx % (dimx)
		}
		if j >= 0 {
			newy = j % (dimy)
		} else {
			newy = dimy - ((-1 * j) % dimy)
			newy = newy % (dimy)
		}
		return newx, newy
	}
}