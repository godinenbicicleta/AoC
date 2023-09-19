package day01

import (
	"bufio"
	"log"
	"os"
	"strconv"
)

func SumFile(fname string) int {
	input, err := os.Open(fname)
	if err != nil {
		log.Fatalf("Error reading input file %s", err)
	}
	defer input.Close()
	scanner := bufio.NewScanner(input)
	total := 0
	for scanner.Scan() {
		line := scanner.Text()
		num, err := strconv.Atoi(line)
		if err != nil {
			log.Fatalf("Error parsing num %s: %s", line, err)
		}
		total += num
	}
	return total
}

func FindTwice(fname string) int {
	input, err := os.Open(fname)
	if err != nil {
		log.Fatalf("Error reading input file %s", err)
	}
	defer input.Close()
	total := 0
	cache := make(map[int]int)
	nums := []int{}

	scanner := bufio.NewScanner(input)
	for scanner.Scan() {
		line := scanner.Text()
		num, err := strconv.Atoi(line)
		if err != nil {
			log.Fatalf("Error parsing num %s: %s", line, err)
		}
		nums = append(nums, num)
	}
	for i := 0; ; i = (i + 1) % len(nums) {
		total += nums[i]
		cache[total]++
		if cache[total] > 1 {
			return total
		}
	}
}
