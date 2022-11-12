package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
)

func valid1(ws []string) bool {
	seen := map[string]bool{}
	for _, w := range ws {
		if seen[w] {
			return false
		}
		seen[w] = true
	}
	return true
}

func valid(line string) (int, int) {
	ws := strings.Split(line, " ")
	if valid2(ws) {
		return 1, 1
	}
	if valid1(ws) {
		return 1, 0
	}
	return 0, 0

}

func valid2(ws []string) bool {
	sorted := []string{}
	for _, w := range ws {
		list := []byte(w)
		sort.Slice(list, func(i, j int) bool { return list[i] < list[j] })
		sorted = append(sorted, string(list))
	}
	return valid1(sorted)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	valids1 := 0
	valids2 := 0
	for scanner.Scan() {
		line := scanner.Text()
		delta1, delta2 := valid(line)
		valids1 += delta1
		valids2 += delta2
	}
	fmt.Println(valids1, valids2)
}
