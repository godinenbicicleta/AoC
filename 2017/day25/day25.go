package main

import "fmt"

func main() {
	tape := make(map[int]int)
	cursor := 0
	state := 'A'
	for i := 0; i < 12368930; i++ {
		switch state {
		case 'A':
			if tape[cursor] == 0 {
				tape[cursor] = 1
				state = 'B'
			} else {
				delete(tape, cursor)
				state = 'C'
			}
			cursor++
		case 'B':
			if tape[cursor] == 0 {
				cursor--
				state = 'A'
			} else {
				delete(tape, cursor)
				cursor++
				state = 'D'
			}
		case 'C':
			if tape[cursor] == 0 {
				tape[cursor] = 1
				state = 'D'
			} else {
				tape[cursor] = 1
				state = 'A'
			}
			cursor++
		case 'D':
			if tape[cursor] == 0 {
				tape[cursor] = 1
				state = 'E'
			} else {
				delete(tape, cursor)
				state = 'D'
			}
			cursor--
		case 'E':
			if tape[cursor] == 0 {
				tape[cursor] = 1
				cursor++
				state = 'F'
			} else {
				tape[cursor] = 1
				cursor--
				state = 'B'
			}
		case 'F':
			if tape[cursor] == 0 {
				tape[cursor] = 1
				state = 'A'
			} else {
				tape[cursor] = 1
				state = 'E'
			}
			cursor++
		}
	}
	total := 0
	for _, elem := range tape {
		total += elem
	}
	fmt.Println(total)
}
