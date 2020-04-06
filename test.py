import unittest
import data.player as player


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
