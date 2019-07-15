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
            print(
                "Tiles cannot have those values. Try again with valid colours and/or numbers. \n"
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
        self.available_moves = []
        self.deck = []
        for colour in VALID_COLOURS:
            for number in VALID_NUMBERS:
                self.deck.append(Tile(colour, number))

        for i in range(len(self.deck)):
            self.deck.append(self.deck[i])

        for i in range(2):
            self.deck.append(Tile(JOKER[0], JOKER[1]))

    def drawn(self, tile: Tile):
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

    def get_number_of_tiles_on_board(self):
        return len(self.board.get_tiles())

    def view_board(self):
        print(self.board.get_tiles())
        return self.board.get_tiles()

    def get_board(self):
        return self.board

    #
    # Draws (Removes) a tile from the deck which is then placed in the player's hand#
    def draw(self, *args):
        """ args can either be (colour, number) or object Tile
        """
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
    
    def remove_from_board(self, tile : Tile):
        #removes a tile from the board
        #to be used with possible_moves only
        self.get_board().get_tiles().remove(tile)

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
                  "Use: game.view_hand() to view the current tiles in your "
                  "hand\n "
                  "Use: game.draw('colour', number) to add a tile to your "
                  "hand".format(tile))

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
            print("There are no options. Draw a piece from the deck. Using:\n"
                  "game.draw('colour', number)")
        else:
            print("Using the tiles in player hand: {0} \n"
                  "Create the following sets:".format(longest))
            for i in plays[longest][0]:
                print(i)
            return longest, plays[longest][0]

    def best_move_fast(self):
        """Find the longest hand that you can play that will create valid
        sets with the tiles on the board"""
        # Find a valid set from your hand starting from longest to shortest

        # Different hands that you can play from longest to shortest
        maximum_hand_lenth = len(self.player.get_hand())
        for i in range(maximum_hand_lenth, 0, -1):
            hands = itertools.combinations(self.player.get_hand(), i)
            # For each option in those list of hands see if they are able to
            # create valid sets
            for hand in hands:
                play = list(hand) + self.get_board().get_tiles()
                # Find a valid solution for that one play
                solution = self.one_valid_solution(play)


        # return that hand and a list of sets that can be made once you play
        # that hand

    def one_valid_solution(self, tiles: list) -> list:
        """Returns the one valid solution for the list of tiles that is
        entered. The aim is to do as minimal calculations as possible

        TODO Can't be bothered untill I see leo's strategy """
        original_tiles = tiles
        itertools.combinations(original_tiles, 3)
        # Start with one combination. Largest length
        for i in range(len(tiles), 0, -1):
            potential_sets = itertools.combinations(original_tiles)
            for set in potential_sets:
                pass




        # If that combination an create a valid set then remove those tiles
        # from the list

        # create combinations of the remain tiles and repeat.

        # If none of the combinations can make a valid set then this is not a
        # valid solution

        # If the number of tiles remaining reaches 0 then this is a valid
        # solution. Return the pathway for this as the final answer.



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
    def combinations_delthis(tiles: [], minimum_length):
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

    @staticmethod
    def combinations(tiles, minimum_length):
        res = []
        for L in range(minimum_length, len(tiles) + 1):
            for subset in itertools.combinations(tiles, L):
                res.append(list(subset))
        return res

    def list_duplicate_tiles(self):
        #returns a list of tiles that their duplicate also presents on the board
        res = []
        board = self.board.get_tiles()
        for i in board:
            if board.count(i) > 1 and i not in res:
                res.append(i)
        return res

    def possible_tile_combinations_on_board(self):
        # max_set_length = len(self.board.get_tiles())
        set_length = 3
        test_list = self.board.get_tiles().copy()
        if len(test_list) < 3:
            return []
        coms = Game.combinations(test_list, set_length)
        coms_cp = coms.copy()
        for i in coms_cp:
            if not Set(i).is_valid():
                coms.remove(i)
        return coms

    def possible_set_combinations_on_board(self):
        dup_list = self.list_duplicate_tiles()
        combs = self.possible_tile_combinations_on_board()
        #groups possible combinations on the board, if they use up all the tiles available, there's a possible move
        mix = Game.combinations(combs, 2)
        mix_cp = mix.copy()
        #discards combinations of sets that involve the same tile with no duplicate on the board twice
        for i in mix_cp:
            flag = False
            for j in range(len(i) - 1):
                dup = set(i[j]).intersection(set(i[j+1]))
                if len(dup) > 0:
                    for k in dup:
                        if k not in dup_list:
                            flag = True
                            break
            if flag:
                mix.remove(i)
                continue
        #copies the updated list
        mix_cp = mix.copy()
        #discards combinations of sets that don't use up all the tiles present on the board
        for i in mix_cp:
            mix_len = 0
            for j in i:
                mix_len += len(j)
            if mix_len != self.get_number_of_tiles_on_board():
                mix.remove(i)
        return mix

    def possible_moves(self):
        """bool whether there is any available moves can be made from player's hand
            possible moves are then stored in self.possible_moves"""
        res = []
        hand = self.get_player().get_hand()
        if len(hand) == 0:
            print("Player's hand is empty")
            raise ValueError()
        for i in hand:
            self.add_to_board(i)
            sol = self.possible_set_combinations_on_board()
            if len(sol) != 0:
                res.extend(sol)
            else:
                self.remove_from_board(i)
        if len(res) != 0:
            self.possible_moves = res
        else:
            return False
        return True

    def get_possible_moves(self):
        if self.possible_moves():
            return self.possible_moves


    @staticmethod
    def generate_random_tile():
        """Generates and returns a random tile"""
        colour_index = random.randrange(3)
        number_index = random.randrange(1, 13)
        return Tile(VALID_COLOURS[colour_index], number_index)


if __name__ == '__main__':
    game = Game()
    tile_list = []
    for i in range(1, 4):
        game.add_to_board(Tile("red", i))
        game.add_to_board(Tile("blue", i))
        game.add_to_board(Tile("orange", i))
    game.add_to_board(Tile("blue",4))
    # game.add_to_board(Tile("blue",4))
    game.draw("blue", 5)
    print(game.get_possible_moves())

    # s = Set([Tile("red", 1), Tile("blue", 1), Tile("blue", 2)])
    # print(s.is_valid())


