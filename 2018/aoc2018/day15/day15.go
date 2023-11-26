package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
)

const (
	GoblinType = 'G'
	ElfType    = 'E'
)

type Unit struct {
	id       int
	unitType byte
	hp       int
	Point
}

func result(s State, rounds int) int {
	res := 0
	for _, elem := range s.Units() {
		res += elem.hp
	}
	return res * rounds
}

func (u Unit) String() string {
	if u.unitType == GoblinType {
		return fmt.Sprintf("G[%d](x=%d,y=%d,hp=%d)", u.id, u.x, u.y, u.hp)
	}
	return fmt.Sprintf("E[%d](x=%d,y=%d,hp=%d)", u.id, u.x, u.y, u.hp)
}

var grid [][]byte

type State struct {
	elfs    []Unit
	goblins []Unit
}

func (s State) delete(u Unit) State {
	var newGoblins []Unit
	var newElfs []Unit
	if u.unitType == GoblinType {
		newElfs = make([]Unit, len(s.elfs))
		copy(newElfs, s.elfs)
		for _, elem := range s.goblins {
			if elem.id != u.id {
				newGoblins = append(newGoblins, elem)
			}
		}
	} else {
		newGoblins = make([]Unit, len(s.goblins))
		copy(newGoblins, s.goblins)
		for _, elem := range s.elfs {
			if elem.id != u.id {
				newElfs = append(newElfs, elem)
			}
		}
	}
	return State{elfs: newElfs, goblins: newGoblins}
}
func (s State) replace(old Unit, u Unit) State {
	var newGoblins []Unit
	var newElfs []Unit
	if u.unitType == GoblinType {
		newElfs = make([]Unit, len(s.elfs))
		copy(newElfs, s.elfs)
		for _, elem := range s.goblins {
			if elem.id != u.id {
				newGoblins = append(newGoblins, elem)
			} else {
				newGoblins = append(newGoblins, u)
			}
		}
	} else {
		newGoblins = make([]Unit, len(s.goblins))
		copy(newGoblins, s.goblins)
		for _, elem := range s.elfs {
			if elem.id != u.id {
				newElfs = append(newElfs, elem)
			} else {
				newElfs = append(newElfs, u)
			}
		}
	}
	return State{elfs: newElfs, goblins: newGoblins}
}

func (u Unit) targets(s State) []Unit {
	if u.unitType == GoblinType {
		return s.elfs
	}
	return s.goblins
}

type Point struct {
	x int
	y int
}

func neighbors(p Point) []Point {
	var ns []Point
	for _, ps := range []Point{
		{p.x, p.y - 1},
		{p.x - 1, p.y},
		{p.x + 1, p.y},
		{p.x, p.y + 1},
	} {
		if ps.x < len(grid[0]) && p.y < len(grid) && p.y >= 0 && p.x >= 0 {
			ns = append(ns, ps)
		}
	}
	return ns
}

func (u Unit) openSquares(s State) []Point {
	taken := make(map[Point]bool)
	for _, elem := range s.Units() {
		taken[elem.Point] = true
	}
	squares := make(map[Point]bool)
	for _, target := range u.targets(s) {
		for _, elem := range neighbors(target.Point) {
			if grid[elem.y][elem.x] == '#' {
				continue
			}
			if taken[elem] {
				continue
			}

			squares[elem] = true

		}
	}
	var sq []Point
	for k := range squares {
		sq = append(sq, k)

	}
	return sq
}

func (u Unit) inRange(s State) bool {
	for _, p := range neighbors(u.Point) {
		for _, elem := range u.targets(s) {
			if p == elem.Point {
				return true
			}
		}
	}
	return false

}

func (u Unit) chooseTargets(s State) []Unit {
	var candidates []Unit

	for _, p := range neighbors(u.Point) {
		for _, elem := range u.targets(s) {
			if p == elem.Point {
				candidates = append(candidates, elem)
			}
		}
	}
	sort.Slice(candidates, func(i, j int) bool {
		if candidates[i].hp < candidates[j].hp {
			return true
		}
		if candidates[i].hp > candidates[j].hp {
			return false
		}
		left := candidates[i].Point
		right := candidates[j].Point
		if left.y < right.y {
			return true
		}
		if left.y > right.y {
			return false
		}
		return left.x < right.x
	})
	return candidates
}

func (g State) Units() map[int]Unit {
	units := make(map[int]Unit)
	for _, elem := range g.elfs {
		units[elem.id] = elem

	}
	for _, elem := range g.goblins {
		units[elem.id] = elem
	}
	return units
}

func (g State) SortedUnits() []Unit {
	units := g.Units()
	var arr []Unit
	for _, u := range units {
		arr = append(arr, u)
	}
	sort.Slice(arr, func(i int, j int) bool {
		left := arr[i]
		right := arr[j]
		if left.y < right.y {
			return true
		}
		if left.y > right.y {
			return false
		}
		return left.x < right.x
	})
	return arr
}

func (g State) String() string {
	var arr [][]byte
	for y := 0; y < len(grid); y++ {
		row := grid[y]
		newRow := make([]byte, len(row))
		copy(newRow, row)
		arr = append(arr, newRow)
	}
	var s strings.Builder
	s.WriteByte('\n')
	for _, elem := range g.SortedUnits() {
		arr[elem.y][elem.x] = elem.unitType
		s.WriteString(elem.String())
		s.WriteByte('\n')
	}
	s.WriteByte('\n')
	for _, row := range arr {
		for _, elem := range row {
			s.WriteByte(elem)
		}
		s.WriteByte('\n')
	}

	return s.String()
}

type Node struct {
	Point
	steps int
	path  Path
}

type Path []Point

func (u Unit) stepsTo(goal Point, s State) (int, []Path) {
	currentPos := u.Point
	taken := make(map[Point]bool)
	for _, unit := range s.Units() {
		taken[unit.Point] = true
	}
	queue := []Node{{Point: currentPos, steps: 0, path: []Point{}}}
	minSteps := -1
	var shortestPaths []Path

	for len(queue) != 0 {
		current := queue[0]
		queue = queue[1:]
		if minSteps != -1 && current.steps > minSteps {
			continue
		}
		if current.Point == goal {
			if minSteps == -1 {
				minSteps = current.steps
			}
			if current.steps > minSteps {
				break
			}
			shortestPaths = append(shortestPaths, current.path)
			continue
		}
		for _, n := range neighbors(current.Point) {
			if grid[n.y][n.x] == '#' {
				continue
			}
			if taken[n] {
				continue
			}
			taken[n] = true

			newPath := make(Path, len(current.path))
			copy(newPath, current.path)
			newPath = append(newPath, n)

			queue = append(queue, Node{Point: n, steps: current.steps + 1, path: newPath})
		}

	}
	return minSteps, shortestPaths
}

func chooseStep(paths []Path) Point {
	var candidates []Point
	for _, p := range paths {
		candidates = append(candidates, p[0])
	}
	sort.Slice(candidates, func(i int, j int) bool {
		left := candidates[i]
		right := candidates[j]
		if left.y < right.y {
			return true
		}
		if left.y > right.y {
			return false
		}
		return left.x < right.x
	})

	return candidates[0]

}

type Target struct {
	Point
	steps int
	paths []Path
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var goblins []Unit
	var elfs []Unit
	y := 0
	id := 0
	for scanner.Scan() {
		txt := scanner.Text()
		var row []byte
		for i := 0; i < len(txt); i++ {
			if txt[i] == GoblinType {
				goblin := Unit{unitType: GoblinType, hp: 200, Point: Point{x: i, y: y}, id: id}
				id++
				goblins = append(goblins, goblin)
				row = append(row, '.')
			} else if txt[i] == ElfType {
				elf := Unit{unitType: ElfType, hp: 200, Point: Point{x: i, y: y}, id: id}
				id++

				elfs = append(elfs, elf)
				row = append(row, '.')
			} else {
				row = append(row, txt[i])
			}
		}
		grid = append(grid, row)
		y++
	}

	s := State{elfs: elfs, goblins: goblins}

	attack := 3
	stopOnDeath := false
	run(attack, s, stopOnDeath)

	for attack := 4; ; attack++ {
		if run(attack, s, true) {
			break
		}
	}

}

func run(elfAttack int, s State, stopOnDeath bool) bool {
	rounds := -1
	var state State
	attack := make(map[byte]int)
	attack[ElfType] = elfAttack
	attack[GoblinType] = 3

loop:
	for {
		// each unit takes a turn
		// for unit in units:
		// try to move into range of a unit if it isn't already
		gs := make([]Unit, len(s.goblins))
		es := make([]Unit, len(s.elfs))
		if len(s.goblins) == 0 || len(s.elfs) == 0 {
			break
		}
		rounds++
		copy(gs, s.goblins)
		copy(es, s.elfs)
		state = State{elfs: es, goblins: gs}
		for _, oldUnit := range s.SortedUnits() {
			units := state.Units()
			u, ok := units[oldUnit.id]
			if !ok {
				continue
			}
			if len(u.targets(state)) == 0 {
				break loop
			}
			if !u.inRange(state) {
				// u moves
				openSquares := u.openSquares(state)
				if len(openSquares) == 0 {
					continue
				}

				var targets []Target
				for _, elem := range openSquares {
					steps, shortestPaths := u.stepsTo(elem, state)
					if steps == -1 {
						continue
					}
					targets = append(targets, Target{Point: elem, paths: shortestPaths, steps: steps})
				}

				sort.Slice(targets, func(i, j int) bool {
					left := targets[i]
					right := targets[j]
					if left.steps < right.steps {
						return true
					}
					if left.steps > right.steps {
						return false
					}
					if left.y < right.y {
						return true
					}
					if left.y > right.y {
						return false
					}
					return left.x < right.x
				})
				if len(targets) != 0 {

					target := targets[0]

					nextStep := chooseStep(target.paths)
					u = Unit{Point: nextStep, hp: u.hp, unitType: u.unitType, id: u.id}
					newGoblins := make([]Unit, len(state.goblins))
					newElfs := make([]Unit, len(state.elfs))
					for i := 0; i < len(state.goblins); i++ {
						if state.goblins[i].id == oldUnit.id {
							newGoblins[i] = u
						} else {
							newGoblins[i] = state.goblins[i]
						}
					}
					for i := 0; i < len(state.elfs); i++ {
						if state.elfs[i].id == oldUnit.id {
							newElfs[i] = u
						} else {
							newElfs[i] = state.elfs[i]
						}
					}

					state = State{elfs: newElfs, goblins: newGoblins}
				}
			}

			if !u.inRange(state) {
				continue
			}

			// attack because in range
			targets := u.chooseTargets(state)
			target := targets[0]
			if target.hp <= attack[u.unitType] {
				state = state.delete(target)
				if target.unitType == ElfType && stopOnDeath {
					return false
				}
			} else {
				state = state.replace(target, Unit{unitType: target.unitType, hp: target.hp - attack[u.unitType], id: target.id, Point: target.Point})
			}

		}
		s = state

	}

	fmt.Println(result(state, rounds))
	return true

}
