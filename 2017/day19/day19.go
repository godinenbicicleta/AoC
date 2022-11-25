package main

import (
	"bufio"
	"fmt"
	"os"
)

// Pos represents a position
type Pos struct {
	x int
	y int
}

func getNs(p Pos, g map[Pos]rune, seen map[Pos]bool, delta Pos) (Pos, Pos, error) {
	newPos := Pos{p.x + delta.x, p.y + delta.y}
	if g[newPos] != ' ' && g[newPos] != 0 {
		return newPos, delta, nil
	}

	for _, delta := range []Pos{{1, 0}, {-1, 0}, {0, -1}, {0, 1}} {
		newPos := Pos{p.x + delta.x, p.y + delta.y}
		if g[newPos] != ' ' && g[newPos] != 0 && !seen[newPos] {
			return newPos, delta, nil
		}

	}

	return Pos{}, Pos{}, fmt.Errorf("")

}

func run(p Pos, g map[Pos]rune) string {
	var s []rune

	delta := Pos{0, 1}
	seen := map[Pos]bool{p: true}
	steps := 1
	for {
		var err interface{}
		p, delta, err = getNs(p, g, seen, delta)
		if err != nil {
			break
		}
		steps++
		seen[p] = true
		if g[p] >= 'A' && g[p] <= 'Z' {
			s = append(s, g[p])
		}
	}

	fmt.Println("Steps:", steps)
	return string(s)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	g := map[Pos]rune{}
	y := -1
	ystart := 0
	xstart := -1
	for scanner.Scan() {
		y++
		for x, c := range scanner.Text() {
			g[Pos{x, y}] = c
			if y == 0 && xstart < 0 && c == '|' {
				xstart = x
			}
		}
	}
	start := Pos{xstart, ystart}
	fmt.Println(start)
	path := run(start, g)
	fmt.Println(path)

}
