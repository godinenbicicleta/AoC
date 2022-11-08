package main

import (
	"crypto/md5"
	"fmt"
	"strconv"
)

const (
	input = "ihaygndm"
)


func toMd5(index int, n int) string {
	data := []byte(input)
	data = append(data, []byte(strconv.Itoa(index))...)
	s := fmt.Sprintf("%x", md5.Sum(data))
	for i := 1; i < n; i++ {
		data := []byte(s)
		s = fmt.Sprintf("%x", md5.Sum(data))
	}
	return s
}

func toMaps(s string) (map[byte]bool, map[byte]bool) {
	has3 := map[byte]bool{}
	has5 := map[byte]bool{}
	i := 0
	found3 := false
	for i+2 < len(s) {
		c := s[i]
		if c == s[i+1] && c == s[i+2] {
			if !found3 {
				has3[c] = true
				found3 = true
			}
			if i+4 < len(s) {
				if c == s[i+3] && c == s[i+4] {
					has5[c] = true
					i += 5
					continue
				}

			}
			i += 3
			continue
		}
		i++
	}
	return has3, has5
}

func main() {
	index := 0
	size := 1000000
	hs := make([]string, size, size)
	n := 2017
	hashes := 0
	for hashes < 64 {
		h := hs[index]
		if h == "" {
			h = toMd5(index, n)
			hs[index] = h
		}
		m3, _ := toMaps(h)
		if len(m3) == 0 {
			index++
			continue
		}
	Loop:
		for i := index + 1; i < index+1000; i++ {
			h2 := hs[i]
			if h2 == "" {
				h2 = toMd5(i, n)
				hs[i] = h2
			}
			_, m5 := toMaps(h2)
			if len(m5) == 0 {
				continue
			}
			for k := range m3 {
				if m5[k] {
					hashes++
					break Loop
				}

			}
		}

		index++

	}

	fmt.Println("Index: ", index-1)
}
