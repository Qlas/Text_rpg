class Player:
    lvl = 1
    exp = 0
    exp_to_next_lvl = 100
    gold = 1000
    eq = {
        'helmet': 0,
        'armor': 0,
        'gloves': 0,
        'legs': 0,
        'boots': 0,
        'first_weapon': 0,
        'second_weapon': 0

    }
    spell_book = {}
    location = 'Village'
    inventory = {}

    def __init__(self, name, hp, mana, defensive, strength, dexterity, intelligence):
        self.name = name
        self.hp = 100 + hp
        self.hp_max = self.hp
        self.mana = 10 + mana
        self.mana_max = self.mana
        self.dmg = 5
        self.defensive = 5 + defensive
        self.strength = 5 + strength
        self.dexterity = 5 + dexterity
        self.intelligence = 5 + intelligence

    def return_stat(self):
        pass

    def wear_item(self):
        pass

    def take_off_item(self):
        pass

    def dead(self):
        pass

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 1
            self.dead()

    def heal(self, heal):
        self.hp += heal
        if self.hp > self.hp_max:
            self.hp = self.hp_max

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
                         strength=strength, dexterity=dexterity, intelligence=intelligence)

    def __str__(self):
        return 'Warrior'
