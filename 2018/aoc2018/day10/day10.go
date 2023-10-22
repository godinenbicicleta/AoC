package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Dot struct {
	x  int
	y  int
	vx int
	vy int
}

type XY struct {
	x int
	y int
}
type Bounds struct {
	xmin int
	xmax int
	ymin int
	ymax int
}

func update(dots map[Dot]bool) (map[Dot]bool, map[XY]bool) {
	newDots := make(map[Dot]bool)
	newPos := make(map[XY]bool)
	for k, v := range dots {
		if !v {
			continue
		}

		newDot := Dot{x: k.x + k.vx, y: k.y + k.vy, vx: k.vx, vy: k.vy}
		newDots[newDot] = true
		p := XY{x: newDot.x, y: newDot.y}
		newPos[p] = true
	}

	return newDots, newPos
}

func getBounds(positions map[XY]bool) Bounds {
	bounds := Bounds{}
	for k, v := range positions {
		if !v {
			continue
		}
		bounds.ymin = k.y
		bounds.ymax = k.y

		bounds.xmin = k.x
		bounds.xmax = k.x
		break
	}

	for k, v := range positions {
		if !v {
			continue
		}
		if k.x < bounds.xmin {
			bounds.xmin = k.x
		}
		if k.x > bounds.xmax {
			bounds.xmax = k.x
		}
		if k.y > bounds.ymax {
			bounds.ymax = k.y
		}
		if k.y < bounds.ymin {
			bounds.ymin = k.y
		}
	}

	return bounds
}

func getArea(positions map[XY]bool) int {
	bounds := getBounds(positions)
	dx := (bounds.xmax - bounds.xmin)
	dy := (bounds.ymax - bounds.ymin)
	if dx < 0 {
		dx = -dx
	}
	if dy < 0 {
		dy = -dy
	}
	return dx * dy
}

func ToString(positions map[XY]bool) string {
	var builder strings.Builder
	bounds := getBounds(positions)
	for y := bounds.ymin; y <= bounds.ymax; y++ {
		for x := bounds.xmin; x <= bounds.xmax; x++ {
			xy := XY{x: x, y: y}
			if positions[xy] {
				builder.WriteString("#")
			} else {
				builder.WriteString(".")
			}
		}
		builder.WriteString("\n")

	}
	return builder.String()
}
func main() {
	f, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	dots := make(map[Dot]bool)
	pos := make(map[XY]bool)
	for scanner.Scan() {
		text := scanner.Text()
		dot := Dot{}
		fmt.Sscanf(text, "position=<%d,%d> velocity=<%d,%d>", &dot.x, &dot.y, &dot.vx, &dot.vy)
		dots[dot] = true
		xy := XY{x: dot.x, y: dot.y}
		pos[xy] = true
	}
	prev := -1
	steps := 0
	for {
		oldPos := pos
		dots, pos = update(dots)
		steps++
		newArea := getArea(pos)
		if prev == -1 {
			prev = newArea
			continue
		} else if prev < newArea {
			fmt.Println("\n", ToString(oldPos), "\n", "steps: ", steps-1)
			break
		}
		prev = newArea

	}

}
