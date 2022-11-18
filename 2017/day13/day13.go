package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type cell struct {
	r int
	d int
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var in []cell
	maxr := 0
	for scanner.Scan() {
		var r, d int
		line := scanner.Text()
		_, err := fmt.Sscanf(scanner.Text(), "%d: %d", &r, &d)
		if err != nil {
			log.Fatal("Error parsing", line)
		}
		in = append(in, cell{r: r, d: d})
		if r > maxr {
			maxr = r
		}
	}

	arr := make([]int, maxr+1, maxr+1)
	for _, elem := range in {
		arr[elem.r] = elem.d
	}

	fmt.Println(arr)

	sev := 0
	for i := range arr {
		d := arr[i]
		if d == 0 {
			continue
		}
		if i%(2*(d-1)) == 0 {
			if len(arr) < 10 {
				fmt.Println("Hit at i", i, "d", d)
			}
			sev += (i * d)
		}
	}
	fmt.Println(sev)
	delay := 0
Loop:
	for {
		for i := range arr {
			d := arr[i]
			if d == 0 {
				continue
			}
			if (delay+i)%(2*(d-1)) == 0 {
				delay++
				continue Loop
			}
		}
		fmt.Println(delay)
		break
	}
}
