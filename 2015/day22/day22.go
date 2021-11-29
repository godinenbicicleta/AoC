package main

// 173 too low
import (
	"fmt"
	"os"
)

// boss stats
// Hit Points: 71
// Damage: 10

type Game struct {
	player       Player
	boss         Player
	effects      []Spell
	manaSpent    int
	winner       string
	spellHistory []Spell
}

type Player struct {
	hitPoints int
	damage    int
	mana      int
}

type Spell struct {
	name      string
	cost      int
	damage    int
	hitPoints int
	armor     int
	turns     int
	mana      int
}

var spells = [...]Spell{
	{name: "Magic Missile", cost: 53, damage: 4},
	{name: "Drain", cost: 73, damage: 2, hitPoints: 2},
	{name: "Shield", cost: 113, turns: 6, armor: 7},
	{name: "Poison", cost: 173, turns: 6, damage: 3},
	{name: "Recharge", cost: 229, turns: 5, mana: 101},
}

func contains(effects []Spell, spell Spell) bool {
	for _, eff := range effects {
		if eff.name == spell.name {
			return true
		}

	}
	return false
}

func (s Spell) String() string {
	return s.name
}

func (p Player) String() string {
	return fmt.Sprintf("P( ht: %d, mana: %d, damage: %d ,)", p.hitPoints, p.mana, p.damage)
}

func (game Game) String() string {
	return fmt.Sprintf("player: %s, boss: %s, sh: %s, manaSpent: %d, winner: %s", game.player, game.boss, game.spellHistory, game.manaSpent, game.winner)
}

func sh(s []Spell) []Spell {
	var res []Spell
	res = append(res, s...)
	return res
}
func (game Game) newTurn(hardMode bool) []Game {
	if game.winner == "player" || game.winner == "boss" {
		return []Game{game}
	}
	var newEffects []Spell
	// effects before player's turn
	if hardMode {
		game.player.hitPoints -= 1
	}
	if game.player.hitPoints <= 0 {
		return []Game{{winner: "boss", manaSpent: game.manaSpent, spellHistory: sh(game.spellHistory)}}
	}
	for _, effect := range game.effects {
		game.player.mana += effect.mana
		game.boss.hitPoints -= effect.damage
		effect.turns -= 1

		if effect.turns > 0 {
			newEffects = append(newEffects, effect)
		}
	}
	if game.boss.hitPoints <= 0 {
		return []Game{{winner: "player", manaSpent: game.manaSpent, spellHistory: sh(game.spellHistory)}}
	}
	var newGames []Game

	// players turn
	for _, spell := range spells {
		if spell.cost > game.player.mana {
			continue
		}
		if spell.turns > 0 && contains(newEffects, spell) {
			continue
		}
		if spell.turns == 0 {
			newPlayer := Player{hitPoints: game.player.hitPoints + spell.hitPoints, damage: 0, mana: game.player.mana - spell.cost}
			newBoss := Player{hitPoints: game.boss.hitPoints - spell.damage, damage: game.boss.damage}
			if newBoss.hitPoints <= 0 {
				newSh := sh(game.spellHistory)
				newSh = append(newSh, spell)

				newGames = append(newGames, Game{winner: "player", player: newPlayer, boss: newBoss, manaSpent: game.manaSpent + spell.cost, spellHistory: newSh})
				continue
			}

			var gameEffects []Spell
			gameEffects = append(gameEffects, newEffects...)

			newSh := sh(game.spellHistory)
			newSh = append(newSh, spell)
			g := Game{player: newPlayer, boss: newBoss, manaSpent: game.manaSpent + spell.cost, effects: gameEffects, spellHistory: newSh}
			newGames = append(newGames, g)
			continue
		}
		newPlayer := Player{hitPoints: game.player.hitPoints, damage: 0, mana: game.player.mana - spell.cost}
		newBoss := Player{hitPoints: game.boss.hitPoints, damage: game.boss.damage}
		var gameEffects []Spell
		gameEffects = append(gameEffects, newEffects...)
		gameEffects = append(gameEffects, spell)

		newSh := sh(game.spellHistory)
		newSh = append(newSh, spell)

		g := Game{player: newPlayer, boss: newBoss, manaSpent: game.manaSpent + spell.cost, effects: gameEffects, spellHistory: newSh}
		newGames = append(newGames, g)
	}
	// effects before boss's turn
	var resultGames []Game
	for _, g := range newGames {
		var resultEffects []Spell
		playerArmor := 0
		for _, effect := range g.effects {

			g.player.mana += effect.mana
			g.boss.hitPoints -= effect.damage
			playerArmor += effect.armor
			effect.turns -= 1

			if effect.turns > 0 {
				resultEffects = append(resultEffects, effect)
			}
		}
		if g.boss.hitPoints <= 0 {
			resultGames = append(resultGames, Game{winner: "player", player: g.player, manaSpent: g.manaSpent, spellHistory: sh(g.spellHistory)})
			continue
		}
		// boss attacks
		bossDamage := g.boss.damage - playerArmor
		if bossDamage <= 0 {
			bossDamage = 1
		}
		if bossDamage >= g.player.hitPoints {
			resultGames = append(resultGames, Game{winner: "boss", player: g.player, manaSpent: g.manaSpent, spellHistory: sh(g.spellHistory)})
			continue
		}
		resultGames = append(resultGames, Game{player: Player{damage: g.player.damage, hitPoints: g.player.hitPoints - bossDamage, mana: g.player.mana}, boss: g.boss, manaSpent: g.manaSpent, effects: resultEffects, spellHistory: sh(g.spellHistory)})
	}

	return resultGames
}

// 1419 not it
func main() {
	boss := Player{hitPoints: 71, damage: 10}
	player := Player{hitPoints: 50, mana: 500}
	//boss := Player{hitPoints: 14, damage: 8}
	//player := Player{hitPoints: 10, mana: 250}
	var games []Game
	startingGame := Game{player: player, boss: boss, manaSpent: 0, effects: []Spell{}, spellHistory: []Spell{}}
	games = append(games, startingGame)
	ended := false
	for mana := 0; mana < 100; mana++ {
		fmt.Println("Mana: ", mana)
		if len(games) == 0 {
			fmt.Println("No more games")
			break
		} else {
			fmt.Println("Games length: ", len(games))
		}
		var newGames []Game
		for _, game := range games {
			//res := game.newTurn(false) // p1
			res := game.newTurn(true) // p2

			for _, r := range res {

				//fmt.Println(r, r.winner)
				if r.winner == "player" {
					fmt.Printf("Player won with mana %d,\n game: %s\n", r.manaSpent, r)
					ended = true
				}
			}
			newGames = append(newGames, res...)

		}
		if ended {
			os.Exit(0)
		}
		games = newGames
	}
}
