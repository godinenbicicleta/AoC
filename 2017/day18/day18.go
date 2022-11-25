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

func play1(ins []string) {
	var sounds []int
	regs := map[string]int{}
	i := 0
Loop:
	for i >= 0 && i < len(ins) {
		in := ins[i]
		switch {
		case strings.HasPrefix(in, "snd"):
			var s string
			_, err := fmt.Sscanf(in, "snd %s", &s)
			if err != nil {
				log.Fatal("Error parsing snd ", in)
			}
			x := parse(s, regs)
			sounds = append(sounds, x)
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
		case strings.HasPrefix(in, "mul"):
			var s string
			var x string
			_, err := fmt.Sscanf(in, "mul %s %s", &x, &s)
			if err != nil {
				log.Fatal("Error parsing mul ", in)
			}
			y := parse(s, regs)
			regs[x] *= y
		case strings.HasPrefix(in, "mod"):
			var s string
			var x string
			_, err := fmt.Sscanf(in, "mod %s %s", &x, &s)
			if err != nil {
				log.Fatal("Error parsing mod ", in)
			}
			y := parse(s, regs)
			regs[x] = regs[x] % y
		case strings.HasPrefix(in, "rcv"):
			var s string
			_, err := fmt.Sscanf(in, "rcv %s", &s)
			if err != nil {
				log.Fatal("Error parsing rcv ", in)
			}
			x := parse(s, regs)
			if x != 0 {
				fmt.Println(sounds[len(sounds)-1])
				break Loop
			}
		case strings.HasPrefix(in, "jgz"):
			var s1 string
			var s2 string
			_, err := fmt.Sscanf(in, "jgz %s %s", &s1, &s2)
			if err != nil {
				log.Fatal("Error parsing jgz ", in)
			}
			x := parse(s1, regs)
			y := parse(s2, regs)
			if x > 0 {
				i += y
				continue
			}
		}
		i++
	}
}

func play2(ins []string, send chan<- int, rcv <-chan int, p int, done chan interface{}) {
	sends := 0
	regs := map[string]int{"p": p}
	i := 0
	for i >= 0 && i < len(ins) {
		in := ins[i]
		switch {
		case strings.HasPrefix(in, "snd"):
			var s string
			_, err := fmt.Sscanf(in, "snd %s", &s)
			if err != nil {
				log.Fatal("Error parsing snd ", in)
			}
			x := parse(s, regs)
			if p == 1 {
				sends++
				fmt.Println("COUNT SENDS", sends)
			}
			send <- x
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
		case strings.HasPrefix(in, "mul"):
			var s string
			var x string
			_, err := fmt.Sscanf(in, "mul %s %s", &x, &s)
			if err != nil {
				log.Fatal("Error parsing mul ", in)
			}
			y := parse(s, regs)
			regs[x] *= y
		case strings.HasPrefix(in, "mod"):
			var s string
			var x string
			_, err := fmt.Sscanf(in, "mod %s %s", &x, &s)
			if err != nil {
				log.Fatal("Error parsing mod ", in)
			}
			y := parse(s, regs)
			regs[x] = regs[x] % y
		case strings.HasPrefix(in, "rcv"):
			var s string
			_, err := fmt.Sscanf(in, "rcv %s", &s)
			if err != nil {
				log.Fatal("Error parsing rcv ", in)
			}
			regs[s] = <-rcv
		case strings.HasPrefix(in, "jgz"):
			var s1 string
			var s2 string
			_, err := fmt.Sscanf(in, "jgz %s %s", &s1, &s2)
			if err != nil {
				log.Fatal("Error parsing jgz ", in)
			}
			x := parse(s1, regs)
			y := parse(s2, regs)
			if x > 0 {
				i += y
				continue
			}
		}
		i++
	}
	close(done)
}

func main() {
	var instructions []string
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		instructions = append(instructions, scanner.Text())
	}
	play1(instructions)
	fmt.Println("PART 2")
	p1 := make(chan int, 1<<20)
	p2 := make(chan int, 1<<20)
	done := make(chan interface{})
	go play2(instructions, p2, p1, 1, done)
	go play2(instructions, p1, p2, 0, done)
	for range done {
		fmt.Println("DONE")
	}

}
