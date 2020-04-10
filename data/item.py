class Item:
    requirements = {
            'lvl': 0,
            'strength': 0,
            'dexterity': 0,
            'intelligence': 0,
        }

    def __init__(self, name=None, inv_type=None, stats=None, requirements=None):
        self.name = name
        self.inv_type = inv_type
        # stats = {'name': ['type','value']} stats ={'hp':['*',10]}
        # if *, second value is %, if we give 10, this is 10% more
        self.stats = stats
        if requirements is not None:
            for id_req, item in requirements.items():
                self.requirements[id_req] = item

    def return_bonus(self, bonus_name, bonus_value):
        if self.name is not None and bonus_name in self.stats:
            if self.stats[bonus_name][0] == '+':
                return self.stats[bonus_name][1]
            elif self.stats[bonus_name][0] == '*':
                return self.stats[bonus_name][1]*bonus_value/100
        return 0

    def __str__(self):
        return self.name
