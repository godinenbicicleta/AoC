package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

// Node represents a Node
type Node struct {
	name string
	w    int
}

// Graph represents a graph
type Graph map[Node][]Node

func parseNode(s string) Node {
	re := regexp.MustCompile(`(\w+)\s+\((\d+)\)`)
	ms := re.FindStringSubmatch(s)
	w, err := strconv.Atoi(ms[2])
	if err != nil {
		log.Fatal("Error parsing s", s)
	}

	return Node{name: ms[1], w: w}
}

func parse(lines []string) (Graph, map[string]Node) {

	graph := make(map[Node][]Node)
	nodes := make(map[string]Node)
	for _, line := range lines {
		node := parseNode(line)
		graph[node] = []Node{}
		nodes[node.name] = node
	}
	for _, line := range lines {
		node := parseNode(line)
		parts := strings.Split(line, " -> ")
		if len(parts) < 2 {
			continue
		}
		for _, name := range strings.Split(parts[1], ", ") {
			graph[node] = append(graph[node], nodes[name])

		}

	}
	return graph, nodes

}
func process(g Graph, n Node, cws []int) {
	fmt.Println("Unbalanced", g[n], cws)
}

func weight(g Graph, n Node) int {
	w := n.w
	cws := []int{}
	for _, s := range g[n] {
		sw := weight(g, s)
		cws = append(cws, sw)
		w += sw
	}
	if len(cws) > 1 {
		for _, cw := range cws[1:] {
			if cw != cws[0] {
				process(g, n, cws)
				break
			}
		}
	}

	return w
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	lines := []string{}
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	graph, _ := parse(lines)
	// part 1
Loop:
	for n := range graph {
		for m, successors := range graph {
			if m == n {
				continue
			}
			for _, s := range successors {
				if n == s {
					continue Loop
				}
			}
		}
		fmt.Println(n)
		weight(graph, n)
	}
}
