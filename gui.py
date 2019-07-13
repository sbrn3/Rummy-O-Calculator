import tkinter as tk


class Rummy(tk.Tk):
    def __init__(self):
        super(Rummy, self).__init__()
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
        file_menu.add_command(label="Exit", command=self.quit)

        help_menu = tk.Menu(root_menu)
        root_menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Open Instructions",
                              command=self.open_instructions())

        # Create Frames
        self.left_frame = tk.Frame(self, width=500, height=500)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.right_frame = tk.Frame(self, bg="gray")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.r1 = tk.Frame(self.left_frame, bg="red")
        self.r1.pack(side=tk.TOP, fill=tk.X, expand=True)

        # self.label = tk.Label(self.right_frame, text="Hello World", padx=10, pady=10)
        # self.label.pack(side=tk.LEFT)
        #
        # self.hi = tk.Label(self.right_frame, text="Not Yet")
        # self.hi.pack()
        #
        # self.button = tk.Button(self.right_frame, text="Click Me!",
        #                         command=self.say_hi())
        # self.button.pack()

    def say_hi(self):
        pass

    def reset_game(self): # TODO Reset the game
        pass

    def open_instructions(self): # TODO open documentation
        pass


if __name__ == '__main__':
    root = Rummy()
    root.mainloop()
