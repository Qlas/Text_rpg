import random
import numpy as np
import data.item
import data.player
import math


def generate_money(player):
    return int(np.random.triangular(1000, 1000, 10000*player.stats['lvl']))


def generate_random_item(player):
    names = ['Training', 'Steel', 'Brutal', 'Fire', 'Obsidian']
    requirements = {
            'lvl': 0,
            'strength': 0,
            'dexterity': 0,
            'intelligence': 0,
        }
    stats = {

    }
    lvl = player.stats['lvl']
    # every item bonus to dmg if weapon, def if defensive part, 1 more bonus if amulet, rings
    # common - 1 - 0 bonus
    # uncommon - 2 - 1 bonus
    # Rare - 3 - 2 bonus
    # Epic - 4 - 2 bonus
    # Ultimate - 5 - 3 bonus
    rarity = np.random.choice(
        [1, 1.5, 2, 2.5, 3],
        1,
        p=[0.5, 0.25, 0.15, 0.07, 0.03]  # probability
    )
    items = ['helmet', 'armor', 'gloves', 'legs', 'boots', 'first_weapon', 'second_weapon']
    item_type = np.random.choice(
        items,
        1)
    if item_type == 'first_weapon':
        dmg = math.ceil(rarity * random.random() * 5)
        stats['dmg'] = ['+', dmg]
    else:
        defensive = math.ceil(rarity * random.random() * 5)
        stats['defensive'] = ['+', defensive]

    stats_cap = ['max_hp', 'max_mana', 'strength', 'dexterity', 'intelligence']
    x = ['+', '*']
    if rarity == 3:
        while len(stats) != 4:
            bonus = random.choice(stats_cap)
            if bonus not in stats:
                typ = random.choice(x)
                if typ == '+':
                    bonus_value = math.ceil(rarity * random.random())
                else:
                    bonus_value = math.ceil(rarity * random.uniform(0, 10))
                stats[bonus] = [typ, bonus_value]
    elif rarity == 2.5 or rarity == 2:
        while len(stats) != 3:
            bonus = random.choice(stats_cap)
            if bonus not in stats:
                typ = random.choice(x)
                if typ == '+':
                    bonus_value = math.ceil(rarity * random.random())
                else:
                    bonus_value = math.ceil(rarity * random.uniform(0, 10))
                stats[bonus] = [typ, bonus_value]
    elif rarity == 1.5:
        while len(stats) != 2:
            bonus = random.choice(stats_cap)
            if bonus not in stats:
                typ = random.choice(x)
                if typ == '+':
                    bonus_value = math.ceil(rarity * random.random())
                else:
                    bonus_value = math.ceil(rarity * random.uniform(0, 10))
                stats[bonus] = [typ, bonus_value]
    requirements['lvl'] = lvl
    new_item = data.item.Item(f'{random.choice(names)} {item_type[0]}', item_type, stats, requirements)
    return new_item
