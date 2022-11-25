package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

func abs(i int) int {
	if i > 0 {
		return i
	}
	return -i
}

// V represents a vector
type V struct {
	x int
	y int
	z int
}

// P represents a particle
type P struct {
	p V
	v V
	a V
}

func dist(p1, p2 P) int {
	return abs(p1.p.x-p2.p.x) + abs(p1.p.y-p2.p.y) + abs(p1.p.z-p2.p.z)
}

func update(particle P) P {
	a := particle.a
	v := particle.v
	p := particle.p
	nv := V{v.x + a.x, v.y + a.y, v.z + a.z}
	np := V{p.x + nv.x, p.y + nv.y, p.z + nv.z}
	return P{np, nv, a}
}

func sim(particles []P) []P {
	var unchanged int
	for unchanged < 20 {
		toRemove := map[P]bool{}
		for ix, p1 := range particles {
			for jx, p2 := range particles {
				if jx <= ix {
					continue
				}
				d := dist(p1, p2)
				if d == 0 {
					toRemove[p1] = true
					toRemove[p2] = true
				}
			}
		}
		newP := make([]P, 0, len(particles))
		for _, p := range particles {
			if toRemove[p] {
				continue
			}
			newP = append(newP, p)
		}
		// fill newP
		minDistance := -1
		for ix, p1 := range newP {
			for jx, p2 := range newP {
				if jx <= ix {
					continue
				}
				d := abs(p1.p.x-p2.p.x) + abs(p1.p.y-p2.p.y) + abs(p1.p.z-p2.p.z)
				if d < minDistance || minDistance < 0 {
					minDistance = d
				}
			}
		}
		// see if there were particles that collided
		if len(newP) == len(particles) {
			unchanged++
		} else {
			unchanged = 0
		}

		// update positions and velocities
		for i := 0; i < len(newP); i++ {
			newP[i] = update(particles[i])
		}
		particles = newP
	}
	return particles

}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	minA := 1 << 50
	i := -1
	index := -1
	pattern := `p=<\s?(-?\d+),\s?(-?\d+),\s?(-?\d+)>, v=<\s?(-?\d+),\s?(-?\d+),\s?(-?\d+)>, a=<\s?(-?\d+),\s?(-?\d+),\s?(-?\d+)>`
	re := regexp.MustCompile(pattern)
	var particles []P
	for scanner.Scan() {
		i++
		text := scanner.Text()
		var ms []int
		for _, m := range re.FindStringSubmatch(text)[1:] {
			mInt, err := strconv.Atoi(m)
			if err != nil {
				log.Fatal("ERROR parsing ", m)
			}
			ms = append(ms, mInt)
		}
		p := P{V{ms[0], ms[1], ms[2]}, V{ms[3], ms[4], ms[5]}, V{ms[6], ms[7], ms[8]}}
		particles = append(particles, p)
		a := abs(p.a.x) + abs(p.a.y) + abs(p.a.z)
		if a < minA {
			index = i
			minA = a
		}
	}
	fmt.Println(index)
	p := sim(particles)
	fmt.Println("Particles left", len(p))
}
