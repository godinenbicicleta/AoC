package main

import (
	"fmt"
	"strings"
)

// Position represents a Position
type Position struct {
	x int
	y int
}

func getMax(g map[Position]int) (int, int) {
	var maxX, maxY int
	for k := range g {
		if k.x > maxX {
			maxX = k.x
		}
		if k.y > maxY {
			maxY = k.y
		}
	}
	return maxX, maxY
}

func gridString(g map[Position]int) string {
	x, y := getMax(g)
	var b strings.Builder
	for j := y; j >= -1*y; j-- {
		for i := -1 * x; i <= x; i++ {
			p := Position{x: i, y: j}
			fmt.Fprintf(&b, "%5d", g[p])
		}
		fmt.Fprint(&b, "\n")
	}
	return b.String()
}

func abs(x int) int {
	if x < 0 {
		return -1 * x
	}
	return x
}

func checkNum(cond bool, p Position) {
	if cond {
		fmt.Println(abs(p.x) + abs(p.y))
	}
}

var printed = false

func ns(vs map[Position]int, p Position, input int) int {
	res := 0
	x := p.x
	y := p.y
	for _, n := range []Position{{x + 1, y}, {x - 1, y}, {x, y + 1}, {x, y - 1}, {x - 1, y - 1}, {x + 1, y + 1}, {x - 1, y + 1}, {x + 1, y - 1}} {
		res += vs[n]
	}
	if res > input && !printed {
		fmt.Println(res)
		printed = true
	}
	return res
}

func main() {
	input := 289326
	start := Position{0, 0}
	num := 1
	grid := map[Position]int{start: 1}
	vals := map[Position]int{start: 1}
	for delta := 1; num <= input; delta++ {
		for i := -delta + 1; i <= delta; i++ {
			num++
			p := Position{start.x + delta, start.y + i}
			grid[p] = num
			checkNum(input == num, p)
			vals[p] = ns(vals, p, input)
		}
		for i := delta - 1; i >= -1*delta; i-- {
			num++
			p := Position{start.x + i, start.y + delta}
			grid[p] = num
			checkNum(input == num, p)
			vals[p] = ns(vals, p, input)
		}
		for i := delta - 1; i >= -1*delta; i-- {
			num++
			p := Position{start.x - delta, start.y + i}
			grid[p] = num
			checkNum(input == num, p)
			vals[p] = ns(vals, p, input)
		}
		for i := -delta + 1; i <= delta; i++ {
			num++
			p := Position{start.x + i, start.y - delta}
			grid[p] = num
			checkNum(input == num, p)
			vals[p] = ns(vals, p, input)
		}
	}

}
