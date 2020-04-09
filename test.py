import unittest
import data.player as player
import data.map_generator as dungeon
import data.item as item
import numpy as np


class Map(unittest.TestCase):
    def test_map_generator(self):
        for _ in range(10):
            tiles = [5, 10, 20, 100]
            for tile in tiles:
                new_map = dungeon.Map(tile)
                result = np.reshape(new_map.rooms, -1)
                result = [elem for elem in result if elem is not None]
                self.assertEqual(tile, len(result))

    def test_room(self):
        text = 'test'
        test_room = dungeon.Room(text)
        self.assertEqual('?', str(test_room))
        test_room.visited = True
        self.assertEqual(text, str(test_room))


class Player(unittest.TestCase):
    name = 'Test'
    character = player.Warrior(name)

    def test_create_character(self):
        self.assertEqual(self.name, self.character.name)
        self.assertEqual(self.character.stats['hp'], self.character.stats['max_hp'])
        self.assertEqual(self.character.stats['mana'], self.character.stats['max_mana'])
        self.assertEqual(self.character.stats['strength'], 10)
        self.assertEqual(self.character.stats['dexterity'], 7)
        self.assertEqual(self.character.stats['intelligence'], 5)
        self.assertEqual(self.character.stats['defensive'], 5)

    def test_get_exp(self):
        self.assertEqual(self.character.exp, 0)
        self.assertEqual(self.character.lvl, 1)
        self.character.get_exp(100)
        self.assertEqual(self.character.exp, 100)
        self.assertEqual(self.character.lvl, 2)
        self.assertEqual(self.character.exp_to_next_lvl, 150)
        self.character.get_exp(1000)
        self.assertEqual(self.character.exp, 1100)
        self.assertEqual(self.character.lvl, 7)
        self.assertEqual(self.character.exp_to_next_lvl, 1135)

    def test_hp(self):
        self.character.take_dmg(10)
        self.assertEqual(self.character.stats['hp'], 140)
        self.character.heal(20)
        self.assertEqual(self.character.stats['hp'], 150)
        self.character.take_dmg(160)
        self.assertEqual(self.character.stats['hp'], 1)
        self.character.heal(200)

    def test_creating_item(self):
        player_dmg = 10
        player_str = 5
        stats = {'dmg': ['*', 10], 'strength': ['+', 2]}
        items = item.Item('test', 'first_weapon', stats)
        self.assertEqual('test', str(items))
        first_item_bonus_dmg = items.return_bonus('dmg', player_dmg)
        first_item_bonus_str = items.return_bonus('strength', player_str)
        self.assertEqual(1, first_item_bonus_dmg)
        self.assertEqual(2, first_item_bonus_str)
        stats2 = {'dmg': ['+', 5], 'strength': ['*', 10]}
        item2 = item.Item('test2', 'shield', stats2)
        self.assertEqual('test2', str(item2))
        second_item_bonus_dmg = item2.return_bonus('dmg', player_dmg)
        second_item_bonus_str = item2.return_bonus('strength', player_str)
        self.assertEqual(5, second_item_bonus_dmg)
        self.assertEqual(0.5, second_item_bonus_str)
        self.assertEqual(16, player_dmg+first_item_bonus_dmg+second_item_bonus_dmg)
        self.assertEqual(7.5, player_str + first_item_bonus_str + second_item_bonus_str)

    def test_item_in_player(self):
        self.assertEqual(self.character.stats['hp'], self.character.stats_bonus['hp'])
        self.assertEqual(self.character.stats['max_hp'], self.character.stats_bonus['max_hp'])
        self.assertEqual(self.character.stats['mana'], self.character.stats_bonus['mana'])
        self.assertEqual(self.character.stats['max_mana'], self.character.stats_bonus['max_mana'])
        self.assertNotEqual(self.character.stats['dmg'], self.character.stats_bonus['dmg'])
        self.assertEqual(self.character.stats['defensive'], self.character.stats_bonus['defensive'])
        self.assertNotEqual(self.character.stats['strength'], self.character.stats_bonus['strength'])
        self.assertEqual(self.character.stats['dexterity'], self.character.stats_bonus['dexterity'])
        self.assertEqual(self.character.stats['intelligence'], self.character.stats_bonus['intelligence'])
        self.assertEqual(7, self.character.stats_bonus['dmg'])
        self.assertEqual(11, self.character.stats_bonus['strength'])


if __name__ == '__main__':
    unittest.main()
