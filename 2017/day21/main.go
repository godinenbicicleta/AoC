package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strings"
)

// Pos represents a pos
type Pos struct {
	x int
	y int
}

func show(s map[Pos]byte) string {
	size := int(math.Sqrt(float64(len(s))))
	buff := make([]byte, 0, size*size+size)
	for y := 0; y < size; y++ {
		for x := 0; x < size; x++ {
			pos := Pos{x, y}
			buff = append(buff, s[pos])
		}
		buff = append(buff, '\n')
	}
	return string(buff)
}

func partition(s map[Pos]byte) []map[Pos]byte {
	size := int(math.Sqrt(float64(len(s))))
	if size < 4 {
		return []map[Pos]byte{s}
	}
	var res []map[Pos]byte
	if size%2 == 0 {
		for j := 0; j < size/2; j++ {
			for i := 0; i < size/2; i++ {
				nS := make(map[Pos]byte, size)
				nS[Pos{0, 0}] = s[Pos{2*i + 0, 2*j + 0}]
				nS[Pos{0, 1}] = s[Pos{2*i + 0, 2*j + 1}]
				nS[Pos{1, 0}] = s[Pos{2*i + 1, 2*j + 0}]
				nS[Pos{1, 1}] = s[Pos{2*i + 1, 2*j + 1}]
				res = append(res, nS)
			}
		}
		return res
	}
	for j := 0; j < size/3; j++ {
		for i := 0; i < size/3; i++ {
			nS := make(map[Pos]byte, size)
			nS[Pos{0, 0}] = s[Pos{3*i + 0, 3*j + 0}]
			nS[Pos{0, 1}] = s[Pos{3*i + 0, 3*j + 1}]
			nS[Pos{0, 2}] = s[Pos{3*i + 0, 3*j + 2}]

			nS[Pos{1, 0}] = s[Pos{3*i + 1, 3*j + 0}]
			nS[Pos{1, 1}] = s[Pos{3*i + 1, 3*j + 1}]
			nS[Pos{1, 2}] = s[Pos{3*i + 1, 3*j + 2}]

			nS[Pos{2, 0}] = s[Pos{3*i + 2, 3*j + 0}]
			nS[Pos{2, 1}] = s[Pos{3*i + 2, 3*j + 1}]
			nS[Pos{2, 2}] = s[Pos{3*i + 2, 3*j + 2}]
			res = append(res, nS)
		}
	}
	return res
}

func merge(states []map[Pos]byte) map[Pos]byte {
	if len(states) == 1 {
		return states[0]
	}
	size := int(math.Sqrt(float64(len(states))))
	res := map[Pos]byte{}
	stateSize := int(math.Sqrt(float64(len(states[0]))))
	//	fmt.Println("MERGING SIZE", len(states), stateSize)
	//	for _, state := range states {
	//		fmt.Println(show(state))
	//	}
	for row := 0; row < size; row++ {
		for col := 0; col < size; col++ {
			s := states[row*size+col]
			for j := 0; j < stateSize; j++ {
				for i := 0; i < stateSize; i++ {
					//					fmt.Println("Setting", []int{i*stateSize + col, j*stateSize + row}, "to", "s[", row*size+col, "]", []int{i, j})
					res[Pos{i + col*stateSize, j + row*stateSize}] = s[Pos{i, j}]
				}
			}
		}
	}
	//	if stateSize%2 == 0 {
	//		for row := 0; row < size; row++ {
	//			for col := 0; col < size; col++ {
	//				s := states[row*size+col]
	//				res[Pos{0 + 2*col, 0 + 2*row}] = s[Pos{0, 0}]
	//				res[Pos{1 + 2*col, 0 + 2*row}] = s[Pos{1, 0}]
	//				res[Pos{0 + 2*col, 1 + 2*row}] = s[Pos{0, 1}]
	//				res[Pos{1 + 2*col, 1 + 2*row}] = s[Pos{1, 1}]
	//			}
	//		}
	//		return res
	//	}
	//	for row := 0; row < size; row++ {
	//		for col := 0; col < size; col++ {
	//			s := states[row*size+col]
	//			res[Pos{0 + 3*col, 0 + 3*row}] = s[Pos{0, 0}]
	//			res[Pos{1 + 3*col, 0 + 3*row}] = s[Pos{1, 0}]
	//			res[Pos{2 + 3*col, 0 + 3*row}] = s[Pos{2, 0}]
	//
	//			res[Pos{0 + 3*col, 1 + 3*row}] = s[Pos{0, 1}]
	//			res[Pos{1 + 3*col, 1 + 3*row}] = s[Pos{1, 1}]
	//			res[Pos{2 + 3*col, 1 + 3*row}] = s[Pos{2, 1}]
	//
	//			res[Pos{0 + 3*col, 2 + 3*row}] = s[Pos{0, 2}]
	//			res[Pos{1 + 3*col, 2 + 3*row}] = s[Pos{1, 2}]
	//			res[Pos{2 + 3*col, 2 + 3*row}] = s[Pos{2, 2}]
	//
	//		}
	//	}
	return res
}

func toPattern(s map[Pos]byte) string {
	size := int(math.Sqrt(float64(len(s))))
	res := []string{}
	//fmt.Println("SIZE", size)
	//fmt.Println(s)
	for y := 0; y < size; y++ {
		buff := make([]byte, 0, size)
		for x := 0; x < size; x++ {
			pos := Pos{x, y}
			buff = append(buff, s[pos])
		}
		res = append(res, string(buff))
	}
	return strings.Join(res, "/")
}

func fromPattern(s string) map[Pos]byte {
	s = strings.ReplaceAll(s, "/", "")
	res := map[Pos]byte{}
	cols := 4
	//fmt.Println("SSSS", s)
	if len(s) == 9 {
		cols = 3
		//	fmt.Println("COLS", 4)
	}
	for i, v := range s {
		res[Pos{i % cols, i / cols}] = byte(v)
	}
	return res
}

type transform func(p map[Pos]byte) map[Pos]byte

func combs(arr []transform) [][]transform {

	if len(arr) == 0 {
		return [][]transform{{}}
	}
	res := [][]transform{}
	for _, elem := range combs(arr[1:]) {
		res = append(res, elem)
		n := make([]transform, len(elem), len(elem))
		copy(n, elem)
		n = append(n, arr[0])
		res = append(res, n)
	}
	return res

}

func update(s map[Pos]byte, rules map[string]string) map[Pos]byte {
	//fmt.Println("UPDATE")
	//fmt.Println(show(s))
	//fmt.Println("PARTS")
	parts := partition(s)
	//fmt.Println("RULES")
	res := []map[Pos]byte{}
Loop:
	for _, p := range parts {
		for _, fs := range transforms {
			c := p
			//		fmt.Println("TO TRANSFORM")
			//		fmt.Println(c)
			for _, f := range fs {
				c = f(c)
			}
			//		fmt.Println("TRANSFORMED")
			//		fmt.Println(c)
			//		fmt.Println("BEFORE PATTERN")
			//		fmt.Println(show(c))
			pattern := toPattern(c)
			//		fmt.Println("TRY PATTERN", pattern)
			if v, ok := rules[pattern]; ok {
				//			fmt.Println("RULE MATCHED", v)
				v := fromPattern(v)
				//			fmt.Println(show(v))
				//			fmt.Println("APPEND")
				res = append(res, v)
				continue Loop
			}
		}
		//	fmt.Println(show(p))
		log.Fatal("No rule found")
	}
	merged := merge(res)
	return merged
}

func flipv(s map[Pos]byte) map[Pos]byte {
	nS := make(map[Pos]byte, len(s))
	if len(s) == 4 {
		nS[Pos{0, 0}] = s[Pos{1, 0}]
		nS[Pos{1, 0}] = s[Pos{0, 0}]
		nS[Pos{0, 1}] = s[Pos{1, 1}]
		nS[Pos{1, 1}] = s[Pos{0, 1}]
	} else {
		nS[Pos{0, 0}] = s[Pos{2, 0}]
		nS[Pos{0, 1}] = s[Pos{2, 1}]
		nS[Pos{0, 2}] = s[Pos{2, 2}]
		nS[Pos{2, 0}] = s[Pos{0, 0}]
		nS[Pos{2, 1}] = s[Pos{0, 1}]
		nS[Pos{2, 2}] = s[Pos{0, 2}]
		nS[Pos{1, 0}] = s[Pos{1, 0}]
		nS[Pos{1, 1}] = s[Pos{1, 1}]
		nS[Pos{1, 2}] = s[Pos{1, 2}]
	}
	return nS
}

func fliph(s map[Pos]byte) map[Pos]byte {
	nS := make(map[Pos]byte, len(s))
	if len(s) == 4 {
		nS[Pos{0, 0}] = s[Pos{0, 1}]
		nS[Pos{1, 0}] = s[Pos{1, 1}]
		nS[Pos{0, 1}] = s[Pos{0, 0}]
		nS[Pos{1, 1}] = s[Pos{1, 0}]
	} else {
		nS[Pos{0, 0}] = s[Pos{0, 2}]
		nS[Pos{1, 0}] = s[Pos{1, 2}]
		nS[Pos{2, 0}] = s[Pos{2, 2}]
		nS[Pos{0, 2}] = s[Pos{0, 0}]
		nS[Pos{1, 2}] = s[Pos{1, 0}]
		nS[Pos{2, 2}] = s[Pos{2, 0}]
		nS[Pos{0, 1}] = s[Pos{0, 1}]
		nS[Pos{1, 1}] = s[Pos{1, 1}]
		nS[Pos{2, 1}] = s[Pos{2, 1}]

	}
	return nS
}
func rotate(s map[Pos]byte) map[Pos]byte {
	nS := make(map[Pos]byte, len(s))
	if len(s) == 4 {
		nS[Pos{0, 0}] = s[Pos{0, 1}]
		nS[Pos{0, 1}] = s[Pos{1, 1}]
		nS[Pos{1, 0}] = s[Pos{0, 0}]
		nS[Pos{1, 1}] = s[Pos{1, 0}]
	} else {
		nS[Pos{0, 0}] = s[Pos{0, 2}]
		nS[Pos{0, 1}] = s[Pos{1, 2}]
		nS[Pos{0, 2}] = s[Pos{2, 2}]
		nS[Pos{1, 0}] = s[Pos{0, 1}]
		nS[Pos{1, 1}] = s[Pos{1, 1}]
		nS[Pos{1, 2}] = s[Pos{2, 1}]
		nS[Pos{2, 0}] = s[Pos{0, 0}]
		nS[Pos{2, 1}] = s[Pos{1, 0}]
		nS[Pos{2, 2}] = s[Pos{2, 0}]
	}
	return nS
}

var transforms [][]transform

func main() {
	transforms = combs([]transform{rotate, rotate, rotate, flipv, fliph, flipv, fliph})
	rounds := 18
	state := map[Pos]byte{
		{0, 0}: '.',
		{1, 0}: '#',
		{2, 0}: '.',
		{0, 1}: '.',
		{1, 1}: '.',
		{2, 1}: '#',
		{0, 2}: '#',
		{1, 2}: '#',
		{2, 2}: '#',
	}
	scanner := bufio.NewScanner(os.Stdin)
	rules := map[string]string{}
	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), " => ")
		rules[parts[0]] = parts[1]
	}
	for i := 0; i < rounds; i++ {
		state = update(state, rules)
		fmt.Println("iterations", i+1, "ON", strings.Count(show(state), "#"))
	}
}
