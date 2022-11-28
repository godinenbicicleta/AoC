package main

import (
	"fmt"
	"log"
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

func isPrime(n int) bool {
	for i := 2; i <= n/2; i++ {

		if n%i == 0 {
			return false
		}
	}
	return true
}

func play(ins []string, regs map[string]int) {
	muls := 0
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
		case strings.HasPrefix(in, "--"):
			regs["g"] = 0
			regs["d"] = regs["b"]
			if isPrime(regs["b"]) {
				regs["f"] = 1
			} else {
				regs["f"] = 0
			}
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

	fmt.Println(regs)
}

func main() {
	var instructions []string
	fmt.Println("LOOP 1")
	instructions = strings.Split(strings.TrimSpace(`
set b 79
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -7
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23
`), "\n")
	play(instructions, map[string]int{"a": 0})
	fmt.Println("P2")

	instructions = strings.Split(strings.TrimSpace(`
set b 79
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
-- set g = 0, d = b, f = 1 if prime(b) else 0
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -10
`), "\n")
	play(instructions, map[string]int{"a": 1})
}
