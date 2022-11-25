package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

// Pos represents a position
type Pos struct {
	x int
	y int
}

// Grid represents a grid
type Grid map[Pos]byte

func dimensions(g Grid) (int, int, int, int) {
	minX, minY, maxX, maxY := 0, 0, 0, 0
	for k := range g {
		x := k.x
		y := k.y
		if x > maxX {
			maxX = x
		}
		if x < minX {
			minX = x
		}
		if y < minY {
			minY = y
		}
		if y > maxY {
			maxY = y
		}
	}
	return maxX, maxY, minX, minY
}

// V represents a virus
type V struct {
	dir        Pos
	pos        Pos
	infections int
}

func turnRight(d Pos) Pos {
	switch {
	case d == Pos{0, -1}:
		return Pos{1, 0}
	case d == Pos{0, 1}:
		return Pos{-1, 0}
	case d == Pos{1, 0}:
		return Pos{0, 1}
	case d == Pos{-1, 0}:
		return Pos{0, -1}
	}
	log.Fatal("ERROR handling Pos ", d)
	return d
}

func turnLeft(d Pos) Pos {
	switch {
	case d == Pos{0, -1}:
		return Pos{-1, 0}
	case d == Pos{0, 1}:
		return Pos{1, 0}
	case d == Pos{1, 0}:
		return Pos{0, -1}
	case d == Pos{-1, 0}:
		return Pos{0, 1}
	}
	log.Fatal("ERROR handling Pos ", d)
	return d
}

func advance(p Pos, d Pos) Pos {
	return Pos{p.x + d.x, p.y + d.y}
}

func burst1(g Grid, v V) V {
	if g[v.pos] == '#' {
		v.dir = turnRight(v.dir)
		delete(g, v.pos)
	} else {
		v.dir = turnLeft(v.dir)
		g[v.pos] = '#'
		v.infections++
	}
	v.pos = advance(v.pos, v.dir)
	return v
}

func reverse(d Pos) Pos {
	switch {
	case d == Pos{1, 0}:
		return Pos{-1, 0}
	case d == Pos{-1, 0}:
		return Pos{1, 0}
	case d == Pos{0, 1}:
		return Pos{0, -1}
	case d == Pos{0, -1}:
		return Pos{0, 1}
	}
	return d
}

func burst2(g Grid, v V) V {
	switch g[v.pos] {
	case 'W':
		g[v.pos] = '#'
		v.infections++
	case '#':
		v.dir = turnRight(v.dir)
		g[v.pos] = 'F'
	case 'F':
		v.dir = reverse(v.dir)
		delete(g, v.pos)
	default:
		v.dir = turnLeft(v.dir)
		g[v.pos] = 'W'
	}
	v.pos = advance(v.pos, v.dir)
	return v
}

func (g Grid) String() string {
	maxX, maxY, minX, minY := dimensions(g)
	buff := make([]byte, 0, 2*len(g))
	for y := minY; y <= maxY; y++ {
		for x := minX; x <= maxX; x++ {
			switch g[Pos{x, y}] {
			case '#':
				buff = append(buff, '#')
			default:
				buff = append(buff, '.')
			}
		}
		buff = append(buff, '\n')
	}
	return string(buff[:len(buff)-1])
}

func cp(g Grid) Grid {

	g1 := Grid{}
	for k, v := range g {
		g1[k] = v
	}
	return g1
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	y := 0
	g := Grid{}
	maxX := 0
	for scanner.Scan() {
		for x, v := range scanner.Text() {
			pos := Pos{x, y}
			if v == rune('#') {
				g[pos] = '#'
			}
			if x > maxX {
				maxX = x
			}
		}
		y++
	}
	v := V{pos: Pos{y / 2, maxX / 2}, dir: Pos{0, -1}, infections: 0}
	v1 := v
	v2 := v
	g1 := cp(g)
	g2 := cp(g)
	fmt.Println(g)
	// part1

	for i := 0; i < 10000; i++ {
		v1 = burst1(g1, v1)
	}
	fmt.Println(v1.infections)
	for i := 0; i < 10000000; i++ {
		v2 = burst2(g2, v2)
	}
	fmt.Println(v2.infections)
}
