package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func p1(line string) {
	i := 0
	for {
		c := line[i]
		if c == '(' {
			re := regexp.MustCompile(`\((\d+)x(\d+)\)`)
			matchArray := re.FindStringSubmatch(line[i:])
			leftNum, err := strconv.Atoi(matchArray[1])
			if err != nil {
				panic(err)
			}
			rightNum, err := strconv.Atoi(matchArray[2])
			if err != nil {
				panic(err)
			}
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

		if i >= len(line) {
			break
		}
	}
	fmt.Println(len(line))

}

func p2(line string) int {
	total := 0
	for len(line) > 0 {
		c := line[0]
		if c != '(' {
			ix := strings.Index(line, "(")
			if ix == -1 {
				total += len(line)
				break
			}
			total += ix
			line = line[ix:]
			continue
		}

		re := regexp.MustCompile(`\((\d+)x(\d+)\)`)
		matchArray := re.FindStringSubmatch(line)
		leftNum, err := strconv.Atoi(matchArray[1])
		if err != nil {
			panic(err)
		}
		rightNum, err := strconv.Atoi(matchArray[2])
		if err != nil {
			panic(err)
		}
		nextP := len(matchArray[1]) + 1 + len(matchArray[2]) + 1
		if rightNum == 1 {
			line = line[nextP+1:]
			continue
		}
		start, end := nextP+1, nextP+1+leftNum
		segment := line[start:end]
		if !strings.Contains(segment, "(") {
			total += leftNum * rightNum
			line = line[end:]
		} else {
			total += rightNum * p2(line[start:end])
			line = line[end:]

		}

		if len(line) == 0 {
			break
		}
	}
	return total

}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		line := scanner.Text()
		//fmt.Printf("%s\t", line)
		//p1(line)
		fmt.Println(p2(line))

	}
}
