package day09

func maxScore(scores map[int]int) int {
	score := -1
	for _, v := range scores {
		if v > score {
			score = v
		}
	}
	return score
}

type Circle struct {
	value int
	next  *Circle
	prev  *Circle
}

func insert(circle []int, pos int, marble int) []int {
	if pos == len(circle) {
		circle = append(circle, marble)
		return circle
	}
	circle = append(circle, 0)
	copy(circle[pos+1:], circle[pos:])
	circle[pos] = marble
	return circle
}
func (c *Circle) insert(value int) *Circle {
	newC := &Circle{value: value, next: nil, prev: nil}
	if c.next == nil {
		c.next = newC
		c.prev = newC
		newC.next = c
		newC.prev = c
		return newC

	}

	target := c.next
	// update pointers for new
	newC.prev = target
	newC.next = target.next
	// update pointers for existing
	target.next.prev = newC
	target.next = newC
	return newC
}

func (c *Circle) remove() (*Circle, int) {
	toRemove := c
	for i := 0; i < 7; i++ {
		toRemove = toRemove.prev
	}
	value := toRemove.value
	toReturn := toRemove.next
	toRemove.prev.next = toRemove.next
	toRemove.next.prev = toRemove.prev
	toRemove.next = nil
	toRemove.prev = nil

	return toReturn, value
}
func remove(circle []int, index int) (int, int, []int) {
	pos := (index - 7)
	if pos < 0 {
		delta := 7 % len(circle)
		if index-delta >= 0 {
			pos = index - delta
		} else {
			pos = len(circle) - delta + index
		}
	}
	value := circle[pos]
	circle = append(circle[:pos], circle[pos+1:]...)
	return pos, value, circle

}

func Solve(players int, last_marble int) int {
	nextPlayer := func(currentPlayer int) int {
		if currentPlayer == players {
			return 1
		}
		return currentPlayer + 1

	}
	// C 1 N2
	//circle := []int{0}
	circle := &Circle{value: 0, next: nil, prev: nil}
	//	nextPos := func(currentPos int) int {
	//		newPos := (currentPos + 1) % len(circle)
	//		return newPos + 1
	//	}
	marble := 1
	player := 1
	scores := make(map[int]int)
	//	index := 0
	for marble <= last_marble {
		if marble%23 != 0 {
			//pos := nextPos(index)
			//circle = insert(circle, pos, marble)
			//index = pos
			circle = circle.insert(marble)
		} else {
			scores[player] += marble
			add := 0
			//index, add, circle = remove(circle, index)
			circle, add = circle.remove()
			scores[player] += add
		}
		player = nextPlayer(player)
		marble++
	}

	return maxScore(scores)
}
