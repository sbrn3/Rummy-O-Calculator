from main import *

class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.tileR1 = Tile("red", 1)
        self.tileR2 = Tile("red", 2)
        self.tileR3 = Tile("red", 3)
        self.tileR4 = Tile("red", 4)
        self.tileB3 = Tile("blue", 3)
        self.tileO3 = Tile("orange", 3)
        self.game = Game()

    def test_valid_set_1(self) -> None:
        """  Create a set with tiles of 3 different colours, same number

        The set should be valid"""
        set1 = Set([self.tileR3, self.tileB3, self.tileO3])
        self.assertTrue(set1.is_valid())

    def test_valid_set_2(self):
        """"Same number, Too many of one colour - Should fail"""
        tile4 = Tile("red", 3)
        set2 = Set([self.tileR3, self.tileB3, self.tileO3, tile4])
        self.assertFalse(set2.is_valid())

    def test_valid_set_3(self):
        """Same number, four different colours - should pass"""
        tile4 = Tile("black", 3)
        set3 = Set([self.tileR3, self.tileB3, self.tileO3, tile4])
        self.assertTrue(set3.is_valid())

    def test_valid_set_4(self):
        """3 numbers in a row, Same colour - Should pass"""
        tile1 = Tile("red", 1)
        tile2 = Tile("red", 2)
        tile3 = Tile("red", 3)
        set4 = Set([tile1, tile2, tile3])
        self.assertTrue(set4.is_valid())

    def test_valid_set_5(self):
        """3 number in a row, Different colour - Should fail"""

        set5 = Set([self.tileR1, self.tileR2, self.tileB3])
        self.assertFalse(set5.is_valid())

    def test_valid_set_6(self):
        """3 numbers in a row, unordered, same colour - Should pass"""
        set6 = Set([self.tileR1, self.tileR3, self.tileR2])
        self.assertTrue(set6.is_valid())

    def test_valid_set_7(self):
        """4 numbers not in a row, same colour - Should fail"""
        set7 = Set([self.tileR1, self.tileR2, self.tileR4])
        self.assertFalse(set7.is_valid())

    def test_combinations(self):
        observed_combinations = self.game.combinations(
            [self.tileR1, self.tileR2,
             self.tileR3,
             self.tileR4], 2)
        theoretical_value = list(itertools.combinations([1, 2, 3, 4],
                                                        2)) + \
                            list(itertools.combinations([1, 2, 3, 4],
                                                        3)) + \
                            list(itertools.combinations([1, 2, 3, 4], 4))
        self.assertEqual(len(theoretical_value), len(observed_combinations))

    def test_add_to_board(self):
        """ Able to add tiles to the board"""
        self.game.add_to_board("red", 4)
        new_tile = Tile("red", 4)
        board_tiles = self.game.get_board().get_tiles()[0]
        self.assertTrue(new_tile == board_tiles)

    def test_add_to_player(self):
        """Able to add tiles to hand"""
        self.game.draw("red", 4)
        self.assertTrue(Tile("red", 4), self.game.get_player().get_hand()[0])

if __name__ == '__main__':
    unittest.main()