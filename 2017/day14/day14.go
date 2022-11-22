package main

import (
	"fmt"
	"strconv"
	"strings"
)

func reverse(arr []int) {
	for i := 0; i < len(arr)/2; i++ {
		j := len(arr) - 1 - i
		arr[i], arr[j] = arr[j], arr[i]
	}
}

func run(arr []int, lengths []int, index int, skip int) (int, int) {

	for _, le := range lengths {
		if le > len(arr) {
			continue
		}
		start := index
		s := make([]int, le, le)
		for j := 0; j < le; j++ {
			s[j] = arr[(start+j)%len(arr)]
		}
		reverse(s)
		for j := 0; j < le; j++ {
			arr[(start+j)%len(arr)] = s[j]
		}
		index = (index + le + skip) % len(arr)
		skip++
	}
	return index, skip
}
func reduce(arr []int) []int {
	res := []int{}
	for i := 0; i < len(arr); i += 16 {
		r := arr[i]
		for j := 1; j < 16; j++ {
			r = r ^ arr[j+i]
		}
		res = append(res, r)
	}
	return res
}

func toS(arr []int) string {
	s := []string{}
	for _, v := range arr {
		s = append(s, fmt.Sprintf("%d", v))
	}
	return strings.Join(s, ",")
}

var toNum = map[byte]int{'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

func toHash(input string) []int {
	arr := make([]int, 256, 256)
	for i := range arr {
		arr[i] = i
	}
	lengths := []int{}
	for _, v := range input {
		lengths = append(lengths, int(v))
	}
	lengths = append(lengths, 17, 31, 73, 47, 23)
	index := 0
	skip := 0
	for i := 0; i < 64; i++ {
		index, skip = run(arr, lengths, index, skip)
	}
	denseHash := reduce(arr)
	s := ""
	for _, v := range denseHash {
		s += fmt.Sprintf("%02x", v)
	}
	return toBinary(s)
}

func toBinary(s string) []int {
	s2 := []int{}
	for i := range s {
		for _, v := range fmt.Sprintf("%04b", toNum[s[i]]) {
			num, _ := strconv.Atoi(string(v))
			s2 = append(s2, num)
		}
	}
	return s2

}

// Pos represents a position
type Pos struct {
	x int
	y int
}

func neighbors(p Pos, g map[Pos]int) []Pos {
	ns := []Pos{}
	for _, n := range []Pos{{p.x + 1, p.y}, {p.x - 1, p.y}, {p.x, p.y - 1}, {p.x, p.y + 1}} {
		if g[n] == 1 {
			ns = append(ns, n)
		}
	}
	return ns

}

func canReach(start Pos, goal Pos, g map[Pos]int, groups map[Pos]Pos) bool {
	queue := []Pos{start}
	seen := map[Pos]bool{}
	for len(queue) > 0 {
		lastIndex := len(queue) - 1
		current := queue[lastIndex]
		seen[current] = true
		queue = queue[:lastIndex]
		if current == goal {
			return true
		}
		for _, n := range neighbors(current, g) {
			if _, ok := groups[n]; !ok {
				groups[n] = start
			}
			if seen[n] {
				continue
			}
			queue = append(queue, n)
		}
	}
	return false
}

func main() {
	grid := make(map[Pos]int)
	used := 0
	base := "amgozmfv"
	// low 7991
	for i := 0; i < 128; i++ {
		input := fmt.Sprintf("%s-%d", base, i)
		h := toHash(input)
		for j, v := range h {
			p := Pos{x: j, y: i}
			grid[p] = v
			used += v
		}
	}
	fmt.Println(used)
	groups := map[Pos]Pos{}
	for start, v1 := range grid {
		if _, ok := groups[start]; v1 == 0 || ok {
			continue
		}
		groups[start] = start
		for target, v2 := range grid {
			if _, ok := groups[target]; v2 == 0 || ok {
				continue
			}
			if canReach(start, target, grid, groups) {
				groups[target] = start
			}
		}
	}
	seen := map[Pos]bool{}
	numGroups := 0
	for _, v := range groups {
		if seen[v] {
			continue
		}
		numGroups++
		seen[v] = true
	}
	fmt.Println(numGroups)
}
