from dataclasses import dataclass, field
from typing import List


@dataclass
class Spell:
    cost: int
    damage: int
    duration: int
    active: bool
    mana: int
    name: str
    heal: int
    armor: int
    dead: bool = False

    def run(self):
        if self.active:
            self.duration -= 1
        elif not self.dead:
            self.active = True
        else:
            raise ValueError("Cant run spell")


spells = [
    (53, 4, 1, True, 0, "Magic Missile", 0, 0),
    (73, 2, 1, True, 0, "Drain", 2, 0),
    (113, 0, 6, False, 0, "Shield", 0, 7),
    (173, 3, 6, False, 0, "Poison", 0, 0),
    (229, 0, 5, False, 101, "Recharge"),
]


@dataclass
class Player:
    hit_points: int
    mana_points: int
    active_spells: List[int] = field(default_factory=list)

    def buy_spell(self, spell_args):
        spell = Spell(*spell_args)
        self.mana_points -= spell.cost
        self.active_spells.append(spell)
