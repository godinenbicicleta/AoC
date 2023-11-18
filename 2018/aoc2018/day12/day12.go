package main

import (
	"fmt"
	"math"
	"strings"
)

const INITIAL_STATE string = "#.####...##..#....#####.##.......##.#..###.#####.###.##.###.###.#...#...##.#.##.#...#..#.##..##.#.##"

const RULES string = `.##.. => .
..##. => #
.#..# => #
.#.#. => .
..#.. => #
###.. => #
##..# => .
##... => #
#.### => #
.##.# => #
#.... => .
###.# => .
..... => .
.#... => #
....# => .
#.#.. => .
...#. => #
#...# => .
##.#. => .
.#.## => #
..#.# => #
#.#.# => .
.#### => .
##### => .
..### => .
...## => .
#..## => .
#.##. => .
#..#. => #
.###. => #
##.## => #
####. => .`

type Rules = map[string]byte

func parse() Rules {
	rules := strings.Split(RULES, "\n")
	m := make(Rules)
	for _, rule := range rules {
		from := rule[:5]
		to := rule[9]
		m[from] = to
	}
	return m
}

func Convert(current int, rules Rules, state map[int]byte) byte {
	var s strings.Builder
	for i := current - 2; i < current+3; i++ {
		v, ok := state[i]
		if ok {
			s.WriteByte(v)
		} else {
			s.WriteByte('.')
		}
	}
	return rules[s.String()]

}

func apply(rules Rules, state map[int]byte) map[int]byte {
	min_index := minIndex(state)
	max_index := maxIndex(state)
	newState := make(map[int]byte)
	for i := min_index - 4; i <= max_index+4; i++ {
		newState[i] = Convert(i, rules, state)
	}

	return newState
}

func Sum(state map[int]byte) int {
	total := 0
	for i, v := range state {
		if v == '#' {
			total += i
		}
	}
	return total

}

func minIndex(state map[int]byte) int {
	res := math.MaxInt
	for k := range state {
		if k < res {
			res = k
		}
	}
	return res
}
func maxIndex(state map[int]byte) int {
	res := math.MinInt
	for k := range state {
		if k > res {
			res = k
		}
	}
	return res
}

func parseState() map[int]byte {
	state := make(map[int]byte)
	for i := 0; i < len(INITIAL_STATE); i++ {
		state[i] = INITIAL_STATE[i]
	}
	return state
}

func main() {
	rules := parse()
	fmt.Println(rules)

	state := parseState()

	p1000 := -1
	p2000 := -1
	for i := 1; i <= 2000; i++ {
		state = apply(rules, state)
		if i == 20 {
			fmt.Println(i, Sum(state))
			continue
		}
		if i == 1000 {
			p1000 = Sum(state)
			continue
		}
		if i == 2000 {
			p2000 = Sum(state)
		}
	}

	r := (p2000-p1000)/(2000-1000)*(50000000000-1000) + p1000
	fmt.Println(r)
}
