package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type M struct {
	registers []int
}

func NewM(o int, a int, b int, c int) M {
	return M{registers: []int{o, a, b, c}}
}

func addr(m M, a int, b int, c int) {
	m.registers[c] = m.registers[a] + m.registers[b]
}
func addi(m M, a int, b int, c int) {
	m.registers[c] = m.registers[a] + b
}
func mulr(m M, a int, b int, c int) {
	m.registers[c] = m.registers[a] * m.registers[b]
}
func muli(m M, a int, b int, c int) {
	m.registers[c] = m.registers[a] * b
}
func banr(m M, a int, b int, c int) {
	m.registers[c] = m.registers[a] & m.registers[b]
}
func bani(m M, a int, b int, c int) {
	m.registers[c] = m.registers[a] & b
}
func borr(m M, a int, b int, c int) {
	m.registers[c] = m.registers[a] | m.registers[b]
}
func bori(m M, a int, b int, c int) {
	m.registers[c] = m.registers[a] | b
}
func setr(m M, a int, b int, c int) {
	m.registers[c] = m.registers[a]
}
func seti(m M, a int, b int, c int) {
	m.registers[c] = a
}
func gtir(m M, a int, b int, c int) {
	if a > m.registers[b] {
		m.registers[c] = 1
	} else {
		m.registers[c] = 0
	}
}
func gtri(m M, a int, b int, c int) {
	if m.registers[a] > b {
		m.registers[c] = 1
	} else {
		m.registers[c] = 0
	}
}
func gtrr(m M, a int, b int, c int) {
	if m.registers[a] > m.registers[b] {
		m.registers[c] = 1
	} else {
		m.registers[c] = 0
	}
}
func eqir(m M, a int, b int, c int) {
	if a == m.registers[b] {
		m.registers[c] = 1
	} else {
		m.registers[c] = 0
	}
}
func eqri(m M, a int, b int, c int) {
	if m.registers[a] == b {
		m.registers[c] = 1
	} else {
		m.registers[c] = 0
	}
}
func eqrr(m M, a int, b int, c int) {
	if m.registers[a] == m.registers[b] {
		m.registers[c] = 1
	} else {
		m.registers[c] = 0
	}
}

var funcs = map[string]func(M, int, int, int){
	"addr": addr,
	"addi": addi,
	"mulr": mulr,
	"muli": muli,
	"banr": banr,
	"bani": bani,
	"borr": borr,
	"bori": bori,
	"setr": setr,
	"seti": seti,
	"gtir": gtir,
	"gtri": gtri,
	"gtrr": gtrr,
	"eqir": eqir,
	"eqri": eqri,
	"eqrr": eqrr,
}

type Line struct {
	before      []int
	instruction []int
	after       []int
}

func main() {
	f, err := os.Open("input1.txt")
	if err != nil {
		panic(err)
	}
	scanner := bufio.NewScanner(f)
	var lines []Line
	var current [][]int
	for scanner.Scan() {
		txt := scanner.Text()
		if strings.HasPrefix(txt, "Before") {
			var o, a, b, c int
			fmt.Sscanf(txt, "Before: [%d, %d, %d, %d]", &o, &a, &b, &c)
			current = append(current, []int{o, a, b, c})
		} else if strings.HasPrefix(txt, "After") {
			var o, a, b, c int
			fmt.Sscanf(txt, "After: [%d, %d, %d, %d]", &o, &a, &b, &c)
			current = append(current, []int{o, a, b, c})
		} else if len(txt) > 5 {
			var o, a, b, c int
			fmt.Sscanf(txt, "%d %d %d %d", &o, &a, &b, &c)
			current = append(current, []int{o, a, b, c})
		} else {
			line := Line{before: current[0], instruction: current[1], after: current[2]}
			lines = append(lines, line)
			current = [][]int{}
		}
	}

	candidates := make([][]string, 16)
	threeOrMore := 0
	var samples []Line
	for _, line := range lines {
		success := 0
	outer:
		for n, f := range funcs {
			before := line.before
			m := NewM(before[0], before[1], before[2], before[3])
			f(m, line.instruction[1], line.instruction[2], line.instruction[3])
			expected := line.after
			actual := m.registers
			for i := 0; i < 4; i++ {
				if expected[i] != actual[i] {
					continue outer
				}
			}
			success++
			if success == 3 {
				threeOrMore++
				samples = append(samples, line)
			}
			if success >= 3 {
				exists := false
				for _, elem := range candidates[line.instruction[0]] {
					if elem == n {
						exists = true
						break

					}
				}
				if !exists {
					candidates[line.instruction[0]] = append(candidates[line.instruction[0]], n)
				}
			}
		}
	}
	fmt.Println(len(samples))
	funcNames := make([]string, 0, len(funcs))

	for i := range funcs {
		funcNames = append(funcNames, i)
	}
	for i := 0; i < len(candidates); i++ {
		if len(candidates[i]) == 0 {
			candidates[i] = append(candidates[i], funcNames...)
		}
	}

	assignments := make(map[int]string)
	taken := make(map[string]bool)

	Fill(assignments, lines, candidates, taken)
	//func Solves(samples []Line, candidate string, opcode int) bool {
	for opcode, candidate := range assignments {

		if !Solves(lines, candidate, opcode) {
			panic("err")
		}
	}

	f, err = os.Open("input2.txt")
	if err != nil {
		panic(err)
	}
	scanner = bufio.NewScanner(f)
	m := NewM(0, 0, 0, 0)

	for scanner.Scan() {
		txt := scanner.Text()
		var o, a, b, c int
		fmt.Sscanf(txt, "%d %d %d %d", &o, &a, &b, &c)
		name := assignments[o]
		f := funcs[name]

		f(m, a, b, c)
	}
	fmt.Println(m.registers[0])

}

func Fill(assignments map[int]string, samples []Line, candidates [][]string, taken map[string]bool) bool {
	if Solved(assignments) {
		return true
	}
	minIx := MinIx(candidates)
	for _, elem := range candidates[minIx] {
		if taken[elem] {
			continue
		}
		assignments[minIx] = elem
		taken[elem] = true
		if !Solves(samples, elem, minIx) {
			assignments[minIx] = ""
			taken[elem] = false
			continue
		}
		newCandidates := [][]string{}
		for i, elem := range candidates {
			if i != minIx {
				newS := make([]string, len(elem))
				copy(newS, elem)
				newCandidates = append(newCandidates, newS)
			} else {
				newCandidates = append(newCandidates, []string{})
			}
		}
		if Fill(assignments, samples, newCandidates, taken) {
			return true
		}
		assignments[minIx] = ""
		taken[elem] = false
	}
	return false
}

func Solved(assignments map[int]string) bool {
	if len(assignments) < 16 {
		return false
	}
	for _, elem := range assignments {
		if elem == "" {
			return false
		}
	}
	return true
}

func MinIx(candidates [][]string) int {
	minIx := len(candidates) + 1
	minLen := len(funcs) + 1
	for ix, c := range candidates {
		if len(c) == 0 {
			continue
		}
		if len(c) < minLen {
			minIx = ix
			minLen = len(c)
		}
	}
	return minIx
}

func Solves(samples []Line, candidate string, opcode int) bool {
	for _, line := range samples {
		if line.instruction[0] != opcode {
			continue

		}
		before := line.before
		m := NewM(before[0], before[1], before[2], before[3])
		funcs[candidate](m, line.instruction[1], line.instruction[2], line.instruction[3])
		expected := line.after
		actual := m.registers
		for i := 0; i < 4; i++ {
			if expected[i] != actual[i] {
				return false
			}
		}

	}
	return true
}
