package main

import "fmt"

func generate(num int) int {
	matches := 0
	a, b := 516, 190
	for i := 0; i < num; i++ {
		a = (a * 16807) % 2147483647
		b = (b * 48271) % 2147483647
		s1 := fmt.Sprintf("%032b", a)
		s2 := fmt.Sprintf("%032b", b)
		s1 = s1[16:]
		s2 = s2[16:]
		if s1 == s2 {
			matches++
		}
	}
	return matches
}
func generate2(num int) int {
	matches := 0
	a, b := 516, 190
	as := make([]string, 0, num)
	bs := make([]string, 0, num)
	for len(as) < num {
		a = (a * 16807) % 2147483647
		if a%4 != 0 {
			continue
		}
		s1 := fmt.Sprintf("%032b", a)
		s1 = s1[16:]
		as = append(as, s1)
	}
	for len(bs) < num {
		b = (b * 48271) % 2147483647
		if b%8 != 0 {
			continue
		}
		s2 := fmt.Sprintf("%032b", b)
		s2 = s2[16:]
		bs = append(bs, s2)
	}
	for i := 0; i < num; i++ {
		if as[i] == bs[i] {
			matches++
		}
	}
	return matches
}

func main() {
	// Generator A starts with 516
	//Generator B starts with 190
	fmt.Println(generate(40000000))
	fmt.Println(generate2(5000000))

}
