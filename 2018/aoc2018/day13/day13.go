package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

type Track = map[Position]byte

type Position struct {
	x int
	y int
}

func matchingStraightLine(d Direction) byte {
	switch d {
	case UP:
		return '|'
	case DOWN:
		return '|'
	case LEFT:
		return '-'
	case RIGHT:
		return '-'
	default:
		panic("invalid direction" + string(d))
	}

}

type nextTurn = int

const (
	left = iota
	straight
	right
)

type Direction = byte

const (
	UP    = '^'
	DOWN  = 'v'
	LEFT  = '<'
	RIGHT = '>'
)

type Car struct {
	direction Direction
	Position
	next nextTurn
}

func move(c Car, track Track) Car {
	var newPos Position
	switch c.direction {
	case UP:
		newPos = Position{c.Position.x, c.Position.y - 1}
	case DOWN:
		newPos = Position{c.Position.x, c.Position.y + 1}
	case LEFT:
		newPos = Position{c.Position.x - 1, c.Position.y}
	case RIGHT:
		newPos = Position{c.Position.x + 1, c.Position.y}
	default:
		panic("invalid direction" + c.String())
	}

	switch valueAtPos := track[newPos]; valueAtPos {
	case '|', '-':
		return Car{Position: newPos, next: c.next, direction: c.direction}
	case '/':
		switch c.direction {
		case UP:
			return Car{Position: newPos, next: c.next, direction: RIGHT}

		case LEFT:
			return Car{Position: newPos, next: c.next, direction: DOWN}
		case RIGHT:
			return Car{Position: newPos, next: c.next, direction: UP}
		case DOWN:
			return Car{Position: newPos, next: c.next, direction: LEFT}
		default:
			panic("invalid direction")
		}
	case '\\':
		switch c.direction {
		case UP:
			return Car{Position: newPos, next: c.next, direction: LEFT}
		case LEFT:
			return Car{Position: newPos, next: c.next, direction: UP}
		case RIGHT:
			return Car{Position: newPos, next: c.next, direction: DOWN}
		case DOWN:
			return Car{Position: newPos, next: c.next, direction: RIGHT}
		default:
			panic("invalid direction")
		}

	case '+':
		switch c.next {
		case left:
			switch c.direction {
			case UP:
				return Car{Position: newPos, next: straight, direction: LEFT}
			case LEFT:
				return Car{Position: newPos, next: straight, direction: DOWN}
			case RIGHT:
				return Car{Position: newPos, next: straight, direction: UP}
			case DOWN:
				return Car{Position: newPos, next: straight, direction: RIGHT}
			default:
				panic("invalid direction")
			}

		case straight:
			return Car{Position: newPos, next: right, direction: c.direction}
		case right:
			switch c.direction {
			case UP:
				return Car{Position: newPos, next: left, direction: RIGHT}
			case LEFT:
				return Car{Position: newPos, next: left, direction: UP}
			case RIGHT:
				return Car{Position: newPos, next: left, direction: DOWN}
			case DOWN:
				return Car{Position: newPos, next: left, direction: LEFT}
			default:
				panic("invalid direction")
			}
		default:
			panic("unknown next")
		}

	default:
		panic("unhandled valueAtPos" + strconv.Itoa(int(valueAtPos)))
	}
}

func isCar(b byte) bool {
	switch b {
	case 'v', '>', '<', '^':
		return true
	default:
		return false
	}
}

type Cars = map[Position]Car

func (c Car) String() string {
	return fmt.Sprintf("Car{x: %d, y: %d, dir: %q, next: %d}", c.x, c.y, c.direction, c.next)
}

func SortedCars(cars Cars) []Car {
	var keys []Position
	for k := range cars {
		keys = append(keys, k)
	}
	sort.Slice(keys,
		func(i, j int) bool {
			if keys[i].y < keys[j].y {
				return true
			}
			if keys[i].y > keys[j].y {
				return false
			}
			return keys[i].x <= keys[j].x
		},
	)
	var res []Car
	for _, key := range keys {
		res = append(res, cars[key])
	}
	return res
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	track := make(Track)
	cars := make(Cars)
	y := 0
	for scanner.Scan() {
		txt := scanner.Text()
		for x := 0; x < len(txt); x++ {
			pos := Position{x: x, y: y}
			var value byte
			if isCar(txt[x]) {
				value = matchingStraightLine(txt[x])
				cars[pos] = Car{direction: Direction(txt[x]), next: left, Position: pos}
			} else {
				value = txt[x]
			}
			track[pos] = value
		}
		y++
	}

	for len(cars) > 1 {
		newCars := make(Cars)
		moved := make(map[Car]bool)
		for _, car := range SortedCars(cars) {
			if moved[car] {
				continue
			}
			newCar := move(car, track)
			moved[car] = true
			if v, ok := cars[newCar.Position]; ok && !moved[v] {
				fmt.Printf("crash at %#v\n", newCar.Position)
				moved[v] = true
				continue
			}
			if _, ok := newCars[newCar.Position]; ok {
				fmt.Printf("crash at %#v\n", newCar.Position)
				delete(newCars, newCar.Position)
				continue
			}
			newCars[newCar.Position] = newCar
		}
		cars = newCars
	}
	fmt.Println(cars)
}
