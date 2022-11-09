package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func run(a int, lines [][]string) []int {
	res := []int{}
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
		if len(res) > 100 {
			return res
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
		case "out":
			val := parser(parts[1])
			if val == 0 || val == 1 {
				if len(res) > 1 && res[len(res)-1] == val {
					return []int{}
				}
				res = append(res, val)
			} else {
				return []int{}
			}
			index++
		}

	}
	return []int{}
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
	case "out":
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

	for i := 0; ; i++ {
		res := run(i, lines)
		if i%10000 == 0 {
			fmt.Println(i)
		}
		if len(res) > 0 {
			fmt.Println("DONE", i)
			os.Exit(0)
		}
	}

}
