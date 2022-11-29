package main

import (
	"bufio"
	"fmt"
	"os"
)

// Component represents a component
type Component struct {
	id int
	x  int
	y  int
}

func sum(cs []BComponent) int {
	s := 0
	for _, elem := range cs {
		s += elem.x + elem.y
	}
	return s
}

func in(c Component, bridge []BComponent) bool {
	for _, elem := range bridge {
		if elem.id == c.id {
			return true
		}
	}
	return false
}

// BComponent represents a component in a bridge
type BComponent struct {
	id    int
	x     int
	y     int
	xUsed bool
	yUsed bool
}

func copyBridge(bridge []BComponent) []BComponent {
	nb := make([]BComponent, len(bridge)-1)
	copy(nb, bridge)
	return nb
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var cs []Component
	id := 0
	for scanner.Scan() {
		var x, y int
		fmt.Sscanf(scanner.Text(), "%d/%d", &x, &y)
		component := Component{id: id, x: x, y: y}
		cs = append(cs, component)
		id++
	}
	fmt.Println(cs)
	bridges := [][]BComponent{{{x: 0, y: 0, xUsed: false, yUsed: false, id: -1}}}
	built := [][]BComponent{}

	for len(bridges) > 0 {
		bridge := bridges[0]
		bridges = bridges[1:]
		grows := false
		for _, c := range cs {
			if in(c, bridge) {
				continue
			}
			last := bridge[len(bridge)-1]
			if last.x != c.x && last.y != c.y && last.y != c.x && last.x != c.y {
				continue
			}
			if last.x == c.x && !last.xUsed {
				nb := copyBridge(bridge)
				nb = append(nb, BComponent{x: last.x, y: last.y, xUsed: true, yUsed: last.yUsed, id: c.id})
				nb = append(nb, BComponent{x: c.x, y: c.y, xUsed: true, yUsed: false, id: c.id})
				bridges = append(bridges, nb)
				grows = true
				continue
			}
			if last.y == c.x && !last.yUsed {
				nb := copyBridge(bridge)
				nb = append(nb, BComponent{x: last.x, y: last.y, xUsed: true, yUsed: last.yUsed, id: c.id})
				nb = append(nb, BComponent{x: c.x, y: c.y, xUsed: true, yUsed: false, id: c.id})
				bridges = append(bridges, nb)
				grows = true
				continue
			}
			if last.x == c.y && !last.xUsed {
				nb := copyBridge(bridge)
				nb = append(nb, BComponent{x: last.x, y: last.y, xUsed: true, yUsed: last.yUsed, id: c.id})
				nb = append(nb, BComponent{x: c.x, y: c.y, xUsed: false, yUsed: true, id: c.id})
				bridges = append(bridges, nb)
				grows = true
				continue
			}
			if last.y == c.y && !last.yUsed {
				nb := copyBridge(bridge)
				nb = append(nb, BComponent{x: last.x, y: last.y, xUsed: true, yUsed: last.yUsed, id: c.id})
				nb = append(nb, BComponent{x: c.x, y: c.y, xUsed: false, yUsed: true, id: c.id})
				bridges = append(bridges, nb)
				grows = true
				continue
			}
		}
		if !grows {
			built = append(built, bridge)
		}
	}
	maxSum := 0
	for _, b := range built {
		s := sum(b)
		if s > maxSum {
			maxSum = s
		}
	}
	fmt.Println(maxSum)

	var maxLengthB int
	for _, b := range built {
		if len(b) > maxLengthB {
			maxLengthB = len(b)
		}
	}
	fmt.Println(maxLengthB)
	maxValue := 0
	for _, b := range built {
		if len(b) == maxLengthB && sum(b) > maxValue {
			maxValue = sum(b)
		}
	}
	fmt.Println(maxValue)
}
