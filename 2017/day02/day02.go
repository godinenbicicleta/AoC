package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"sort"
	"strconv"
)

func process(nums []int) (int, int) {
	sort.Ints(nums)
	p1 := nums[len(nums)-1] - nums[0]
	var p2 int
Loop:
	for i := len(nums) - 1; i > -1; i-- {
		for j, div := range nums {
			if i == j {
				continue
			}
			if nums[i]%div == 0 {
				p2 = nums[i] / div
				break Loop
			}
		}
	}
	return p1, p2
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	re := regexp.MustCompile(`\d+`)
	total1 := 0
	total2 := 0
	for scanner.Scan() {
		line := scanner.Text()
		elems := re.FindAllString(line, -1)
		nums := make([]int, 0, len(elems))
		for _, elem := range elems {
			num, err := strconv.Atoi(elem)
			if err != nil {
				log.Fatal("Error parsing", elem)
			}
			nums = append(nums, num)
		}

		p1, p2 := process(nums)
		total1 += p1
		total2 += p2

	}

	fmt.Println(total1)
	fmt.Println(total2)
}
