package main

import (
	"fmt"
)

// Player struct
type Player struct {
	hitPoints int
	damage    int
	armor     int
	inventory []Item
	//items     []Item
}

// Item struct
type Item struct {
	cost   int
	damage int
	armor  int
	name   string
}

var weapons = []Item{
	{name: "Dagger", cost: 8, damage: 4},
	{name: "Shortsword", cost: 10, damage: 5},
	{name: "Warhammer", cost: 25, damage: 6},
	{name: "Longsword", cost: 40, damage: 7},
	{name: "Greataxe", cost: 74, damage: 8},
}

var armors = []Item{
	{name: "Leather", cost: 13, armor: 1},
	{name: "Chainmail", cost: 31, armor: 2},
	{name: "Splintmail", cost: 53, armor: 3},
	{name: "Bandedmail", cost: 75, armor: 4},
	{name: "Platemail", cost: 102, armor: 5},
}

var rings = []Item{
	{name: "Damage+1", cost: 25, armor: 0, damage: 1},
	{name: "Damage+2", cost: 50, armor: 0, damage: 2},
	{name: "Damage+3", cost: 100, armor: 0, damage: 3},
	{name: "Defense+1", cost: 20, armor: 1},
	{name: "Defense+2", cost: 40, armor: 2},
	{name: "Defense+3", cost: 80, armor: 3},
}


func cost(items []Item) int {
	totalCost := 0
	for _, item :=range items {
		totalCost += item.cost
	}
	return totalCost
}
// boss stats
// Hit Points: 109
// Damage: 8
// Armor: 2
// least amount of gold you can spend and still win the fight

func toKey(player Player) string {
	return fmt.Sprintf("%d %d %d", player.damage, player.armor, cost(player.inventory))
}
func main() {
	boss := Player{
		hitPoints: 109,
		damage:    8,
		armor:     2,
	}
	minGold := 8
	maxGold := 1000
	maxGoldToLose := 0
	seen := make(map[string]bool)
	shouldPrint := true
	for gold := minGold; gold < maxGold; gold++ {
		players := getPossiblePlayers(gold)
		for _, player := range players {
			if seen[toKey(player)]{
				continue
			} else {
				seen[toKey(player)] = true
			}
			playerWins := play(player, boss)
			if playerWins && shouldPrint {
				fmt.Printf("with gold = %d the player wins\n%#v\n", gold, player)
				shouldPrint = false
			} else {
				if invCost :=  cost(player.inventory); invCost > maxGoldToLose {
					maxGoldToLose = invCost
				}
			}

		}
	}
	fmt.Println("nMax Gold to lose", maxGoldToLose)
}

func play(player Player, boss Player) bool {
	bossDamage := boss.damage - player.armor
	if bossDamage < 0 {
		bossDamage = 1
	}
	playerDamage := player.damage - boss.armor
	if playerDamage < 0 {
		playerDamage = 1
	}
	playerLife := player.hitPoints
	bossLife := boss.hitPoints
	for {
		bossLife -= playerDamage
		if bossLife <= 0 {
			return true
		}
		playerLife -= bossDamage
		if playerLife <= 0 {
			return false
		}
	}
}

func getPossiblePlayers(gold int) []Player {
	var players []Player
	for _, weapon := range weapons {
		if weapon.cost > gold {
			continue
		}
		// only weapon
		players = append(players, Player{hitPoints: 100, damage: weapon.damage, inventory: []Item{weapon}})

		g := gold - weapon.cost
		// weapon + armor
		for _, armor := range armors {
			if armor.cost > g {
				continue
			}

			// only weapon + armor
			players = append(players, Player{hitPoints: 100, damage: weapon.damage, armor: armor.armor, inventory: []Item{weapon, armor}})
			// weapon + armor + rings
			d := g - armor.cost
			for i := 0; i < len(rings); i++ {
				ring := rings[i]
				if ring.cost > d {
					continue
				}

				// weapon + armor + ring1
				players = append(players, Player{hitPoints: 100, damage: weapon.damage + ring.damage, armor: armor.armor + ring.armor, inventory: []Item{weapon, ring, armor}})
				e := d - ring.cost
				for j := i + 1; j < len(rings); j++ {
					ring2 := rings[j]
					if ring2.cost > e {
						continue
					}
					// weapon + armor + ring + ring2
					players = append(players, Player{hitPoints: 100, damage: weapon.damage + ring.damage + ring2.damage, armor: armor.armor + ring.armor + ring2.armor, inventory: []Item{weapon, ring, ring2, armor}})

				}

			}

		}
		// weapon + rings
		for i := 0; i < len(rings); i++ {
			ring := rings[i]
			if ring.cost > g {
				continue
			}
			// weapon  + ring1
			players = append(players, Player{hitPoints: 100, damage: weapon.damage + ring.damage, armor: ring.armor, inventory: []Item{weapon, ring}})
			e := g - ring.cost
			for j := i + 1; j < len(rings); j++ {
				ring2 := rings[j]
				if ring2.cost > e {
					continue
				}
				// weapon + armor + ring + ring2
				players = append(players, Player{hitPoints: 100, damage: weapon.damage + ring.damage + ring2.damage, armor: ring.armor + ring2.armor, inventory: []Item{weapon, ring, ring2}})

			}

		}
	}

	return players
}
