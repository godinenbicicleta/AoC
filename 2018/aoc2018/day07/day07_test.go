package day07

import (
	"testing"
)

func TestSolve(t *testing.T) {
	//t.Log(Solve("input_test.txt"))
	t.Log("P1:", Solve("input.txt"))
	//t.Log(Solve2("input_test.txt", 2, 0))
	t.Log("P2: ", Solve2("input.txt", 4, 60))
}
