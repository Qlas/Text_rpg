class Enemy:
    stats = {
        'hp': 0,
        "max_hp": 100,
        'defensive': 0,
        'dmg': 0
    }
    def __init__(self, player_lvl):
        self.enemy_lvl = player_lvl
        self.generate_stats()

    def generate_stats(self):
        self.stats['max_hp'] = self.enemy_lvl * 50
        self.stats['hp'] = self.stats['max_hp']
        self.stats['defensive'] = self.enemy_lvl
        self.stats['dmg'] = self.enemy_lvl

    def dead(self):
        pass

    def take_dmg(self, dmg):
        self.stats['hp'] -= dmg
        if self.stats['hp'] <= 0:
            self.stats['hp'] = 1
            self.dead()
