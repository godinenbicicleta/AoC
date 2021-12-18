package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func parseInt(s string) int {
	n, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return n
}
func p1(line string) {
	i := 0
	for i < len(line) {
		c := line[i]
		if c == '(' {
			re := regexp.MustCompile(`\((\d+)x(\d+)\)`)
			matchArray := re.FindStringSubmatch(line[i:])
			leftNum := parseInt(matchArray[1])
			rightNum := parseInt(matchArray[2])
			nextP := i + len(matchArray[1]) + 1 + len(matchArray[2]) + 1
			segment := line[nextP+1 : nextP+1+leftNum]
			newLine := line[:i]
			for k := 0; k < rightNum; k++ {
				newLine += segment
				i += leftNum
			}
			line = newLine + line[nextP+1+leftNum:]

		} else {
			i++
		}

	}
	fmt.Println(len(line))

}

func p2(line string) int {
	total := 0
	for len(line) > 0 {
		if line[0] != '(' {
			total++
			line = line[1:]
			continue
		}

		re := regexp.MustCompile(`\((\d+)x(\d+)\)`)
		matchArray := re.FindStringSubmatch(line)
		leftNum := parseInt(matchArray[1])
		rightNum := parseInt(matchArray[2])
		nextP := len(matchArray[1]) + 1 + len(matchArray[2]) + 1
		start, end := nextP+1, nextP+1+leftNum
		total += rightNum * p2(line[start:end])
		line = line[end:]

	}
	return total

}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		line := scanner.Text()
		//fmt.Printf("%s\t", line)
		p1(line)
		fmt.Println(p2(line))

	}
}
