package day04

import "testing"

func TestSolve(t *testing.T) {
	p1, p2 := Solve("input.txt")
	t.Logf("P1: %d", p1)
	t.Logf("P2: %d", p2)
}
