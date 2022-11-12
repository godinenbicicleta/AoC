package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func run(arr []int, increase func(int) int) int {
	nums := make([]int, len(arr), len(arr))
	copy(nums, arr)

	var steps int
	for index := 0; index < len(nums) && index >= 0; steps++ {
		old := index
		index += nums[index]
		nums[old] = increase(nums[old])

	}
	return steps
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	arr := []int{}
	for scanner.Scan() {
		var num int
		_, err := fmt.Sscanf(scanner.Text(), "%d", &num)
		if err != nil {
			log.Fatal("Error parsing")
		}
		arr = append(arr, num)
	}

	steps := run(arr, func(i int) int { return i + 1 })
	fmt.Println(steps)
	steps = run(arr, func(i int) int {
		if i >= 3 {
			return i - 1
		}
		return i + 1
	})
	fmt.Println(steps)
}
