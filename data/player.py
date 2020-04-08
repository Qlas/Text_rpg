import data.item as item
import copy

class Player:
    lvl = 1
    exp = 0
    exp_to_next_lvl = 100
    gold = 1000
    eq = {
        'helmet': None,
        'armor': None,
        'gloves': None,
        'legs': None,
        'boots': None,
        'first_weapon': None,
        'second_weapon': None

    }
    spell_book = {}
    location = 'Village'
    inventory = {}

    def __init__(self, name, hp, mana, defensive, strength, dexterity, intelligence, max_item_in_inventory):
        self.name = name
        self.stats = {
            'hp': 100 + hp,
            'max_hp': 100 + hp,
            'mana': 10 + mana,
            'max_mana': 10 + mana,
            'dmg': 5,
            'defensive': 5 + defensive,
            'strength': 5 + strength,
            'dexterity': 5 + dexterity,
            'intelligence': 5 + intelligence
        }
        self.max_item_in_inventory = max_item_in_inventory
        self.stats_bonus = copy.deepcopy(self.stats)
        self.stats_math()

    def stats_math(self):
        for stat_name, stat_value in self.stats.items():
            stat_sum = stat_value
            for eq_name, eq_value in self.eq.items():
                if eq_value is not None:
                    stat_sum += eq_value.return_bonus(stat_name, stat_value)
            self.stats_bonus[stat_name] = stat_sum

    def wear_item(self):
        pass

    def take_off_item(self):
        pass

    def dead(self):
        pass

    def take_dmg(self, dmg):
        self.stats['hp'] -= dmg
        if self.stats['hp'] <= 0:
            self.stats['hp'] = 1
            self.dead()

    def heal(self, heal):
        self.stats['hp'] += heal
        if self.stats['hp'] > self.stats['max_hp']:
            self.stats['hp'] = self.stats['max_hp']

    def lvl_up(self):
        self.lvl += 1
        self.exp_to_next_lvl = int(self.exp_to_next_lvl * 1.5)

    def get_exp(self, exp):
        self.exp += exp
        while self.exp >= self.exp_to_next_lvl:
            self.lvl_up()


class Warrior(Player):
    def __init__(self, name, hp=50, mana=0, defensive=0, strength=5, dexterity=2, intelligence=0):
        super().__init__(name=name, hp=hp, mana=mana, defensive=defensive,
                         strength=strength, dexterity=dexterity, intelligence=intelligence, max_item_in_inventory=10)
        stats = {'dmg': ['+', 2], 'strength': ['*', 10]}
        self.eq['helmet'] = item.Item('Training sword', 'first_weapon', stats)
        self.stats_math()

    def __str__(self):
        return 'Warrior'
