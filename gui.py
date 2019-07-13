import tkinter as tk
from main import VALID_NUMBERS, VALID_COLOURS


class Rummy(tk.Tk):
    def __init__(self):
        super(Rummy, self).__init__()
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
        file_menu.add_command(label="Reset Game", command=self.reset_game())
        file_menu.add_command(label="Refresh Screen", command=self.refresh())
        file_menu.add_command(label="Exit", command=self.quit)

        help_menu = tk.Menu(root_menu)
        root_menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Open Instructions",
                              command=self.open_instructions())

        # Create Main Frames
        self.left_frame = tk.Frame(self, width=500, height=500, bg="brown")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self, bg="gray")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ## Left side of the screen

        self.l1 = tk.Frame(self.left_frame, bg="red", height=150, width=500)
        self.l1.pack(side=tk.TOP, anchor=tk.N)

        self.l2 = tk.Frame(self.left_frame, bg="blue", height=150, width=500)
        self.l2.pack(side=tk.TOP, anchor=tk.N, expand=True, fill=tk.BOTH)

        self.l3 = tk.Frame(self.left_frame, bg="white", height=200, width=500)
        self.l3.pack(fill=tk.Y, expand=True)

        self.l1_left = tk.Frame(self.l1, bg="green", height=150, width=300)
        self.l1_left.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X)

        self.l1_right = tk.Frame(self.l1, bg="yellow", height=150, width=200)
        self.l1_right.pack(side=tk.RIGHT, fill=tk.X, anchor=tk.E)

        # Frames for the Labels

        self.l1_left_left = tk.Frame(self.l1_left, bg='blue', height=150,
                                     width=100, padx=20)
        self.l1_left_left.pack(side=tk.LEFT)

        self.number_label = tk.Label(self.l1_left_left, text="Tile Number",
                                     font=("Helvetica", self.title_size))
        self.number_label.pack(side=tk.TOP)
        self.choose_number = tk.OptionMenu(self.l1_left_left, self.number,
                                           *VALID_NUMBERS)
        self.choose_number.config(width=10)
        self.choose_number.pack(side=tk.TOP)

        self.l1_left_right = tk.Frame(self.l1_left, bg='blue', height=150,
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
                                          command=self.add_to_board())
        self.add_board_button.pack(fill=tk.X, pady=5, expand=True)
        self.draw_button = tk.Button(self.l1_right, text="Add to Hand",
                                     command=self.draw(), font=("Helvetica",
                                                                12))
        self.draw_button.pack(fill=tk.X, expand=True)
        self.play_button = tk.Button(self.l1_right, text="Play From Hand",
                                     command=self.play(), font=("Helvetica",
                                                                12))
        self.play_button.pack(fill=tk.X, pady=5, expand=True)

        # Add row for remove from board

        self.l21 = tk.Frame(self.l2, bg='gray')
        self.l21.pack()

        self.remove_from_board_button = tk.Button(self.l21,
                                                  text="Remove from Board",
                                                  command=self.remove_from_board(),
                                                  font=("Helvetica",
                                                        12))
        self.remove_from_board_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.remove_from_hand_button = tk.Button(self.l21, text="Remove from "
                                                                "Hand",
                                                 command=self.remove_from_hand(),
                                                 font=("Helvetica",
                                                       12))
        self.remove_from_hand_button.pack(side=tk.LEFT, padx=10, pady=10)

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

        self.r1 = tk.Frame(self.right_frame, bg="green")
        self.r1.pack(fill=tk.X)

        # Best Move and possible moves
        self.best_move_button = tk.Button(self.r1, text="Best Move",
                                          command=self.best_move(),
                                          font=("Helvetica",
                                                12))
        self.best_move_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.possible_sets_button = tk.Button(self.r1, text="All Possible Sets",
                                          command=self.best_move(),
                                          font=("Helvetica",
                                                12))

    def reset_game(self):
        pass

    def open_instructions(self):
        pass

    def add_to_board(self):
        pass

    def draw(self):
        pass

    def play(self):
        pass

    def remove_from_board(self):
        pass

    def remove_from_hand(self):
        pass

    def update_hand(self):
        pass

    def update_board(self):
        pass

    def refresh(self):
        self.update()
        self.update_hand()

    def best_move(self):
        pass

    def possible_sets(self):
        pass


if __name__ == '__main__':
    root = Rummy()
    root.mainloop()
