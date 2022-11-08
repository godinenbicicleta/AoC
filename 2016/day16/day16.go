package main

import "fmt"

func rev(s []byte) []byte {
	revS := make([]byte, len(s)+1, len(s)+1)
	revS[0] = '0'
	for i, r := range s {
		if r == '0' {
			revS[len(s)-i] = '1'
		} else {
			revS[len(s)-i] = '0'
		}
	}

	return revS
}

func reduce(w []byte) []byte {
	cs := make([]byte, 0, len(w)/2)
	for i := 0; i < len(w)-1; i += 2 {
		if w[i] == w[i+1] {
			cs = append(cs, '1')
		} else {
			cs = append(cs, '0')
		}
	}
	return cs
}

func main() {

	for _, p := range []struct {
		target  int
		initial string
	}{
		{20, "10000"},
		{272, "11101000110010100"},
		{35651584, "11101000110010100"},
	} {
		target := p.target
		initial := []byte(p.initial)
		w := make([]byte, len(initial), target*2)
		copy(w, initial)
		for len(w) < target {
			w = append(w, rev(w)...)
		}
		w = w[:target]

		for len(w)%2 == 0 {
			w = reduce(w)
		}

		fmt.Println(string(w))
	}

}
