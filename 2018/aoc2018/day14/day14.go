package main

import (
	"fmt"
	"strings"
)

const INPUT int = 939601
const SIZE int = INPUT + 10

func toString(arr []int) string {
	var s strings.Builder
	for _, num := range arr {
		s.WriteString(fmt.Sprintf("%d", num))
	}
	return s.String()
}

func main() {
	arr := make([]int, 0, SIZE*3)
	arr = append(arr, 3)
	arr = append(arr, 7)
	x := 0
	y := 1
	inputString := fmt.Sprintf("%d", INPUT)
	lenInput := len(inputString)
	for {
		sum := arr[x] + arr[y]
		if sum < 10 {
			arr = append(arr, sum)
		} else {
			arr = append(arr, sum/10)
			arr = append(arr, sum%10)
		}
		x = (1 + arr[x] + x) % len(arr)
		y = (1 + arr[y] + y) % len(arr)

		if len(arr) == SIZE {
			fmt.Println(toString(arr[INPUT : INPUT+10]))
		}

		endPos := len(arr)
		startPos := endPos - lenInput
		if endPos > lenInput && toString(arr[startPos:]) == inputString {
			fmt.Println(endPos-lenInput, arr[startPos:])
			break
		}
		if endPos > lenInput && toString(arr[startPos-1:endPos-1]) == inputString {
			fmt.Println(endPos-lenInput-1, arr[startPos-1:endPos-1])
			break
		}
	}
}
