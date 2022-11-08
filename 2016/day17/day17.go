package main

import (
	"crypto/md5"
	"fmt"
)

var dirs = [...]string{"U", "D", "L", "R"}

// Position is a position in a maze
type Position struct {
	x    int
	y    int
	path string
}

func toMd5(path string) string {
	data := []byte("njfxhljp")
	data = append(data, []byte(path)...)
	s := fmt.Sprintf("%x", md5.Sum(data))
	return s[:4]
}

func ns(p Position) []Position {
	hash := toMd5(p.path)
	ps := []Position{}
	for i, c := range hash {
		if byte(c) < 'b' || byte(c) > 'f' {
			continue
		}
		dir := dirs[i]
		switch dir {
		case "D":
			if p.y+1 <= 3 {
				ps = append(ps, Position{p.x, p.y + 1, p.path + "D"})
			}
		case "U":
			if p.y-1 >= 0 {
				ps = append(ps, Position{p.x, p.y - 1, p.path + "U"})
			}
		case "L":
			if p.x-1 >= 0 {
				ps = append(ps, Position{p.x - 1, p.y, p.path + "L"})
			}
		case "R":
			if p.x+1 <= 3 {
				ps = append(ps, Position{p.x + 1, p.y, p.path + "R"})
			}
		}
	}
	return ps
}

func main() {
	seen := map[Position]bool{}

	queue := []Position{{0, 0, ""}}
	shortest := ""
	largest := 0
	for len(queue) > 0 {
		pos := queue[0]
		queue = queue[1:]
		seen[pos] = true
		if pos.x == 3 && pos.y == 3 {
			if shortest == "" {
				shortest = pos.path
			}
			if len(pos.path) > largest {
				largest = len(pos.path)
			}
			continue
		}
		for _, n := range ns(pos) {
			if seen[n] {
				continue
			}
			queue = append(queue, n)

		}
	}

	fmt.Println(shortest, largest)
}
