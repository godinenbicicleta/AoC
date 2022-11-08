package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

// Interval represents an interval
type Interval struct {
	min int
	max int
}

func max(a int, b int) int {
	if b > a {
		return b
	}
	return a
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var left int
	var right int
	intervals := make([]Interval, 0, 10000)
	for scanner.Scan() {
		line := scanner.Text()
		fmt.Sscanf(line, "%d-%d", &left, &right)
		intervals = append(intervals, Interval{min: left, max: right})
	}
	sort.Slice(intervals, func(i, j int) bool {
		return intervals[i].min < intervals[j].min
	})

	mergedIntervals := make([]Interval, 0, len(intervals))
	mergedIntervals = append(mergedIntervals, intervals[0])
	ci := 0
	for _, next := range intervals[1:] {
		current := mergedIntervals[ci]
		if next.min <= current.max+1 {
			mergedIntervals[ci] = Interval{min: current.min, max: max(next.max, current.max)}
			continue
		}
		mergedIntervals = append(mergedIntervals, next)
		ci++
	}

	// p1
	fmt.Println(mergedIntervals[0].max + 1)

	//p2
	maxNum := 4294967295
	allowed := 0
	for i := 1; i < len(mergedIntervals); i++ {
		right := mergedIntervals[i]
		left := mergedIntervals[i-1]
		allowed += right.min - left.max - 1
	}
	if mergedIntervals[len(mergedIntervals)-1].max < maxNum {
		allowed += maxNum - mergedIntervals[len(mergedIntervals)-1].max + 1
	}
	fmt.Println(allowed)

}
