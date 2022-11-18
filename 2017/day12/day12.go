package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

// Graph represents a graph
type Graph map[int][]int

func canReach(g Graph, start, goal int) bool {
	seen := map[int]bool{}
	toVisit := []int{start}
	for len(toVisit) > 0 {
		current := toVisit[len(toVisit)-1]
		toVisit = toVisit[:len(toVisit)-1]
		if current == goal {
			return true
		}
		seen[current] = true
		for _, n := range g[current] {
			if seen[n] {
				continue
			}
			toVisit = append(toVisit, n)
		}
	}
	return false
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var g Graph = make(map[int][]int)
	for scanner.Scan() {
		text := scanner.Text()
		parts := strings.Split(text, " <-> ")
		node, err := strconv.Atoi(parts[0])
		if err != nil {
			log.Fatal("Error parsing", parts[0])
		}
		g[node] = []int{}
		for _, s := range strings.Split(parts[1], ", ") {
			v, err := strconv.Atoi(s)
			if err != nil {
				log.Fatal("Error parsing", s)

			}
			g[node] = append(g[node], v)
		}
	}
	num := 0
	for node := range g {
		if canReach(g, node, 0) {
			num++
		}
	}
	inGroup := make(map[int]int)
	for nodeTarget := range g {
		if _, ok := inGroup[nodeTarget]; ok {
			continue
		}
		for node := range g {

			if canReach(g, node, nodeTarget) {
				inGroup[node] = nodeTarget
			}
		}
	}
	seen := map[int]bool{}
	groups := 0
	for _, v := range inGroup {
		if !seen[v] {
			groups++
		}
		seen[v] = true
	}
	if len(g) < 100 {
		fmt.Println(g)
	}
	fmt.Println(num)
	fmt.Println(groups)
}
