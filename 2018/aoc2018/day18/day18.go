package main

import (
	"bufio"
	"bytes"
	"fmt"
	"os"
)

func newGrid(g [][]byte) [][]byte {
	n := make([][]byte, len(g))
	for i, row := range g {
		nr := make([]byte, len(row))
		copy(nr, row)
		n[i] = nr
	}
	return n
}

type Adj struct {
	trees      int
	lumberyard int
	open       int
}

func get_ns(x int, y int, grid [][]byte) Adj {
	var trees, lumberyard, open int
	for _, p := range []struct {
		x int
		y int
	}{
		{x: x - 1, y: y},
		{x: x + 1, y: y},
		{x: x, y: y + 1},
		{x: x, y: y - 1},
		{x: x - 1, y: y - 1},
		{x: x - 1, y: y + 1},
		{x: x + 1, y: y - 1},
		{x: x + 1, y: y + 1},
	} {
		if p.x < 0 || p.y < 0 || p.x >= len(grid[0]) || p.y >= len(grid) {
			continue
		}
		switch grid[p.y][p.x] {
		case '.':
			open++
		case '|':
			trees++
		case '#':
			lumberyard++
		default:
			panic("err")
		}

	}
	return Adj{open: open, trees: trees, lumberyard: lumberyard}
}

func update(grid [][]byte) [][]byte {

	g := newGrid(grid)
	for y := 0; y < len(grid); y++ {
		for x := 0; x < len(grid[0]); x++ {
			old := grid[y][x]
			ns := get_ns(x, y, grid)
			switch old {
			case '.':
				if ns.trees >= 3 {
					g[y][x] = '|'
				}
			case '|':
				if ns.lumberyard >= 3 {
					g[y][x] = '#'
				}
			case '#':
				if !(ns.lumberyard >= 1 && ns.trees >= 1) {
					g[y][x] = '.'
				}
			default:
				panic("err")

			}
		}
	}
	return g
}

func state(g [][]byte) string {
	bts := bytes.Join(g, []byte{'\n'})
	return string(bts)
}

func PrintG(g [][]byte) {
	fmt.Println(state(g))
}

func getTotals(g [][]byte) Adj {
	wood := 0
	lumb := 0
	for _, row := range g {
		for _, v := range row {
			if v == '|' {
				wood++
			}
			if v == '#' {
				lumb++
			}
		}
	}
	return Adj{trees: wood, lumberyard: lumb}

}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var grid [][]byte
	states := make(map[string][]int)
	for scanner.Scan() {
		txt := scanner.Text()
		row := make([]byte, len(txt))
		for i := 0; i < len(txt); i++ {
			row[i] = txt[i]
		}
		grid = append(grid, row)
	}
	cycle := 0
	states[state(grid)] = []int{0}
	goal := 1000000000
	gridStates := make(map[string][][]byte)
outer:
	for i := 1; i <= goal; i++ {
		grid = update(grid)
		s := state(grid)
		states[s] = append(states[s], i)
		gridStates[s] = grid
		if len(states[s]) > 2 {
			cycle = states[s][2] - states[s][1]
			for e, vs := range states {
				if len(vs) < 2 {
					continue
				}
				if (goal-vs[len(vs)-1])%cycle == 0 {
					totals := getTotals(gridStates[e])
					fmt.Println(totals.trees * totals.lumberyard)
					break outer

				}
			}
		}

		if i == 10 {
			totals := getTotals(grid)
			fmt.Println(totals.trees * totals.lumberyard)
		}
	}

}
