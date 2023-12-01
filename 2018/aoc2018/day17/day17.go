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
	fmt.Println(sizeX)
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
	fmt.Println("minx", minX)
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

func ns(current Point) []Point {
	return []Point{
		{x: current.x - 1, y: current.y},
		{x: current.x + 1, y: current.y},
	}
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
	fmt.Println(minX, maxX, minY, maxY)

	grid := New(ranges, minX, maxX, minY, maxY)
	fmt.Println(grid)

	atGoal := func(p Point) bool {
		return p.y >= maxY
	}
	end := false
	fmt.Println(end)
	for m := 0; !end; m++ {

		queue := []Point{{x: 500, y: 1}}
		seen := make(map[Point]bool)
		seen[queue[0]] = true
		for len(queue) > 0 {
			current := queue[0]
			queue = queue[1:]
			grid[current.y][current.x] = '|'
			if atGoal(current) {
				end = true
				continue
			}
			if grid[current.y+1][current.x] == '.' || grid[current.y+1][current.x] == '|' {
				p := Point{x: current.x, y: current.y + 1}
				seen[p] = true
				queue = append(queue, Point{x: current.x, y: current.y + 1})
				continue
			}
			right := Point{x: current.x + 1, y: current.y}
			left := Point{x: current.x - 1, y: current.y}
			added := false
			if right.x < len(grid[0]) && !seen[right] && (grid[right.y][right.x] == '.' || grid[right.y][right.x] == '|') {
				queue = append(queue, right)
				seen[right] = true
				added = true
			}
			if left.x >= 0 && !seen[left] && (grid[left.y][left.x] == '.' || grid[left.y][left.x] == '|') {
				queue = append(queue, left)
				seen[left] = true
				added = true
			}
			if !added {
				grid[current.y][current.x] = '~'
			}
		}
	}

	fmt.Println(grid)
	total := 0
	for y := minY; y <= maxY; y++ {
		for x := 0; x < len(grid[0]); x++ {
			if grid[y][x] == '|' || grid[y][x] == '~' {
				total += 1
			}
		}
	}
	fmt.Println(total, maxY)
}
