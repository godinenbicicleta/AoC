package day08

import (
	"testing"
)

func TestSolve(t *testing.T) {
	t.Log("P1 (test): ", Solve("input_test.txt"))
	t.Log("P2 (test): ", Solve2("input_test.txt"))
	t.Log("P1: ", Solve("input.txt"))
	t.Log("P2: ", Solve2("input.txt"))
}
