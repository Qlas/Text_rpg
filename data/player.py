import data.item as item
import copy


class Player:
    exp = 0
    exp_to_next_lvl = 100
    gold = 1000
    # player actual eq
    eq = {
        'helmet': item.Item(),
        'armor': item.Item(),
        'gloves': item.Item(),
        'legs': item.Item(),
        'boots': item.Item(),
        'first_weapon': item.Item(),
        'second_weapon': item.Item()

    }
    spell_book = {}
    location = 'Village'
    # player inventory system, need to improve it
    inventory = {}

    def __init__(self, name, hp, mana, defensive, strength, dexterity, intelligence, max_item_in_inventory):
        self.name = name
        # set player stats depends on player class
        self.stats = {
            'lvl': 1,
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
        # temporary inv system
        self.max_item_in_inventory = max_item_in_inventory
        # stats_bonus is stats after add bonus from items, spells
        self.stats_bonus = copy.deepcopy(self.stats)
        # math this stats
        self.stats_math()
        self.dung = None

    def stats_math(self):
        # for every stats
        for stat_name, stat_value in self.stats.items():
            # stat_sum is value with bonuses, starting from base value
            stat_sum = stat_value
            # for every items
            for eq_name, eq_value in self.eq.items():
                if eq_value is not None:
                    stat_sum += eq_value.return_bonus(stat_name, stat_value)
            self.stats_bonus[stat_name] = stat_sum

    def wear_item(self, w_item):
        """
        :param w_item: get item which we want to wear
        """
        if self.eq[w_item.inv_type].name is None:

            if all(self.stats[requirements_id] >= requirements_value
                   for requirements_id, requirements_value in w_item.requirements.items()):
                self.eq[w_item.inv_type] = w_item
        else:
            return w_item

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
        self.stats['lvl'] += 1
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
        self.eq['first_weapon'] = item.Item('Training sword', 'first_weapon', stats)
        self.stats_math()

    def __str__(self):
        return 'Warrior'
