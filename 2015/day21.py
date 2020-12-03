"""
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

from typing import NamedTuple


class Inventory:
    def __init__(self, items):
        self.ring1 = None
        self._armor = None
        self.ring2 = None
        for item in items:
            if isinstance(item, Weapon):
                self.weapon = item
            elif isinstance(item, Armor):
                self._armor = item
            elif isinstance(item, Ring):
                if not self.ring1:
                    self.ring1 = item
                else:
                    self.ring2 = item

    @property
    def names(self):
        return tuple(
            sorted(
                [
                    k.name
                    for k in (self.ring1, self._armor, self.ring2, self.weapon)
                    if k
                ]
            )
        )

    @property
    def not_null(self):
        return [k for k in (self.ring1, self._armor, self.ring2, self.weapon) if k]

    @property
    def damage(self):
        return sum(k.damage for k in self.not_null)

    @property
    def armor(self):
        return sum(k.armor for k in self.not_null)

    def __repr__(self):
        return f"{self.names}"

    def __eq__(self, other):
        return self.names == other.names

    def __hash__(self):
        return hash(self.names)


class Weapon(NamedTuple):
    name: str
    cost: int
    damage: int
    armor: int


class Armor(NamedTuple):
    name: str
    cost: int
    damage: int
    armor: int


class Ring(NamedTuple):
    name: str
    cost: int
    damage: int
    armor: int


rings = [
    Ring(name, int(cost), int(damage), int(armor))
    for name, cost, damage, armor in [
        ("Damage +1,25,1,0".split(",")),
        ("Damage +2,50,2,0".split(",")),
        ("Damage +3,100,3,0".split(",")),
        ("Defense +1,20,0,1".split(",")),
        ("Defense +2,40,0,2".split(",")),
        ("Defense +3,80,0,3".split(",")),
    ]
]

weapons = [
    Weapon(name, int(cost), int(damage), int(armor))
    for name, cost, damage, armor in [
        ("Dagger,8,4,0".split(",")),
        ("Shortsword,10,5,0".split(",")),
        ("Warhammer,25,6,0".split(",")),
        ("Longsword,40,7,0".split(",")),
        ("Greataxe,74,8,0".split(",")),
    ]
]

armors = [
    Armor(name, int(cost), int(damage), int(armor))
    for name, cost, damage, armor in [
        ("Leather,13,0,1".split(",")),
        ("Chainmail,31,0,2".split(",")),
        ("Splintmail,53,0,3".split(",")),
        ("Bandedmail,75,0,4".split(",")),
        ("Platemail,102,0,5".split(",")),
    ]
]


def get_inventories(gold):
    inventories = []
    for weapon in weapons:
        if weapon.cost <= gold:
            rings_gold = gold - weapon.cost
            for ring in rings:
                if ring.cost <= rings_gold:
                    invs_with_ring = get_inventories_ring(
                        rings_gold - ring.cost, [weapon, ring]
                    )
                else:
                    invs_with_ring = []
                invs_without_ring = get_inventories_ring(rings_gold, [weapon])

                inventories.extend(invs_with_ring)
                inventories.extend(invs_without_ring)
    return set([Inventory(inv) for inv in inventories])


def get_inventories_ring(gold, items):
    res = []
    for ring in rings:
        if ring not in items:
            if ring.cost <= gold:
                invs_with_ring = get_inventories_armor(
                    gold - ring.cost, list(items) + [ring]
                )
            else:
                invs_with_ring = []
            invs_without_ring = get_inventories_armor(gold, list(items))

            res.extend(invs_with_ring)
            res.extend(invs_without_ring)
    return res


def get_inventories_armor(gold, items):
    res = [items]
    for armor in armors:
        if armor.cost <= gold:
            res.append(list(items) + [armor])

    return res


"""
Hit Points: 109
Damage: 8
Armor: 2
"""


class Boss(NamedTuple):
    damage: int
    hp: int
    armor: int


PLAYER_HP = 100


def win(inventory, boss):
    eff_boss_damage = max(inventory.damage - boss.armor, 1)
    eff_player_damage = max(boss.damage - inventory.armor, 1)
    boss_hp = boss.hp
    player_hp = PLAYER_HP
    for i in range(boss.hp):
        boss_hp = boss_hp - eff_boss_damage
        if boss_hp <= 0:
            return True
        player_hp = player_hp - eff_player_damage
        if player_hp <= 0:
            return False


gold = 0
boss = Boss(8, 109, 2)
won = False
used = set()
while not won:
    gold += 1
    invs = get_inventories(gold)
    total_invs = len(invs)
    won_invs = 0
    for inventory in invs:
        if inventory not in used:
            used.add(inventory)
        else:
            continue
        if win(inventory, boss):
            won = True
            break

print(gold)

glold = 0
boss = Boss(8, 109, 2)
used = set()
while True:
    gold += 1
    print(gold)
    invs = get_inventories(gold)
    total_invs = len(invs)
    new_invs = 0
    lost_inv = 0
    for inventory in invs:
        if inventory in used:
            continue
        else:
            new_invs += 1
            used.add(inventory)
        if win(inventory, boss):
            continue
        else:
            lost_inv += 1
    if lost_inv == 0 and gold > 111:
        print(f"all wins  with gold {gold} and {total_invs}")
    elif lost_inv > 0 and gold > 111:
        print(f"one lost at {gold}")
    if new_invs == 0 and gold > 111:
        break
