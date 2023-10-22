package day07

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strings"
)

func Contains(list []string, elem string) bool {
	for _, e := range list {
		if e == elem {
			return true
		}
	}
	return false
}

type NodesType = map[string][]string
type TotalNodesType = map[string]bool

func parseNodes(fname string) (NodesType, TotalNodesType) {
	f, err := os.Open(fname)

	if err != nil {
		panic(err)
	}
	defer f.Close()

	nodes := make(map[string][]string) // nodes[after] = [before1, before2, ...]
	totalNodes := make(map[string]bool)

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		text := scanner.Text()
		var before string
		var after string
		_, err := fmt.Sscanf(text, "Step %s must be finished before step %s can begin.", &before, &after)

		if err != nil {
			panic(err)
		}
		totalNodes[before] = true
		totalNodes[after] = true
		nodes[after] = append(nodes[after], before)
	}
	return nodes, totalNodes

}

func Solve(fname string) string {
	// Step D must be finished before step P can begin.
	nodes, totalNodes := parseNodes(fname)
	sorted := []string{}

	candidates := []string{}
	for len(sorted) != len(totalNodes) {
		for after := range nodes {
			newBefores := []string{}
			for _, before := range nodes[after] {
				if !Contains(sorted, before) {
					newBefores = append(newBefores, before)
				}
			}
			nodes[after] = newBefores
		}

		for node := range totalNodes {
			befores := nodes[node]
			if len(befores) == 0 {
				if !Contains(sorted, node) && !Contains(candidates, node) {
					candidates = append(candidates, node)
				}
			}
		}

		slices.Sort(candidates)
		sorted = append(sorted, candidates[0])
		candidates = candidates[1:]

	}
	return strings.Join(sorted, "")
}

func Solve2(fname string, workers int, delta int) int {
	// Step D must be finished before step P can begin.
	nodes, totalNodes := parseNodes(fname)
	sorted := []string{}
	working := make(map[string]int)
	candidates := []string{}
	elapsed_time := 0
	for {
		//	log.Println("working after sort", working)
		newWorking := make(map[string]int)
		for work, t := range working {
			if t == 1 {
				sorted = append(sorted, work)
				continue
			}
			newWorking[work] = t - 1
		}
		working = newWorking
		//log.Println("newWorking", newWorking)
		for after := range nodes {
			newBefores := []string{}
			for _, before := range nodes[after] {
				if !Contains(sorted, before) {
					newBefores = append(newBefores, before)
				}
			}
			nodes[after] = newBefores
		}

		for node := range totalNodes {
			befores := nodes[node]
			if len(befores) == 0 {
				if !Contains(sorted, node) && !Contains(candidates, node) {
					if _, ok := working[node]; ok {
						continue
					}
					candidates = append(candidates, node)
				}
			}
		}

		slices.Sort(candidates)
		//		log.Println("sorted candidates:", candidates)
		newCandidates := []string{}
		for _, c := range candidates {
			if _, ok := working[c]; ok {
				continue
			}
			if len(working) < workers {
				working[c] = delta + int([]byte(c)[0]) - 64
				continue
			}
			newCandidates = append(newCandidates, c)
		}
		candidates = newCandidates
		if len(sorted) == len(totalNodes) {
			break
		}
		elapsed_time += 1
	}
	return elapsed_time
}
