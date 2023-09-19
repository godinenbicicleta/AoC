package day03

import "testing"

func TestTwoOrMore(t *testing.T) {
	count := TwoOrMore("input.txt")
	t.Logf("P1: %d", count)
}
func TestIntersects(t *testing.T) {
	id := NoIntersects("input.txt")
	t.Logf("P2: %d", id)
}
