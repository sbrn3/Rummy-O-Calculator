import itertools
import math
import unittest
import random

VALID_COLOURS = ["red", "black", "blue", "orange"]
VALID_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
MAX_TILE_NUMBERS = 104
JOKER = ["joker", 0]



class Tile:
    def __init__(self, colour: str, number: int):
        if colour in VALID_COLOURS and number in VALID_NUMBERS:
            self._colour = str(colour)
            self._number = int(number)
        elif colour is JOKER[0] and number is JOKER[1]:
            self._colour = JOKER[0]
            self._number = JOKER[1]
        else:
            print("Tiles cannot have those values. Try again with valid colours and/or numbers. \n"
                  "The correct values are \n"
                  "colours: {0} \n"
                  "numbers: {1}".format(VALID_COLOURS, VALID_NUMBERS)
                  )  # ask to input again
            raise ValueError()

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
        try:
            self.tiles.append(tile)
        except ValueError:
            pass


class Player:
    def __init__(self):
        self.tiles = []

    def __str__(self):
        return self.tiles

    def add_tile(self, tile: Tile):
        try:
            self.tiles.append(tile)
        except ValueError:
            pass

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

class Deck:
    def __init__(self):
        self.deck = []
        for colour in VALID_COLOURS:
            for number in VALID_NUMBERS:
                self.deck.append(Tile(colour, number))
        
        for i in range(len(self.deck)):
            self.deck.append(self.deck[i])

        for i in range(2):
            self.deck.append(Tile(JOKER[0], JOKER[1]))
    
    def drawn(self, tile : Tile):
        return self.deck.remove(tile)


class Game:
    def __init__(self):
        self.board = Board()
        self.player = Player()
        self._valid_sets = {}
        self.deck = Deck()

    def __str__(self):
        return self.player.get_hand()

    def get_player(self):
        return self.player

    def view_hand(self):
        print(self.player.get_hand())
        return self.player.get_hand()

    def view_board(self):
        print(self.board.get_tiles())
        return self.board.get_tiles()

    def get_board(self):
        return self.board

    #
    # Draws (Removes) a tile from the deck which is then placed in the player's hand#
    def draw(self, *args):
        if len(args) == 2:
            try:
                tile = Tile(args[0], args[1])
            except ValueError:
                pass
        else:
            tile = args[0]
        self.player.add_tile(tile)
        self.deck.drawn(tile)
        print("Tile " + str(tile) + " is drawn")


    #
    # Places a tile, which is not on the player's hand, on the board
    # This method can either takes (colour, number) to build a tile, or a Tile object#
    def add_to_board(self, *args):
        if len(args) == 2:
            try:
                tile = Tile(args[0], args[1])
            except ValueError:
                pass
        else:
            tile = args[0]
        self.board.add_tile(tile)
        print("Tile " + str(tile) + " is placed on the board")
        

    # duplicated method
    # def add_tile_to_board(self, tile: Tile):
    #     self.board.add_tile(tile)

    # Places a tile from player's hand on the board, the tile is then removed from the hand
    def play(self, colour: str, number: int):
        try:
            tile = Tile(colour, number)
        except ValueError:
            return
        if tile in self.get_player().get_hand():
            self.get_player().get_hand().remove(tile)
            self.add_to_board(tile)
        else:
            print("The tile {0} does not appear to be in your hand\n"
                  "Use: game.view_hand() to view the current tiles in your hand \n "
                  "Use: game.draw('colour', number) to add a tile to your hand".format(tile))

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
        print(pathways)
        print("over")
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
            next_sets = Game.organise_sets(solution[1])
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
        print(valid_solutions)
        return valid_solutions
        # print out the valid sets which contain the largest number of your
        # tiles in them

    def best_move(self):
        plays = self.valid_sets_from_hand()
        longest = []
        for key in plays:
            if len(key) > len(longest):
                longest = key
        if len(longest) == 0:
            print("There are no options. Draw a piece from the deck. Using: " \
                  "\n " \
                  "game.draw('colour', number)")
        else:
            print("Using the tiles in player hand: {0} \n"
                  "Create the following sets:".format(longest))
            for i in plays[longest][0]:
                print(i)
            return longest, plays[longest][0]

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

    def arrange_board(self):
        max_set_length = len(self.board.get_tiles())
        success = False
        arrangement = []
        test_list = []
        while max_set_length > 0:
            for i in self.board.get_tiles():
                test_list.append(i)
                test_list.extend(self.board.get_tiles()[i+1:])
                coms = combinations(test_list, max_set_length)

                for j in coms:
                    s = Set(j)
                    if s.is_valid():
                        arrangement.append(s)
                        new_test_list = test_list.copy()
                        for k in s:
                            new_test_list.remove(s)
                    else:
                        coms.remove(j)

    @staticmethod
    def generate_random_tile():
        """Generates and returns a random tile"""
        colour_index = random.randrange(3)
        number_index = random.randrange(1,13)
        return Tile(VALID_COLOURS[colour_index], number_index)

if __name__ == '__main__':
    game = Game()
    tile_list = []
    # for i in range(15):
    #     tile = generate_random_tile()
    #     tile_list.append(tile)
    #     game.add_to_board(tile)
    # for i in range(7):
    #     tile = generate_random_tile()
    #     game.draw(tile)    
    # game.valid_sets_from_hand()
    for i in range(1,4):
        tile_list.append(Tile("red", i))
        tile_list.append(Tile("blue", i))
        tile_list.append(Tile("orange", i))
    res = game.combinations(tile_list, 3)

