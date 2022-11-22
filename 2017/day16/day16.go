package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func rotate(arr []byte, num int) {
	num = num % len(arr)
	cpy := make([]byte, len(arr), len(arr))
	copy(cpy, arr[len(arr)-num:])
	copy(cpy[num:], arr[:len(arr)-num])
	copy(arr, cpy)
}

func process(arr []byte, w string) {
	switch w[0] {
	case 's':
		num, err := strconv.Atoi(w[1:])
		if err != nil {
			log.Fatal("Error parsing", w)
		}
		rotate(arr, num)
	case 'x':
		parts := strings.Split(w[1:], "/")
		p1, err := strconv.Atoi(parts[0])
		if err != nil {
			log.Fatal("Error parsing", w)
		}
		p2, err := strconv.Atoi(parts[1])
		if err != nil {
			log.Fatal("Error parsing", w)
		}
		arr[p1], arr[p2] = arr[p2], arr[p1]
	case 'p':
		parts := strings.Split(w[1:], "/")
		var i, j int
		for ix, a := range arr {
			if a == parts[0][0] {
				i = ix
			}
			if a == parts[1][0] {
				j = ix
			}
		}
		arr[i], arr[j] = arr[j], arr[i]
	}

}

func parse(ws []string) func(arr []byte, num int) string {
	res := []func(arr []byte){}
	for _, w := range ws {
		switch w[0] {
		case 's':
			num, err := strconv.Atoi(w[1:])
			if err != nil {
				log.Fatal("Error parsing", w)
			}
			f := func(arr []byte) {
				rotate(arr, num)
			}
			res = append(res, f)
		case 'x':
			parts := strings.Split(w[1:], "/")
			p1, err := strconv.Atoi(parts[0])
			if err != nil {
				log.Fatal("Error parsing", w)
			}
			p2, err := strconv.Atoi(parts[1])
			if err != nil {
				log.Fatal("Error parsing", w)
			}
			f := func(arr []byte) {
				arr[p1], arr[p2] = arr[p2], arr[p1]
			}
			res = append(res, f)
		case 'p':
			parts := strings.Split(w[1:], "/")
			f := func(arr []byte) {
				var i, j int
				for ix, a := range arr {
					if a == parts[0][0] {
						i = ix
					}
					if a == parts[1][0] {
						j = ix
					}
				}
				arr[i], arr[j] = arr[j], arr[i]
			}
			res = append(res, f)
		}

	}

	return func(arr []byte, num int) string {
		seen := map[string][]int{}
		for i := 0; i < num%48; i++ {

			for _, f := range res {
				f(arr)
			}
			if len(seen[string(arr)]) > 0 {
				fmt.Println(string(arr), seen[string(arr)])
			}
			seen[string(arr)] = append(seen[string(arr)], i)
		}
		return string(arr)
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		line := scanner.Text()
		words := strings.Split(line, ",")
		funcs := parse(words)
		res1 := funcs([]byte("abcdefghijklmnop"), 1)
		res2 := funcs([]byte("abcdefghijklmnop"), 1000000000)
		fmt.Println(string(res1))
		fmt.Println(string(res2))
	}
}
