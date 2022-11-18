package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

// Position represents a position
type Position struct {
	x int
	y int
	z int
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func distance(p Position) int {
	res := abs(p.x) + abs(p.y) + abs(p.z)
	return res / 2
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		dirs := strings.Split(line, ",")
		ps := make([]Position, 0, len(dirs)+1)
		p := Position{}
		ps = append(ps, p)
		maxD := 0
		for _, dir := range dirs {
			switch dir {
			case "n":
				p = Position{p.x + 1, p.y - 1, p.z}
			case "s":
				p = Position{p.x - 1, p.y + 1, p.z}
			case "ne":
				p = Position{p.x, p.y - 1, p.z + 1}
			case "nw":
				p = Position{p.x + 1, p.y, p.z - 1}
			case "se":
				p = Position{p.x - 1, p.y, p.z + 1}
			case "sw":
				p = Position{p.x, p.y + 1, p.z - 1}
			default:
				log.Fatal("Unknown dir", dir)
			}
			ps = append(ps, p)
			if distance(p) > maxD {
				maxD = distance(p)
			}
		}
		fmt.Println(distance(ps[len(ps)-1]), maxD)
	}
}
