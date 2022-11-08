package main

import (
	"fmt"
	"math"
	"strings"
)

func isEven(n int) bool {
	return n%2 == 0
}

type value int

const (
	wall value = iota
	open
)

type point struct {
	x int
	y int
}

type position struct {
	p     point
	steps int
}

func getValue(fav int, p point) value {
	x := p.x
	y := p.y
	num := x*x + 3*x + 2*x*y + y + y*y + fav
	bin := fmt.Sprintf("%b", num)
	c := strings.Count(bin, "1")
	if isEven(c) {
		return open
	}
	return wall

}
func neighbors(p point, gv func(p point) value) []point {
	cs := []point{
		{p.x, p.y + 1},
		{p.x, p.y - 1},
		{p.x + 1, p.y},
		{p.x - 1, p.y},
	}
	ps := make([]point, 0, 4)

	for _, p := range cs {
		if p.x < 0 || p.y < 0 || gv(p) == wall {
			continue
		}

		ps = append(ps, p)
	}

	return ps

}

type result struct {
	steps int
	seen  map[point]bool
}

func run(x, y, fav, maxDist int) int {
	goal := point{x: x, y: y}
	queue := make([]position, 1, 1000)
	start := position{p: point{1, 1}, steps: 0}
	queue[0] = start
	seen := map[point]bool{}
	gv := func(p point) value { return getValue(fav, p) }
	ns := func(p point) []point { return neighbors(p, gv) }

	for len(queue) > 0 {
		p := queue[0]
		queue = queue[1:]
		seen[p.p] = true
		if p.p == goal {
			return p.steps
		}

		for _, n := range ns(p.p) {
			if seen[n] || p.steps+1 > maxDist {
				continue
			}
			queue = append(queue, position{p: n, steps: p.steps + 1})
		}

	}

	total := 0

	for _, v := range seen {
		if v {
			total++
		}
	}
	return total

}

func main() {
	fmt.Println(run(7, 4, 10, math.MaxInt))
	fmt.Println(run(31, 39, 1352, math.MaxInt))
	fmt.Println(run(31, 39, 1352, 50))
}
