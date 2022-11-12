package main

import "fmt"

const size = 16

var arr = [...]int{4, 10, 4, 1, 8, 4, 9, 14, 5, 1, 14, 15, 0, 15, 3, 5}
var seen = map[[size]int]int{}

func run(cycles int) (int, int) {
	if seen[arr] > 0 {
		return cycles, cycles - seen[arr]
	}
	seen[arr] = cycles
	index := 0
	val := arr[0]
	for i := range arr {
		if arr[i] > val {
			index = i
			val = arr[i]
		}
	}
	arr[index] = 0
	for i := (index + 1) % size; val > 0; i = (i + 1) % size {
		arr[i]++
		val--
	}
	return run(cycles + 1)

}

func main() {
	fmt.Println(run(0))
}
