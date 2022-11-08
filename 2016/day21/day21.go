package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func safeEnd(s string, i int) int {
	if i < len(s) {
		return i
	}
	return len(s)
}
func safeStart(s string, i int) int {
	if i < len(s) {
		return i
	}
	return len(s)
}

func reverse(s string) string {
	rev := make([]byte, len(s), len(s))
	for i := 0; i < len(s); i++ {
		rev[i] = s[len(s)-i-1]
	}
	return string(rev)
}

func rotateRight(s string, times int) string {
	ol := len(s)
	times = times % ol
	s = s + s
	s = s[len(s)-times-ol : len(s)-times]
	return s
}
func rotateLeft(s string, times int) string {
	ol := len(s)
	times = times % ol
	s = s + s
	s = s[times : times+ol]
	return s
}

func run(start string, instruction string) string {
	parse := func(fmtString string, targets ...any) (n int, err error) {
		n, err = fmt.Sscanf(instruction, fmtString, targets...)
		return
	}
	if strings.HasPrefix(instruction, "move position") {
		var x int
		var y int
		parse("move position %d to position %d", &x, &y)
		letter := string(start[x])
		start = strings.Join([]string{start[:x], start[safeEnd(start, x+1):]}, "")
		start = strings.Join([]string{start[:y], letter, start[safeEnd(start, y):]}, "")
		return start
	}
	if strings.HasPrefix(instruction, "reverse positions") {
		var x int
		var y int
		parse("reverse positions %d through %d", &x, &y)
		start = strings.Join([]string{start[:x], reverse(start[x : y+1]), start[safeStart(start, y+1):]}, "")
		return start
	}
	if strings.HasPrefix(instruction, "rotate based on position") {
		var x string
		parse("rotate based on position of letter %s", &x)
		delta := 0
		index := strings.Index(start, x)
		if index >= 4 {
			delta++
		}
		start = rotateRight(start, 1+index+delta)
		return start
	}
	if strings.HasPrefix(instruction, "rotate left") {
		var x int
		n, _ := parse("rotate left %d step", &x)
		if n != 1 {
			parse("rotate left %d steps", &x)
		}
		start = rotateLeft(start, x)
		return start
	}
	if strings.HasPrefix(instruction, "rotate right") {
		var x int
		n, _ := parse("rotate right %d step", &x)
		if n != 1 {
			parse("rotate right %d steps", &x)
		}

		start = rotateRight(start, x)
		return start
	}
	if strings.HasPrefix(instruction, "swap letter") {
		var x string
		var y string
		parse("swap letter %s with letter %s", &x, &y)
		ix := strings.Index(start, x)
		iy := strings.Index(start, y)
		bs := []byte(start)
		bs[ix] = y[0]
		bs[iy] = x[0]
		return string(bs)

	}
	if strings.HasPrefix(instruction, "swap position") {
		var x int
		var y int
		parse("swap position %d with position %d", &x, &y)
		bs := []byte(start)
		bs[x], bs[y] = start[y], start[x]
		return string(bs)
	}

	os.Exit(1)
	return start

}

func perms(w string) []string {
	if len(w) == 0 {
		return []string{}
	}
	if len(w) == 1 {
		return []string{w}
	}
	ps := []string{}

	for _, c := range w {
		for _, p := range perms(strings.Replace(w, string(c), "", 1)) {
			ps = append(ps, string(c)+p)
		}
	}
	return ps

}

func scramble(s string, instructions []string) string {
	for _, instruction := range instructions {
		s = run(s, instruction)
	}

	return s
}

func main() {

	scanner := bufio.NewScanner(os.Stdin)
	instructions := []string{}
	var start string
	i := 0
	for scanner.Scan() {
		if i == 0 {
			start = scanner.Text()
			i++
			continue
		}

		instructions = append(instructions, scanner.Text())
	}

	fmt.Println(scramble(start, instructions))
	for _, w := range perms("fbgdceah") {
		if scramble(w, instructions) == "fbgdceah" {
			fmt.Println(w)
			break
		}
	}

}
