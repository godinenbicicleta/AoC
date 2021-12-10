package main

import "fmt"
import "os"
import "bufio"
import "strings"
import "regexp"
import "strconv"

type screen struct {
	coords [][]string
	width  int
	height int
}

func (s screen) String() string {
	var rowStr = []string{""}
	for _, row := range s.coords {
		rowStr = append(rowStr, strings.Join(row, ""))
	}
	rowStr = append(rowStr, "")

	return strings.Join(rowStr, "\n")
}

func (s screen) mark(j, i int) {
	s.coords[j][i] = "#"
}

func (s screen) rotateRow(y, by int) {
	row := s.coords[y]
	newRow := make([]string, len(row))
	for i, v := range row {
		ix := (i + by) % len(row)
		newRow[ix] = v
	}
	copy(s.coords[y], newRow)
}

func (s screen) rotateColumn(x, by int) {
	var col []string
	for _, row := range s.coords {
		col = append(col, row[x])
	}
	newCol := make([]string, len(col))
	for i, v := range col {
		ix := (i + by) % len(col)
		newCol[ix] = v
	}
	for j := range s.coords {
		s.coords[j][x] = newCol[j]
	}

}

func (s screen) process(instruction string) {
	if strings.HasPrefix(instruction, "rect") {
		var rect = regexp.MustCompile(`(\d+)x(\d+)`)
		var res = rect.FindStringSubmatch(instruction)
		w, err := strconv.Atoi(res[1])
		if err != nil {
			panic(err)
		}
		h, err := strconv.Atoi(res[2])
		if err != nil {
			panic(err)
		}
		for j := 0; j < h; j++ {
			for i := 0; i < w; i++ {
				s.mark(j, i)
			}
		}
	} else if strings.HasPrefix(instruction, "rotate row") {
		var pattern = regexp.MustCompile(`row y=(\d+) by (\d+)`)
		var res = pattern.FindStringSubmatch(instruction)
		row, err := strconv.Atoi(res[1])
		if err != nil {
			panic(err)
		}
		by, err := strconv.Atoi(res[2])
		if err != nil {
			panic(err)
		}
		s.rotateRow(row, by)
	} else if strings.HasPrefix(instruction, "rotate column") {
		var pattern = regexp.MustCompile(`column x=(\d+) by (\d+)`)
		var res = pattern.FindStringSubmatch(instruction)
		column, err := strconv.Atoi(res[1])
		if err != nil {
			panic(err)
		}
		by, err := strconv.Atoi(res[2])
		if err != nil {
			panic(err)
		}
		s.rotateColumn(column, by)
	}
}

func newScreen(width, height int) screen {
	var coords [][]string
	for y := 0; y < height; y++ {
		var row []string
		for x := 0; x < width; x++ {
			row = append(row, ".")
		}
		coords = append(coords, row)
	}
	return screen{coords, width, height}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var instructions []string
	for scanner.Scan() {
		instructions = append(instructions, scanner.Text())
	}

	s := newScreen(50, 6)
	fmt.Println(s)
	for _, instruction := range instructions {
		fmt.Println(instruction)
		s.process(instruction)
		fmt.Println(s)
	}

	total := 0
	for _, row := range s.coords {
		for _, c := range row {
			if c == "#" {
				total++
			}
		}
	}
	fmt.Println(total)
}
