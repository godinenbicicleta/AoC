package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func run(a int, lines [][]string) {
	registers := map[string]int{
		"a": a, "b": 0, "c": 0, "d": 0,
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
		if index == 18 {
			fmt.Println(registers)
		}
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
		case "tgl":
			val := parser(parts[1])
			if index+val > 0 && index+val < len(lines) {
				old := lines[index+val]
				newInstruction := toggle(old)
				lines[index+val] = newInstruction
			}
			index++
		}
	}

	fmt.Println(registers)
}

func toggle(parts []string) []string {
	switch parts[0] {
	case "cpy":
		return []string{"jnz", parts[1], parts[2]}
	case "inc":
		return []string{"dec", parts[1]}
	case "dec":
		return []string{"inc", parts[1]}
	case "jnz":
		return []string{"cpy", parts[1], parts[2]}
	case "tgl":
		return []string{"inc", parts[1]}
	}
	os.Exit(1)
	return []string{}
}

func main() {
	buff := bufio.NewScanner(os.Stdin)
	lines := [][]string{}
	for buff.Scan() {
		line := buff.Text()
		parts := strings.Split(line, " ")
		lines = append(lines, parts)
	}

	run(12, lines)
}
