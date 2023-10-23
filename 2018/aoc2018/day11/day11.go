package main

import (
	"fmt"
	"strconv"
)

const gridSerialNumber int = 9424

type Cell struct {
	x int
	y int
}

func (c *Cell) PowerLevel() int {
	rackId := c.x + 10
	powerLevel := rackId * c.y
	powerLevel += gridSerialNumber
	powerLevel *= rackId

	if powerLevel < 100 {
		return -5
	}

	s := fmt.Sprintf("%d", powerLevel)
	hundreds, err := strconv.Atoi(s[len(s)-3 : len(s)-2])
	if err != nil {
		panic(err)
	}
	return hundreds - 5

}

type Key struct {
	x    int
	y    int
	size int
}

var cache = map[Key]int{}

func (c *Cell) TotalPower(size int) int {
	key := Key{x: c.x, y: c.y, size: size}
	if v, ok := cache[key]; ok {
		return v
	}
	if size == 1 {
		cache[key] = c.PowerLevel()
		return cache[key]
	}
	totalPower := c.TotalPower(size - 1)
	dx := size - 1
	for dy := 0; dy < size; dy++ {
		if c.x+dx > 300 || c.y+dy > 300 {
			break
		}
		cell := Cell{x: c.x + dx, y: c.y + dy}
		totalPower += cell.PowerLevel()

	}
	dy := size - 1
	for dx := 0; dx < size-1; dx++ {
		if c.x+dx > 300 || c.y+dy > 300 {
			break
		}

		cell := Cell{x: c.x + dx, y: c.y + dy}
		totalPower += cell.PowerLevel()
	}
	cache[key] = totalPower
	return totalPower
}
func main() {
	maxPower := -1
	maxCell := Cell{}
	for x := 1; x <= 300; x++ {
		for y := 1; y <= 300; y++ {
			c := Cell{x: x, y: y}
			p := c.TotalPower(3)
			if maxPower < p {
				maxPower = p
				maxCell = c
			}
		}
	}
	fmt.Println(maxPower, maxCell)
	maxPower = -1
	maxCell = Cell{}
	maxSize := 0
	for size := 1; size < 300; size++ {
		for x := 1; x <= 300; x++ {
			for y := 1; y <= 300; y++ {
				c := Cell{x: x, y: y}
				p := c.TotalPower(size)
				if maxPower < p {
					maxPower = p
					maxCell = c
					maxSize = size
				}
			}
		}
	}
	fmt.Println(maxPower, maxCell, maxSize)
}
