package day02

import (
	"log"
	"testing"
)

func TestP1(t *testing.T) {
	res := CheckSum("input.txt")
	log.Printf("\np1: %d\n", res)
}
func TestP2(t *testing.T) {
	res := Differ("input.txt")
	log.Printf("\np2: %s\n", res)
}
