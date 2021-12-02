package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type triangle struct {
	a int
	b int
	c int
}

func (t triangle) valid() bool {
	return t.a+t.b > t.c && t.a+t.c > t.b && t.c+t.b > t.a
}

func (t triangle) String() string {
	return fmt.Sprintf("Triangle(%d %d %d)", t.a, t.b, t.c)
}

func triangleFromSides(a, b, c int) triangle {
	return triangle{a, b, c}
}

func getTriangles() []triangle {
	scanner := bufio.NewScanner(os.Stdin)
	var triangles []triangle
	var allNums []int
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		strSlice := regexp.MustCompile(`\s`).Split(line, -1)
		var nums []int
		for _, s := range strSlice {
			if s == "" {
				continue
			}
			num, err := strconv.Atoi(s)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error %v", err)
				os.Exit(1)
			}
			nums = append(nums, num)
			allNums = append(allNums, num)
		}
		t := triangleFromSides(nums[0], nums[1], nums[2])
		if t.valid() {
			triangles = append(triangles, t)
		}

	}

	var flatNums []int
	for offset := 0; offset < 3; offset++ {
		for i := offset; i < len(allNums); i += 3 {
			flatNums = append(flatNums, allNums[i])
		}
	}
	valid2 := 0
	for i := 0; i < len(flatNums); i += 3 {
		a, b, c := flatNums[i], flatNums[i+1], flatNums[i+2]
		t := triangle{a, b, c}
		if t.valid() {
			valid2++
		}
	}
	fmt.Println("Valid2", valid2)

	return triangles

}

func main() {
	triangles := getTriangles()
	fmt.Println(len(triangles))

}
