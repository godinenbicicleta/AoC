package day05

import (
	"os"
)

func Solve(fname string) int {
	bts, err := os.ReadFile(fname)
	if err != nil {
		panic(err)
	}

	s := reduce(bts[:len(bts)-1])
	return len(s)
}
func filter(bts []byte, c1, c2 byte) []byte {
	res := []byte{}
	for _, c := range bts {
		if c != c1 && c != c2 {
			res = append(res, c)
		}
	}
	return res
}

func Solve2(fname string) int {
	bts, err := os.ReadFile(fname)
	if err != nil {
		panic(err)
	}
	minSize := -1
	for c := 'A'; c <= 'Z'; c++ {
		bs := filter(bts, byte(c), byte(c+32))
		s := reduce(bs[:len(bs)-1])
		size := len(s)
		if minSize < 0 || size < minSize {
			minSize = size
		}
	}
	return minSize
}

func reduce(s []byte) string {
	for {
		size := len(s)
		new_s := []byte{}
		i := 1
		for i < len(s) {
			prev := s[i-1]
			current := s[i]
			if prev-current == 32 || current-prev == 32 {
				i += 2

			} else {
				new_s = append(new_s, prev)
				i++
			}
			if i == len(s) {
				new_s = append(new_s, current)
			}
		}
		s = new_s

		if size == len(s) {
			break
		}
	}

	return string(s)
}
