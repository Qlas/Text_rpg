import unittest
import data.player as player
import data.map_generator as dungeon
import numpy as np


class Map(unittest.TestCase):
    def test_map_generator(self):
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
        self.assertEqual(self.character.hp, self.character.hp_max)
        self.assertEqual(self.character.mana, self.character.mana_max)
        self.assertEqual(self.character.strength, 10)
        self.assertEqual(self.character.dexterity, 7)
        self.assertEqual(self.character.intelligence, 5)
        self.assertEqual(self.character.defensive, 5)

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
        self.assertEqual(self.character.hp, 140)
        self.character.heal(20)
        self.assertEqual(self.character.hp, 150)
        self.character.take_dmg(160)
        self.assertEqual(self.character.hp, 1)
        self.character.heal(200)


if __name__ == '__main__':
    unittest.main()
