package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strings"
)

type Range struct {
	x0 int
	x1 int
	y0 int
	y1 int
}

type grid [][]byte

func New(ranges []Range, minX int, maxX int, minY int, maxY int) grid {
	sizeX := maxX + 1
	var grid [][]byte
	for y := 0; y <= maxY+3; y++ {
		var row []byte
		for x := 0; x <= sizeX; x++ {
			row = append(row, '.')
		}
		grid = append(grid, row)
	}

	for _, elem := range ranges {
		for y := elem.y0; y <= elem.y1; y++ {
			for x := elem.x0; x <= elem.x1; x++ {
				grid[y][x] = '#'
			}
		}
	}
	grid[0][500] = '+'
	return grid
}

func (g grid) String() string {
	var s strings.Builder
	minX := math.MaxInt
	for _, row := range g {
		for ix, v := range row {
			if v != '.' && ix < minX {
				minX = ix
			}
		}
	}
	for _, row := range g {
		for ix, x := range row {
			if ix >= minX-1 {
				s.WriteByte(x)
			}
		}
		s.WriteByte('\n')
	}
	return s.String()
}

type Point struct {
	x int
	y int
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	minY := math.MaxInt
	minX := math.MaxInt
	maxY := math.MinInt
	maxX := math.MinInt
	var ranges []Range

	for scanner.Scan() {
		txt := scanner.Text()
		var x, y, x1, x0, y0, y1 int
		_, err := fmt.Sscanf(txt, "x=%d, y=%d..%d", &x, &y0, &y1)
		if err == nil {
			if y0 < minY {
				minY = y0
			}
			if y1 > maxY {
				maxY = y1
			}
			if x > maxX {
				maxX = x
			}
			if x < minX {
				minX = x
			}
			ranges = append(ranges, Range{x0: x, x1: x, y0: y0, y1: y1})
			continue
		}
		_, err = fmt.Sscanf(txt, "y=%d, x=%d..%d", &y, &x0, &x1)
		if err != nil {
			panic(err)
		}
		if y < minY {
			minY = y
		}
		if y > maxY {
			maxY = y
		}
		if x1 > maxX {
			maxX = x1
		}
		if x0 < minX {
			minX = x0
		}

		ranges = append(ranges, Range{x0: x0, x1: x1, y0: y, y1: y})

	}

	grid := New(ranges, minX, maxX, minY, maxY)

	escapes := func(p Point) bool {
		stack := []Point{p}
		seen := make(map[Point]bool)
		goal := p.y + 1
		for len(stack) > 0 {
			current := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			seen[current] = true
			x := current.x
			y := current.y

			if y >= goal {
				return true
			}
			down := Point{x: x, y: y + 1}
			if down.y > maxY {
				continue
			}
			if grid[down.y][down.x] == '.' || grid[down.y][down.x] == '|' {
				stack = append(stack, down)
				continue
			}
			right := Point{x: x + 1, y: y}
			left := Point{x: x - 1, y: y}
			if grid[left.y][left.x] == '.' || grid[left.y][left.x] == '|' {
				if !seen[left] {
					stack = append(stack, left)
				}
			}
			if grid[right.y][right.x] == '.' || grid[right.y][right.x] == '|' {
				if !seen[right] {
					stack = append(stack, right)
				}
			}

		}
		return false
	}
	changed := true
	for changed {
		changed = false
		current := Point{x: 500, y: 1}
		queue := []Point{current}
		seen := make(map[Point]bool)
		for len(queue) > 0 {
			current := queue[0]
			queue = queue[1:]
			y := current.y
			x := current.x
			seen[current] = true
			currentVal := grid[y][x]
			down := Point{x: x, y: y + 1}
			if down.y > maxY {
				if currentVal != '|' {
					changed = true
				}
				grid[y][x] = '|'
				continue
			}

			if grid[down.y][down.x] == '.' || grid[down.y][down.x] == '|' {
				queue = append(queue, down)
			} else {
				for _, p := range []Point{{x: x + 1, y: y}, {x: x - 1, y: y}} {
					if grid[p.y][p.x] == '.' || grid[p.y][p.x] == '|' {
						if !seen[p] {
							queue = append(queue, p)
						}
					}
				}
			}

			if escapes(current) {
				if currentVal != '|' {
					changed = true
				}
				grid[y][x] = '|'
			} else {
				if currentVal != '~' {
					changed = true
				}
				grid[y][x] = '~'
			}

		}
	}

	total := 0
	p2 := 0
	for y := minY; y <= maxY; y++ {
		for x := 0; x < len(grid[0]); x++ {
			if grid[y][x] == '|' || grid[y][x] == '~' {
				total += 1
			}
			if grid[y][x] == '~' {
				p2 += 1
			}
		}
	}
	fmt.Println(total, p2)
}
