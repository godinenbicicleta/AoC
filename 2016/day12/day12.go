package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func run(c int, lines [][]string) {
	registers := map[string]int{
		"a": 0, "b": 0, "c": c, "d": 0,
	}
	index := 0
	parser := func(s string) int {

		val, err := strconv.Atoi(s)
		if err != nil {
			return registers[s]
		}

		return val

	}
	for index < len(lines) {
		parts := lines[index]
		switch parts[0] {
		case "cpy":
			val := parser(parts[1])
			registers[parts[2]] = val
			index++
		case "inc":
			registers[parts[1]]++
			index++
		case "dec":
			registers[parts[1]]--
			index++
		case "jnz":
			x := parser(parts[1])
			y := parser(parts[2])
			if x != 0 {
				index += y
			} else {
				index++
			}
		}
	}

	fmt.Println(registers)

}

func main() {
	buff := bufio.NewScanner(os.Stdin)
	lines := [][]string{}
	for buff.Scan() {
		line := buff.Text()
		parts := strings.Split(line, " ")
		lines = append(lines, parts)
	}
	run(0, lines)
	run(1, lines)
}
