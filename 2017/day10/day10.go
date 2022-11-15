package main

import (
	"fmt"
	"strings"
)

func reverse(arr []int) {
	for i := 0; i < len(arr)/2; i++ {
		j := len(arr) - 1 - i
		arr[i], arr[j] = arr[j], arr[i]
	}
}

func run(arr []int, lengths []int, index int, skip int) (int, int) {

	for _, le := range lengths {
		if le > len(arr) {
			continue
		}
		start := index
		s := make([]int, le, le)
		for j := 0; j < le; j++ {
			s[j] = arr[(start+j)%len(arr)]
		}
		reverse(s)
		for j := 0; j < le; j++ {
			arr[(start+j)%len(arr)] = s[j]
		}
		index = (index + le + skip) % len(arr)
		skip++
	}
	return index, skip
}
func reduce(arr []int) []int {
	res := []int{}
	for i := 0; i < len(arr); i += 16 {
		r := arr[i]
		for j := 1; j < 16; j++ {
			r = r ^ arr[j+i]
		}
		res = append(res, r)
	}
	return res
}

func toS(arr []int) string {
	s := []string{}
	for _, v := range arr {
		s = append(s, fmt.Sprintf("%d", v))
	}
	return strings.Join(s, ",")
}

func main() {
	arr := make([]int, 5, 5)
	lengths := []int{3, 4, 1, 5}
	for i := range arr {
		arr[i] = i
	}
	run(arr, lengths, 0, 0)
	fmt.Println(arr)

	arr = make([]int, 256, 256)
	lengths = []int{94, 84, 0, 79, 2, 27, 81, 1, 123, 93, 218, 23, 103, 255, 254, 243}
	for i := range arr {
		arr[i] = i
	}
	run(arr, lengths, 0, 0)
	fmt.Println(arr[0] * arr[1])
	//// PART 2

	arr = make([]int, 256, 256)
	for i := range arr {
		arr[i] = i
	}
	lengthsRaw := toS([]int{94, 84, 0, 79, 2, 27, 81, 1, 123, 93, 218, 23, 103, 255, 254, 243})
	lengths = []int{}
	for _, v := range lengthsRaw {
		lengths = append(lengths, int(v))
	}
	fmt.Println("LENGTHS", lengths)

	lengths = append(lengths, 17, 31, 73, 47, 23)
	index := 0
	skip := 0
	for i := 0; i < 64; i++ {
		index, skip = run(arr, lengths, index, skip)
	}
	denseHash := reduce(arr)
	fmt.Println(denseHash)
	for _, v := range denseHash {
		fmt.Printf("%02x", v)
	}
	fmt.Println()
}
