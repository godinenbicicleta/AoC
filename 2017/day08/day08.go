package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func valid(registers map[string]int, cond string, reg string, num int) bool {
	switch cond {
	case ">":
		return registers[reg] > num
	case ">=":
		return registers[reg] >= num
	case "<":
		return registers[reg] < num
	case "<=":
		return registers[reg] <= num
	case "==":
		return registers[reg] == num
	case "!=":
		return registers[reg] != num
	}
	log.Fatal("Invalid cond", cond)
	return false
}

func process(line string, registers map[string]int) {
	var reg1, reg2, inst, cond string
	var num1, num2 int

	_, err := fmt.Sscanf(line, "%s %s %d if %s %s %d", &reg1, &inst, &num1, &reg2, &cond, &num2)

	if err != nil {
		log.Fatal("Error parsing line")
	}

	if !valid(registers, cond, reg2, num2) {
		return
	}

	switch inst {
	case "inc":
		registers[reg1] += num1
	case "dec":
		registers[reg1] -= num1
	default:
		log.Fatal("invalid inst", inst)
	}

}

func max(registers map[string]int) int {
	var maxV int
	for _, v := range registers {
		if v > maxV {
			maxV = v
		}
	}
	return maxV
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	registers := make(map[string]int)
	maxV := 0
	for scanner.Scan() {
		line := scanner.Text()
		process(line, registers)
		v := max(registers)
		if v > maxV {
			maxV = v
		}
	}

	fmt.Println(max(registers))
	fmt.Println(maxV)
}
