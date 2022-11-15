package main

import (
	"bufio"
	"fmt"
	"os"
)

func score(bs []byte) int {
	cancel := false
	garbage := false
	level := 0
	s := 0
	inGarbage := 0
	for _, c := range bs {
		//fmt.Println("c", string([]byte{c}), garbage, inGarbage)
		if cancel {
			cancel = false
			continue
		}
		if c == '!' {
			cancel = true
			continue
		}
		if !garbage && c == '<' {
			garbage = true
			continue
		}
		if garbage && c != '>' {
			inGarbage++
			continue
		}
		if garbage && c == '>' {
			garbage = false
			continue
		}
		if c == '{' {
			level++
			continue
		}
		if c == '}' {
			s += level
			level--
		}
	}
	fmt.Println("garbage", inGarbage)
	return s

}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		fmt.Println(score(scanner.Bytes()))
	}
}
