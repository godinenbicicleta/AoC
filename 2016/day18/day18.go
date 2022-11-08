package main

import (
	"bufio"
	"bytes"
	"fmt"
	"os"
)

func process(line []byte) []byte {
	arr := make([]byte, len(line)+2, len(line)+2)
	res := make([]byte, len(line), len(line))
	arr[0] = '.'
	copy(arr[1:], line)
	arr[len(line)+1] = '.'
	for i := 1; i < len(arr)-1; i++ {
		res[i-1] = parse(arr[i-1], arr[0], arr[i+1])
	}
	return res
}

func parse(left, center, right byte) byte {
	if left == '^' && center == '^' && right == '.' {
		return '^'
	}
	if center == '^' && right == '^' && left == '.' {
		return '^'
	}
	if left == '^' && right != left && center != left {
		return '^'
	}
	if right == '^' && left != right && center != right {
		return '^'
	}
	return '.'
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	rows := 400000
	var prev []byte
	for scanner.Scan() {
		prev = scanner.Bytes()
	}

	var line []byte
	counted := bytes.Count(prev, []byte("."))
	for i := 1; i < rows; i++ {
		line = process(prev)
		counted += bytes.Count(line, []byte("."))
		prev = line
	}
	fmt.Println(counted)
}
