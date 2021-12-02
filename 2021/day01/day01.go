package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func sum(arr []int) int {
	tot := 0
	for _, value := range arr {
		tot += value
	}
	return tot
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var nums []int
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		num, err := strconv.Atoi(line)
		if err != nil {
			log.Fatal("Error parsing num")
		}
		nums = append(nums, num)
	}
	for part, window := range [2]int{1, 3} {
		prev := 0
		counts := 0
		for i := 0; i < len(nums); i++ {
			if i+window > len(nums) {
				break
			}

			current := sum(nums[i : i+window])
			if prev > 0 && current > prev {
				counts++
			}
			prev = current

		}

		fmt.Println("Part ", part+1, counts)
	}
}
