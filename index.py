import sys
import os

class Player:
    lvl = 1
    exp = 0
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

    def __init__(self, name, hp, hp_max, mana, mana_max, dmg, defensive, strength, dexterity, intelligence):
        self.name = name
        self.hp = hp
        self.hp_max = hp_max
        self.mana = mana
        self.mana_max = mana_max
        self.dmg = dmg
        self.defensive = defensive
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence

    def show_stat(self):
        pass

    def wear_item(self):
        pass

    def take_off_item(self):
        pass

    def take_dmg(self):
        pass

    def heal(self):
        pass


def new():
    pass

def load():
    pass

def title_screen():
    print('#' * 100)
    print(' ' * 36, 'Welcome in RPG adventure.', ' ' * 36)
    print('#' * 100)
    print(' ' * 42, '.: New Game :.', ' ' * 42)
    print(' ' * 44, '.: Load :.', ' ' * 44)
    print(' ' * 44, '.: Quit :.', ' ' * 44,)
    option = ''
    while option not in ['new', 'new game', 'load', 'quit']:
        option = input("> ").lower()
        if option == 'new' or option == 'new game':
            new()
        elif option == 'load':
            load()
        elif option == 'quit':
            sys.exit()

os.system('mode con: cols=100 lines=30')
title_screen()
