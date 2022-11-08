package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type disc struct {
	positions int
	position  int
}

func parse() []disc {
	scanner := bufio.NewScanner(os.Stdin)
	discs := []disc{}
	i := 1
	var discID, positions, position int
	for scanner.Scan() {
		line := scanner.Text()
		n, err := fmt.Sscanf(line, "Disc #%d has %d positions; at time=0, it is at position%d", &discID, &positions, &position)
		if err != nil || n < 3 {
			log.Fatalf("ERROR parsing %s", line)

		}

		discs = append(discs, disc{positions, (position + i) % positions})
		i++
	}

	return discs

}

func anyD(ds []disc, i int) bool {
	for _, disc := range ds {
		if (disc.position+i)%disc.positions != 0 {
			return true
		}
	}
	return false

}

func main() {
	discs := parse()
	var i int
	for i = 0; anyD(discs, i); i++ {
	}
	fmt.Println(i)

}
