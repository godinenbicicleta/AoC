package day01

import (
	"testing"
)

func TestDay01(t *testing.T) {
	total := SumFile("input.txt")
	t.Logf("Day01 (part 1): %d", total)
}
func TestDay01P2(t *testing.T) {
	total := FindTwice("input.txt")
	t.Logf("Day01 (part 2): %d", total)
}
