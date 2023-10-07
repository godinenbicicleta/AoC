package day06

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Coord struct {
	x     int
	y     int
	label string
}

type Point struct {
	x int
	y int
}

type Bounds struct {
	minx int
	maxx int
	miny int
	maxy int
}

func GetBounds(coords []Coord) Bounds {

	xmax := coords[0].x
	ymax := coords[0].y
	xmin := coords[0].x
	ymin := coords[0].y
	for _, c := range coords[1:] {
		if c.x < xmin {
			xmin = c.x
		}
		if c.x > xmax {
			xmax = c.x
		}

		if c.y > ymax {
			ymax = c.y
		}
		if c.x < ymin {
			ymin = c.y
		}
	}

	return Bounds{minx: xmin, miny: ymin, maxx: xmax, maxy: ymax}
}

func abs(x int) int {
	if x >= 0 {
		return x
	}
	return -x
}

func Distance(p1 Point, p2 Point) int {
	return abs(p1.x-p2.x) + abs(p1.y-p2.y)
}

func DistancePointCoord(p Point, c Coord) int {
	return Distance(p, Point{x: c.x, y: c.y})
}

func StringCoords(coords []Coord) string {
	bounds := GetBounds(coords)
	var s strings.Builder
	for y := 0; y <= bounds.maxy; y++ {
		for x := 0; x <= bounds.maxx; x++ {
			if i := FindPointInCoords(Point{x: x, y: y}, coords); i >= 0 {
				s.WriteString(coords[i].label)
			} else {
				s.WriteString(".")
			}
		}
		s.WriteString("\n")
	}
	return s.String()
}

func FindPointInCoords(point Point, coords []Coord) int {
	for i, c := range coords {
		if c.x == point.x && c.y == point.y {
			return i
		}
	}
	return -1
}

type Bounded struct {
	c       Coord
	bounded bool
	grids   int
}

func NextPoints(p Point) []Point {
	return []Point{
		{x: p.x + 1, y: p.y},
		{x: p.x - 1, y: p.y},
		{x: p.x, y: p.y - 1},
		{x: p.x, y: p.y + 1},
	}
}

func IsUnbounded(c Coord, coords []Coord) Bounded {
	seen := make(map[Point]bool)
	seen[Point{x: c.x, y: c.y}] = true
	grids := 1
	queue := NextPoints(Point{x: c.x, y: c.y})
	b := GetBounds(coords)

	for len(queue) != 0 {
		p := queue[0]
		seen[p] = true
		queue = queue[1:]
		minD := DistancePointCoord(p, c)
		candidate := minD + 1
		for _, other := range coords {
			if c == other {
				continue
			}
			otherD := DistancePointCoord(p, other)
			if otherD < candidate {
				candidate = otherD
			}
		}

		if candidate <= minD {
			continue
		}
		grids++

		for _, n := range NextPoints(p) {
			if !seen[n] {
				seen[n] = true
				if p.x > b.maxx*2 || p.x < (-b.maxx)*2 {
					return Bounded{c: c, bounded: false, grids: 0}
				}
				if p.y > b.maxy*2 || p.y < (-b.maxy)*2 {
					return Bounded{c: c, bounded: false, grids: 0}
				}
				queue = append(queue, n)
			}
		}

	}

	return Bounded{c: c, bounded: true, grids: grids}
}

func ReadCoords(fname string) []Coord {
	f, err := os.Open(fname)
	if err != nil {
		panic(err)
	}

	coords := []Coord{}

	scanner := bufio.NewScanner(f)
	label := 'A'
	for scanner.Scan() {
		text := scanner.Text()
		var x, y int
		_, err := fmt.Sscanf(text, "%d, %d", &x, &y)
		if err != nil {
			panic(err)
		}
		coord := Coord{x: x, y: y, label: string(label)}
		label = label + 1
		coords = append(coords, coord)
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}

	return coords
}

func DistanceLessThan(p Point, coords []Coord) bool {
	distance := 0
	for _, c := range coords {
		distance += DistancePointCoord(p, c)
		if distance > 10_000 {
			return false
		}
	}
	return distance < 10_000
}

func Solve(fname string) int {
	coords := ReadCoords(fname)
	maxGrids := 0

	for _, c := range coords {
		isUnb := IsUnbounded(c, coords)
		if isUnb.bounded && isUnb.grids > maxGrids {
			maxGrids = isUnb.grids
		}
	}

	return maxGrids
}
func Solve2(fname string) int {
	coords := ReadCoords(fname)
	bound := GetBounds(coords)
	region := 0
	for x := bound.minx - 10_000; x <= bound.maxx+10_000; x++ {
		for y := bound.miny - 10_000; y <= bound.maxy+10_000; y++ {
			p := Point{x, y}
			if DistanceLessThan(p, coords) {
				region++
			}
		}
	}
	return region
}
