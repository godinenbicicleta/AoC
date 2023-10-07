package day05

import "testing"

func TestSolve(t *testing.T) {
	res := Solve("input.txt")
	t.Logf("P1: %v", res)
}
func TestSolve2(t *testing.T) {
	res := Solve2("input.txt")
	t.Logf("P2: %v", res)
}
