package day09

import (
	"fmt"
	"testing"
)

func TestSolve(t *testing.T) {
	// 473 players; last marble is worth 70904 points
	tests := []struct {
		players int
		marble  int
		score   int
	}{
		{9, 25, 32},
		{10, 1618, 8317},
		{13, 7999, 146373},
		{17, 1104, 2764},
		{21, 6111, 54718},
		{30, 5807, 37305},
	}
	for _, test := range tests {
		t.Run(fmt.Sprintf("%d players; last marble is worth %d points", test.players, test.marble), func(t *testing.T) {
			actual := Solve(test.players, test.marble)
			if actual != test.score {
				t.Errorf("Expected %d, got %d for %v", test.score, actual, test)
			}
		})
	}
	t.Log("P1: ", Solve(473, 70904))

	t.Log("P2: ", Solve(473, 70904*100))
}
