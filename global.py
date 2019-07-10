import itertools
import math
import unittest

VALID_COLOURS = ["red", "black", "blue", "orange"]
VALID_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


class Tile:
    def __init__(self, colour: str, number: int):
        if colour in VALID_COLOURS and number in VALID_NUMBERS:
            self._colour = str(colour)
            self._number = int(number)
        else:
            print("Try again with valid colours")  # ask to input again

    def get_colour(self):
        return self._colour

    def get_number(self):
        return self._number

    def get_info(self):
        return self._colour, self._number

    def __str__(self):
        return "({0}, {1})".format(self._colour, self._number)

    def __repr__(self):
        return "({0}, {1})".format(self._colour, self._number)

    def __eq__(self, other) -> bool:
        """
        Compare if two tiles have the same values
        :param other: Other tile you are comparing to
        :return: If values on tiles are equal
        """
        other_colour = str(other.get_colour())
        self_colour = str(self.get_colour())
        if other_colour == self_colour and int(other.get_number()) \
                == int(self.get_number()):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.get_colour(), self.get_number()))


class Board:
    def __init__(self):
        self.tiles = []

    def __str__(self):
        return self.tiles

    def get_tiles(self):
        return self.tiles

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)


class Player:
    def __init__(self):
        self.tiles = []

    def __str__(self):
        return self.tiles

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def remove_tile(self, tile: Tile):
        self.tiles.remove(tile)

    def get_hand(self):
        return self.tiles

    def get_tile(self, i):
        return self.tiles[i]


class Set:
    def __init__(self, tiles):
        self.tiles = []
        self.argv = tiles
        # if len(argv) >= 3:
        #     if self.is_valid():
        #         for arg in self.argv:
        #             self.tiles.append(arg)
        #     else:
        #         print("Init failed")
        # else:
        #     print("not enough\n")  # ask to re input

    def is_valid(self):
        if len(self.argv) < 3:
            return False
        # same colour all in a row
        if self.same_colour():
            if self.in_order():
                return True
        # different colour for 3 or 4 tiles. Cannot repeat colours.
        elif self.same_number():
            return True
        return False

    def same_colour(self):
        colour = self.argv[0].get_colour()
        for i in self.argv:
            if i.get_colour() != colour:
                return False
        return True

    def same_number(self):
        number = self.argv[0].get_number()
        colour = []
        for i in self.argv:
            com = i.get_number()
            argv_colour = i.get_colour()
            if argv_colour in colour:
                return False
            if com != number:
                return False
            colour.append(argv_colour)

        return True

    def in_order(self):
        l = []
        for i in self.argv:
            l.append(i.get_number())
        l.sort()
        number = l[0]
        for i in l[1:]:
            if i != number + 1:
                return False
            number = i
        return True

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def my_sets(self):
        return self.tiles

    def __str__(self):
        l = ""
        for i in self.tiles:
            l += i.__str__()
            if i is not self.tiles[-1]:
                l += ","
        return l


class Game:
    def __init__(self):
        self.board = Board()
        self.player = Player()
        self._valid_sets = {}

    def __str__(self):
        return self.player.get_hand()

    def get_player(self):
        return self.player

    def get_board(self):
        return self.board

    def draw(self, colour, number):
        tile = Tile(colour, number)
        self.player.add_tile(tile)

    def add_to_board(self, colour: str, number: int):
        tile = Tile(colour, number)
        self.board.add_tile(tile)

    def add_tile_to_board(self, tile: Tile):
        self.board.add_tile(tile)

    @staticmethod
    def number_of_tiles_used(set_list: list):
        """ Returns the number of tiles used to form the entered solution"""
        count = 0
        for tile_set in set_list:
            count += len(tile_set)
        return count

    @staticmethod
    def valid_solutions(tiles: list):
        """Returns a list of actually valid sets."""
        pathways = Game.set_pathways(tiles)
        potential_solutions = Game.organise_sets(pathways)
        output = []
        for solution in potential_solutions:
            if len(tiles) == Game.number_of_tiles_used(solution):
                output.append(solution)
        return output

    @staticmethod
    def set_pathways(tiles: list) -> list:
        """Forms valid sets based on the tiles that are entered

        :return: potential sets
        :param tiles: List of lists of tiles.
        """
        # For every combination in tiles that is 3 or greater.
        output = []
        potential_sets = Game.combinations(tiles, 3)
        original_tiles = tiles
        for combination in potential_sets:
            # if combination does not make a valid set. continue
            potential_set = Set(combination)
            tiles_2 = original_tiles.copy()
            if not potential_set.is_valid():
                continue
            # List for that valid combination
            combination_list = [combination]
            # remove tiles from list of tiles
            for tile in combination:
                tiles_2.remove(tile)
            # get potential sets from list of tiles
            combination_list.append(Game.set_pathways(tiles_2))
            output.append(combination_list)
        # repeat until there are no tiles left or there is a remainder
        return output

    @staticmethod
    def organise_sets(set_pathway: list) -> list:
        """
        Takes in the set pathway produced from set_pathways method and
        organises them into a list of valid solutions. In the format:
        
        [ solution 1, solution 2, solution 3 ]

        Where each solution is a list of sets. And a set is a list of tiles.

        :param set_pathway:
        :return: List of solutions
        """
        # create a copy of the outermost set based on the number of sets one
        # inside
        output = []
        if len(set_pathway) == 0:
            return [[]]
        for solution in set_pathway:
            next_sets = game.organise_sets(solution[1])
            for i in next_sets:
                output.append([solution[0]] + i)
        return output

    def valid_sets_from_hand(self):
        valid_solutions = {}
        plays = Game.combinations(self.player.get_hand(), 1)
        # for every combination probability of your own tiles
        # form valid sets from those tiles
        for hand in plays:
            test = hand + self.board.get_tiles()
            solutions = self.valid_solutions(test)
            if len(solutions) > 0:
                valid_solutions[tuple(hand)] = tuple(solutions)
        return valid_solutions
        # print out the valid sets which contain the largest number of your
        # tiles in them

    def best_move(self):
        plays = game.valid_sets_from_hand()
        longest = []
        for key in plays:
            if len(key) > len(longest):
                longest = key
        if len(longest) == 0:
            print("There are no options. Draw a piece from the deck. Use: " \
                   "\n " \
                   "game.draw('colour', number)")
        else:
            print((longest, plays[longest][0]))
            print("Tiles from play: {0} \n"
                  "")


    @staticmethod
    def item_at_index(index_list: [], target_list: []):
        """
        Returns the item at the positions in the index_list

        Index list has to be in the format e.g. [0, 1, 2, 3]

        Where the numbers in the list are the indexes of the target items.
        :param index_list: List of target indexes
        :param target_list:
        :return: List of items at the indexes of he
        """
        set = []
        for index in index_list:
            set.append(target_list[index])
        return set

    @staticmethod
    def combinations(tiles: [], minimum_length):
        """
        Returns a list of every combination, from the minimum length
        :param minimum_length: minimum length of combinations
        :param tiles: List of all the items you want to find combinations of
        :return: List of all the combinations. Of all sizes. Starting at the
        minimum length.
        """
        output = []
        maximum_length = len(tiles)
        if minimum_length > maximum_length:
            return []
        for choose in range(minimum_length, maximum_length + 1):  # check + 1
            # combination function
            index_list = []
            for j in range(0, choose):
                index_list.append(j)
            final_possible_index = maximum_length - 1
            index_of_interest = index_list[len(index_list) - 1]
            while True:
                # if index list is -1 then you have finished
                if index_of_interest == -1:
                    break
                # Start by looking at the last index
                index_of_interest = len(index_list) - 1
                output.append(Game.item_at_index(index_list, tiles))
                while True:
                    # if it is pointing to the last tile or one less than the
                    # tile after it . look at the index before it
                    if index_of_interest == -1:
                        break
                    try:
                        after_index = index_list[index_of_interest + 1]
                    except IndexError:
                        after_index = final_possible_index + 1
                    if index_list[index_of_interest] == final_possible_index or \
                            index_list[index_of_interest] == (after_index - 1):
                        index_of_interest -= 1

                        # if the one before it is out of range then you have
                        # reached the last combination

                    # else increase the index you are looking at by one
                    else:
                        index_list[index_of_interest] += 1

                        # make all subsequent indexes increase by one
                        for i in range(index_of_interest, len(index_list) - 1):
                            index_list[i + 1] = index_list[i] + 1
                        break
        return output


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
    # unittest.main()

    game = Game()

    print("create valid sets")
    game.add_to_board("blue", 1)
    game.add_to_board("blue", 2)
    game.add_to_board("blue", 3)

    print("\ncreate valid sets from a list of tiles- should return two valid "
          "hands")
    game.add_to_board("red", 4)
    game.add_to_board("red", 5)
    game.add_to_board("red", 6)
    game.add_to_board("black", 7)
    game.draw("orange", 7)
    game.draw("blue", 7)
    print("tiles on the board: {0} \n".format(game.board.get_tiles()))
    valid_set_test = game.set_pathways(game.board.get_tiles())
    # for i in valid_set_test:
    #     print(i)
    #     for j in i[1]:
    #         print(j)
    #         for k in j[1]:
    #             print(k)
    #     print()

    print("organise output")
    organised_sets = Game.organise_sets(valid_set_test)
    print(organised_sets)
    print()
    for i in organised_sets:
        print(i)
    print()

    print("valid sets")
    valid_sets = game.valid_solutions(game.get_board().get_tiles())
    for i in valid_sets:
        print(i)

    print("\nvalid solutions from hand")
    # game.draw("red", 6)
    print("valid sets")
    valid_sets = game.valid_solutions(game.get_board().get_tiles())
    for i in valid_sets:
        print(i)
    game.valid_sets_from_hand()

    print("\n best move")
    game.best_move()


    # print("\n create no possible valid list from tiles")
    # game.add_to_board("orange", 1)
    # valid_set_test = game.set_pathways(game.board.get_tiles())
    # for i in valid_set_test:
    #     print(i)
    # g = Game()
    # g.draw("red", 5)
    # g.add_to_board("red", 5)
    # print(g.me.get_hand())
    # print(g.board.get_tiles())
