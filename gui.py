import tkinter as tk
from main import VALID_NUMBERS, VALID_COLOURS, Game
import webbrowser


class Rummy(tk.Tk):
    def __init__(self):
        super(Rummy, self).__init__()

        # Initialise a game

        self.game = Game()
        # Member Variables
        self.number = tk.IntVar(self)
        self.number.set(VALID_NUMBERS[0])
        self.colour = tk.StringVar(self)
        self.colour.set(VALID_COLOURS[0])
        self.title_size = 14
        # window dimensions
        self.geometry("1000x500")

        # Create title
        self.title("Rummy-O Calculator")

        # Create Menus
        root_menu = tk.Menu(self)
        self.config(menu=root_menu)

        file_menu = tk.Menu(root_menu)
        root_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reset Game", command=self.reset_game)
        file_menu.add_command(label="Refresh Screen", command=self.refresh)
        file_menu.add_command(label="Exit", command=self.quit)

        help_menu = tk.Menu(root_menu)
        root_menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Open Instructions",
                              command=self.open_instructions)

        # Create Main Frames
        self.left_frame = tk.Frame(self, height=500)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ## Left side of the screen

        self.l1 = tk.Frame(self.left_frame, height=150, width=500,
                           highlightbackground="black",
                           highlightthickness=2 )
        self.l1.pack(side=tk.TOP, anchor=tk.N, fill=tk.X)

        self.l2 = tk.Frame(self.left_frame, height=150, width=500)
        self.l2.pack(side=tk.TOP, anchor=tk.N, expand=True, fill=tk.BOTH)

        self.l3 = tk.Frame(self.left_frame, height=200, width=500)
        self.l3.pack(fill=tk.Y, expand=True)

        self.l1_left = tk.Frame(self.l1, height=150, width=300)
        self.l1_left.pack(side=tk.LEFT, fill=tk.X)

        self.l1_right = tk.Frame(self.l1, height=150, width=200)
        self.l1_right.pack(side=tk.LEFT, fill=tk.X, padx=10)

        # Frames for the Labels

        self.l1_left_left = tk.Frame(self.l1_left, height=150,
                                     width=100, padx=20)
        self.l1_left_left.pack(side=tk.LEFT)

        self.number_label = tk.Label(self.l1_left_left, text="Tile Number",
                                     font=("Helvetica", self.title_size))
        self.number_label.pack(side=tk.TOP)
        self.choose_number = tk.OptionMenu(self.l1_left_left, self.number,
                                           *VALID_NUMBERS)
        self.choose_number.config(width=10)
        self.choose_number.pack(side=tk.TOP)

        self.l1_left_right = tk.Frame(self.l1_left, height=150,
                                      width=100, padx=20)
        self.l1_left_right.pack(side=tk.LEFT)

        self.number_label = tk.Label(self.l1_left_right, text="Tile Colour",
                                     font=("Helvetica", self.title_size))
        self.number_label.pack(side=tk.TOP)
        self.choose_number = tk.OptionMenu(self.l1_left_right, self.colour,
                                           *VALID_COLOURS)
        self.choose_number.config(width=10)
        self.choose_number.pack(side=tk.LEFT)

        # Add the buttons to the right side of l1

        self.add_board_button = tk.Button(self.l1_right, text="Add to Board",
                                          font=("Helvetica", 12),
                                          command=self.add_to_board)
        self.add_board_button.pack(fill=tk.X, pady=5, expand=True)
        self.draw_button = tk.Button(self.l1_right, text="Add to Hand",
                                     command=self.draw, font=("Helvetica",
                                                                12))
        self.draw_button.pack(fill=tk.X, expand=True)
        self.play_button = tk.Button(self.l1_right, text="Play From Hand",
                                     command=self.play, font=("Helvetica",
                                                                12))
        self.play_button.pack(fill=tk.X, pady=5, expand=True)

        # Add row for remove from board

        self.l21 = tk.Frame(self.l1)
        self.l21.pack(side=tk.LEFT)

        self.remove_from_board_button = tk.Button(self.l21,
                                                  text="Remove from Board",
                                                  command=self.remove_from_board,
                                                  font=("Helvetica",
                                                        12))
        self.remove_from_board_button.pack(padx=10, pady=10)
        self.remove_from_hand_button = tk.Button(self.l21, text="Remove from "
                                                                "Hand",
                                                 command=self.remove_from_hand,
                                                 font=("Helvetica",
                                                       12))
        self.remove_from_hand_button.pack(padx=10, pady=10)

        # Players Hand Text

        self.players_hand_title = tk.Label(self.l2, text="Player's Hand",
                                           font=("Helvetica", self.title_size))
        self.players_hand_title.pack(fill=tk.X)
        self.players_hand = tk.Text(self.l2, height=3)
        self.players_hand.pack(fill=tk.BOTH, expand=True)

        # Board Text

        self.board_title = tk.Label(self.l3, text="Tiles on the Board",
                                    font=("Helvetica", self.title_size))
        self.board_title.pack(fill=tk.X)
        self.board = tk.Text(self.l3, height=5)
        self.board.pack(fill=tk.BOTH, expand=True)

        # Right side of the board

        self.r1 = tk.Frame(self.right_frame)
        self.r1.pack(fill=tk.X)

        self.r11 = tk.Frame(self.r1)
        self.r11.pack()

        # Best Move and possible moves
        self.best_move_button = tk.Button(self.r11, text="Best Move",
                                          command=self.best_move,
                                          font=("Helvetica",
                                                12))
        self.best_move_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.possible_sets_button = tk.Button(self.r11, text="All Possible "
                                                             "Sets",
                                              command=self.best_move,
                                              font=("Helvetica",
                                                    12))
        self.possible_sets_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Set Instructions
        self.set_instructions_title = tk.Label(self.right_frame, text="Set "
                                                                      "Instructions",
                                               font=(
                                               "Helvetica", self.title_size))
        self.set_instructions_title.pack(fill=tk.X)
        self.set_instructions = tk.Text(self.right_frame, height=5)
        self.set_instructions.pack(fill=tk.BOTH, expand=True)

    def reset_game(self):
        self.game = Game()
        self.refresh()

    @staticmethod
    def open_instructions():
        """Opens up the github page with the instructions for the program"""
        webbrowser.open('https://github.com/sbrn3/Rummy-O-Calculator')

    def add_to_board(self):
        """Adds the currently selected number and colour as a tile to the 
        board"""
        self.game.add_to_board(self.colour.get(), self.number.get())
        self.refresh()

    def draw(self):
        """Adds the currently input tile to the player's hand"""
        self.game.draw(self.colour.get(), self.number.get())
        self.refresh()

    def play(self):
        """Removes the tile from the players hand and adds it to the board"""
        self.game.play(self.colour.get(), self.number.get())
        self.refresh()

    def remove_from_board(self):
        """Removes the specified tile from the board"""
        self.game.remove_from_board(self.colour.get(), self.number.get())
        self.refresh()

    def remove_from_hand(self):
        self.game.remove_from_hand(self.colour.get(), self.number.get())
        self.refresh()

    def update_hand(self):
        hand = self.game.view_hand()
        print("Hand: {0}".format(hand))
        self.players_hand.config(state=tk.NORMAL)
        self.players_hand.delete(1.0, tk.END)
        self.players_hand.insert(tk.END, hand)
        self.players_hand.config(state=tk.DISABLED)

    def update_board(self):
        hand = str(self.game.view_board()).replace("[", "").replace("]", "")
        print("Hand: {0}".format(hand))
        self.board.config(state=tk.NORMAL)
        self.board.delete(1.0, tk.END)
        self.board.insert(tk.END, hand)
        self.board.config(state=tk.DISABLED)

    def refresh(self):
        self.update_board()
        self.update_hand()

    def best_move(self):
        pass

    def possible_sets(self):
        pass


if __name__ == '__main__':
    root = Rummy()
    root.mainloop()


