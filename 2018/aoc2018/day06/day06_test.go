package day06

import "testing"

func TestSolveTest(t *testing.T) {
	res := Solve("input_test.txt")
	t.Logf("P test: %d", res)
}
func TestSolve(t *testing.T) {
	res := Solve("input.txt")
	t.Logf("P1: %d", res)
	res2 := Solve2("input.txt")
	t.Logf("P2: %d", res2)
}
