package day02

import (
	"bufio"
	"os"
)

func CheckSum(fname string) int {
	file, err := os.Open(fname)
	defer file.Close()
	if err != nil {
		panic(err)
	}
	twoLetters := 0
	threeLetters := 0
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Bytes()
		if CountLetter(line, 2) {
			twoLetters++
		}
		if CountLetter(line, 3) {
			threeLetters++
		}
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}
	return twoLetters * threeLetters
}

func CountLetter(bs []byte, goal int) bool {
	counts := make([]int, 128)
	for _, b := range bs {
		counts[b]++

	}
	for _, elem := range counts {
		if elem == goal {
			return true
		}
	}
	return false
}

func Differ(fname string) string {
	file, err := os.Open(fname)
	defer file.Close()
	if err != nil {
		panic(err)
	}
	scanner := bufio.NewScanner(file)
	lines := [][]byte{}
	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, []byte(line))
	}

	for i := range lines {
		for j := range lines {
			l1 := lines[i]
			l2 := lines[j]
			if Diff(l1, l2) == 1 {
				return Common(l1, l2)
			}
		}
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}
	return ""
}

func Diff(left []byte, right []byte) int {
	total := 0
	for i := range left {
		if left[i] != right[i] {
			total++
		}
	}
	return total
}

func Common(left []byte, right []byte) string {
	res := []byte{}
	for i := range left {
		if left[i] == right[i] {
			res = append(res, left[i])
		}
	}
	return string(res)
}
