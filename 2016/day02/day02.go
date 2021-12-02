package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

var keypad1 = [][]string{
	[]string{"1", "2", "3"},
	[]string{"4", "5", "6"},
	[]string{"7", "8", "9"},
}

var keypad2 = [][]string{
	[]string{"-", "-", "1", "-", "-"},
	[]string{"-", "2", "3", "4", "-"},
	[]string{"5", "6", "7", "8", "9"},
	[]string{"-", "A", "B", "C", "-"},
	[]string{"-", "-", "D", "-", "-"},
}

func cond1(x, y int) bool {
	if x >= 0 && x < 3 && y >= 0 && y < 3 {
		return true
	}
	return false
}

type point struct {
	x int
	y int
}

func cond2(x, y int) bool {
	if x < 0 || y < 0 || y > 4 || x > 4 {
		return false
	}

	if keypad2[y][x] == "-" {
		return false
	}
	return true
}

func run(p point, lines []string, keypad [][]string, cond func(x, y int) bool) {
	x, y := p.x, p.y
	for _, line := range lines {
		for index, instruction := range line {
			prevX, prevY := x, y
			switch instruction {
			case 'U':
				y--
			case 'D':
				y++
			case 'L':
				x--
			case 'R':
				x++
			default:
				panic("no match")
			}

			if !cond(x, y) {
				x, y = prevX, prevY
			}

			if index == len(line)-1 {
				fmt.Printf("%s", keypad[y][x])
			}
		}
	}
	fmt.Println()

}

func main() {

	scanner := bufio.NewScanner(os.Stdin)

	var lines []string
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		lines = append(lines, line)
	}

	run(point{1, 1}, lines, keypad1, cond1)
	run(point{0, 2}, lines, keypad2, cond2)

}
