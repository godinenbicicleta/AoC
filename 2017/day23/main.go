package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func parse(x string, regs map[string]int) int {
	num, err := strconv.Atoi(x)
	if err != nil {
		return regs[x]
	}
	return num
}

func play(ins []string) {
	muls := 0
	regs := map[string]int{}
	i := 0
	for i >= 0 && i < len(ins) {
		in := ins[i]
		switch {
		case strings.HasPrefix(in, "set"):
			var s string
			var x string
			_, err := fmt.Sscanf(in, "set %s %s", &x, &s)
			if err != nil {
				log.Fatal("Error parsing set ", in)
			}
			y := parse(s, regs)
			regs[x] = y
		case strings.HasPrefix(in, "add"):
			var s string
			var x string
			_, err := fmt.Sscanf(in, "add %s %s", &x, &s)
			if err != nil {
				log.Fatal("Error parsing add ", in)
			}
			y := parse(s, regs)
			regs[x] += y
		case strings.HasPrefix(in, "sub"):
			var s string
			var x string
			_, err := fmt.Sscanf(in, "sub %s %s", &x, &s)
			if err != nil {
				log.Fatal("Error parsing sub ", in)
			}
			y := parse(s, regs)
			regs[x] -= y
		case strings.HasPrefix(in, "mul"):
			var s string
			var x string
			_, err := fmt.Sscanf(in, "mul %s %s", &x, &s)
			if err != nil {
				log.Fatal("Error parsing mul ", in)
			}
			y := parse(s, regs)
			regs[x] *= y
			muls++
		case strings.HasPrefix(in, "jnz"):
			var s1 string
			var s2 string
			_, err := fmt.Sscanf(in, "jnz %s %s", &s1, &s2)
			if err != nil {
				log.Fatal("Error parsing jnz ", in)
			}
			x := parse(s1, regs)
			y := parse(s2, regs)
			if x != 0 {
				i += y
				continue
			}
		}
		i++
	}
	fmt.Println(muls)
}

func main() {
	var instructions []string
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		instructions = append(instructions, scanner.Text())
	}
	play(instructions)
}
