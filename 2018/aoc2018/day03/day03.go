package day03

import (
	"bufio"
	"fmt"
	"os"
)

type Rect struct {
	id int
	x0 int
	y0 int
	x1 int
	y1 int
}

func (r Rect) Contains(x int, y int) bool {
	return x <= r.x1 && x >= r.x0 && y <= r.y1 && y >= r.y0
}

func (r Rect) Intersects(other Rect) bool {
	if r.x1 < other.x0 || r.x0 > other.x1 {
		return false
	}
	if r.y0 > other.y1 || r.y1 < other.y0 {
		return false
	}
	return true
}

func Parse(line string) Rect {
	var x0 int
	var y0 int
	var id int
	var w int
	var h int

	fmt.Sscanf(line, "#%d @ %d,%d: %dx%d", &id, &x0, &y0, &w, &h)
	return Rect{id: id, x0: x0, y0: y0, x1: x0 + w - 1, y1: y0 + h - 1}
}

func MinMaxX(rects []Rect) (int, int) {
	minx := -1
	maxx := -1
	for _, rect := range rects {
		if minx == -1 {
			minx = rect.x0
		}
		if maxx == -1 {
			maxx = rect.x1
		}
		if rect.x0 < minx {
			minx = rect.x0
		}
		if rect.x1 > maxx {
			maxx = rect.x1
		}
	}
	return minx, maxx
}
func MinMaxY(rects []Rect) (int, int) {
	miny := -1
	maxy := -1
	for _, rect := range rects {
		if miny == -1 {
			miny = rect.y0
		}
		if maxy == -1 {
			maxy = rect.y1
		}
		if rect.y0 < miny {
			miny = rect.y0
		}
		if rect.y1 > maxy {
			maxy = rect.y1
		}
	}
	return miny, maxy
}

func ParseRects(fname string) []Rect {
	file, err := os.Open(fname)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	rects := []Rect{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		rect := Parse(line)
		rects = append(rects, rect)
	}
	return rects

}

func TwoOrMore(fname string) int {
	rects := ParseRects(fname)
	minx, maxx := MinMaxX(rects)
	miny, maxy := MinMaxY(rects)
	count := 0
	for x := minx; x <= maxx; x++ {
		for y := miny; y <= maxy; y++ {
			contains := 0
			for _, rect := range rects {
				if rect.Contains(x, y) {
					contains++
					if contains >= 2 {
						count++
						break
					}
				}
			}
		}
	}
	return count
}
func NoIntersects(fname string) int {
	rects := ParseRects(fname)
outer:
	for i, rect := range rects {
		for j, other := range rects {
			if j == i {
				continue
			}
			if rect.Intersects(other) {
				continue outer
			}
		}
		return rect.id
	}
	panic("")
}
