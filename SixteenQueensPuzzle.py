import tkinter as tk
import firebase_admin
from firebase_admin import credentials, firestore
import re
import time
import tkinter.ttk as ttk 

class NQueensUI:
    
    class NQueensGame:
        def __init__(self, size):
            self.size = size
            self.board = [[0] * size for _ in range(size)]
            self.queens_left = size
            self.moves_count = 0
            self.move_paths = []  # Store the move paths as a list of strings

        def is_valid_move(self, row, col):
            # Check the row
            for i in range(self.size):
                if self.board[row][i] == 1:
                    return False

            # Check the column
            for i in range(self.size):
                if self.board[i][col] == 1:
                    return False

            # Check the diagonals
            for i in range(self.size):
                for j in range(self.size):
                    if abs(row - i) == abs(col - j) and self.board[i][j] == 1:
                        return False

            return True

        def place_or_remove_queen(self, row, col):
            if self.board[row][col] == 0:  # Try to place a queen
                if self.is_valid_move(row, col):
                    self.board[row][col] = 1
                    self.queens_left -= 1
                    self.moves_count += 1
                    self.move_paths.append(f"P({row}, {col})")
                    return True
            else:  # Remove the queen
                self.board[row][col] = 0
                self.queens_left += 1
                self.moves_count += 1
                self.move_paths.append(f"R({row}, {col})")
                return True

            return False
    
    def __init__(self, root, size, cell_size, offset):
        self.root = root
        self.size = size
        self.cell_size = cell_size
        self.offset = offset
        self.board_locked = False

        # Set the window size to accommodate the chessboard from the start
        self.root.geometry(f"{size * cell_size + 2 * self.offset}x{size * cell_size + 2 * self.offset + 100}")
        self.root.resizable(False, False)

        self.username = tk.StringVar()
        self.canvas = None
        self.history_frame = None
        
        self.initialize_firebase()

        # Create the menu bar
        self.create_menu_bar()

        # Create start screen
        self.create_start_screen()

    def create_menu_bar(self):
        # Create a menu bar
        menu_bar = tk.Menu(self.root)

        # Create a 'Menu' dropdown menu
        self.menu = tk.Menu(menu_bar, tearoff=0)
        self.menu.add_command(label="Start New Game", command=self.start_new_game)
        self.menu.add_command(label="Main Menu", command=self.back_to_start)
        self.menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="Menu", menu=self.menu)

        # Add the menu bar to the root window
        self.root.config(menu=menu_bar)
        
    def create_chessboard(self, canvas, size, cell_size, offset):
        color1 = "#954535"  # Brown color
        color2 = "#F5DEB3"  # White color

        for row in range(size):
            for col in range(size):
                color = color1 if (row + col) % 2 == 0 else color2
                canvas.create_rectangle(
                    col * cell_size + offset, row * cell_size + offset,
                    (col + 1) * cell_size + offset, (row + 1) * cell_size + offset,
                    fill=color, outline=color
                )

    def add_labels(self, root, size, cell_size, offset):
        for i in range(size):
            row_label = tk.Label(root, text=str(size - i), font=('Times New Roman', 10))
            row_label.place(x=offset // 2, y=i * cell_size + offset + cell_size // 4)

            col_label = tk.Label(root, text=str(i + 1), font=('Times New Roman', 10))
            col_label.place(x=i * cell_size + offset + cell_size // 3, y=offset // 4)

            row_label_mirror = tk.Label(root, text=str(size - i), font=('Times New Roman', 10))
            row_label_mirror.place(x=size * cell_size + offset + offset // 3, y=i * cell_size + offset + cell_size // 4)

            col_label_mirror = tk.Label(root, text=str(i + 1), font=('Times New Roman', 10))
            col_label_mirror.place(x=i * cell_size + offset + cell_size // 3, y=size * cell_size + offset + offset // 4)
        
    def initialize_firebase(self):
        # Use your own Firebase credentials
        try:
            if not firebase_admin._apps:  # Check if Firebase is already initialized
                cred = credentials.Certificate(
                    "pdsa-cw-4fe71-firebase-adminsdk-mvt7n-55e5f9e362.json"
                )
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
        except ValueError as e:
            print(f"Error initializing Firebase: {e}")

        self.db = firestore.client()

    def update_menu_state(self, state):
        # Update the menu options based on the current screen
        if state == 'start':
            self.menu.entryconfig("Start New Game", state=tk.DISABLED)
            self.menu.entryconfig("Main Menu", state=tk.DISABLED)
        elif state == 'game':
            self.menu.entryconfig("Start New Game", state=tk.DISABLED)
            self.menu.entryconfig("Main Menu", state=tk.DISABLED)
        elif state == 'history':
            self.menu.entryconfig("Start New Game", state=tk.DISABLED)
            self.menu.entryconfig("Main Menu", state=tk.NORMAL)

    def start_new_game(self):
        # Clear the existing game screen
        self.clear_game_screen()

        # Create a new game
        self.game = self.NQueensGame(self.size)
        self.start_time = time.time()

        # Create canvas and board
        self.canvas = tk.Canvas(self.root, width=self.size * self.cell_size + 2 * self.offset, height=self.size * self.cell_size + 2 * self.offset)
        self.canvas.pack()

        self.create_chessboard(self.canvas, self.size, self.cell_size, self.offset)
        self.add_labels(self.root, self.size, self.cell_size, self.offset)

        # Recreate labels with proper positioning
        center_x = (self.size * self.cell_size + 2 * self.offset) // 2
        self.queens_left_label = tk.Label(self.root, text=f"♛ left: {self.game.queens_left}", font=('Arial', 14))
        self.queens_left_label.place(x=center_x - 100, y=self.size * self.cell_size + self.offset + 10)

        self.moves_label = tk.Label(self.root, text=f"Moves: {self.game.moves_count}", font=('Arial', 14))
        self.moves_label.place(x=center_x + 100, y=self.size * self.cell_size + self.offset + 10)

        # Label to display invalid move messages
        self.invalid_move_label = tk.Label(self.root, text="", font=('Arial', 12), fg="red")
        self.invalid_move_label.place(x=center_x, y=self.size * self.cell_size + self.offset + 40, anchor=tk.CENTER)
        
        # Label to display final move messages
        self.final_move_label = tk.Label(self.root, text="", font=('Arial', 12), fg="green")
        self.final_move_label.place(x=center_x, y=self.size * self.cell_size + self.offset + 40, anchor=tk.CENTER)

        self.canvas.bind("<Button-1>", self.on_click)

        # Enable menu options related to the game
        self.update_menu_state('game')

    def create_start_screen(self):
        # Center the username entry in the window
        self.username_label = tk.Label(self.root, text="Enter your name:", font=('Arial', 12, 'bold'))
        self.username_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.username_entry = tk.Entry(self.root, textvariable=self.username, font=('Arial', 12))
        self.username_entry.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        # Add button to start the game
        self.start_button = tk.Button(self.root, text="Start Game", font=('Arial', 12, 'bold'), fg="white", bg="#FF4040", command=self.validate_and_start_game)
        self.start_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        # Label to display error messages
        self.error_label = tk.Label(self.root, text="", font=('Arial', 10), fg="red")
        self.error_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Add "View History" button
        self.history_button = tk.Button(self.root, text="View History", font=('Arial', 12, 'bold'), fg="white", bg="#FF4040", command=self.view_history)
        self.history_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        # Disable "Start New Game" menu option on start screen
        self.update_menu_state('start')

    def validate_and_start_game(self):
        username = self.username.get()

        try:
            # Validate that the username only contains letters and numbers
            if re.match("^[A-Za-z0-9]+$", username):
                self.error_label.config(text="")  # Clear any previous error message
                self.start_game()
            else:
                raise ValueError("Invalid Input: Username can only contain letters and numbers.")
        except ValueError as e:
            self.error_label.config(text=str(e))


    def start_game(self):
        # Clear the existing widgets (username entry, start button, and error label)
        self.username_label.place_forget()
        self.username_entry.place_forget()
        self.start_button.place_forget()
        self.error_label.place_forget()
        self.history_button.place_forget()

        self.game = self.NQueensGame(self.size)
        self.start_time = time.time()

        # Create canvas and board
        self.canvas = tk.Canvas(self.root, width=self.size * self.cell_size + 2 * self.offset, height=self.size * self.cell_size + 2 * self.offset)
        self.canvas.pack()

        self.create_chessboard(self.canvas, self.size, self.cell_size, self.offset)
        self.add_labels(self.root, self.size, self.cell_size, self.offset)

        # Recalculate center x-coordinate for proper placement of labels
        center_x = (self.size * self.cell_size + 2 * self.offset) // 2

        # Create and place labels to display number of queens left and moves
        self.queens_left_label = tk.Label(self.root, text=f"♛ left: {self.game.queens_left}", font=('Arial', 14))
        self.queens_left_label.place(x=center_x - 150, y=self.size * self.cell_size + self.offset + 50)

        self.moves_label = tk.Label(self.root, text=f"Moves: {self.game.moves_count}", font=('Arial', 14))
        self.moves_label.place(x=center_x + 50, y=self.size * self.cell_size + self.offset + 50)

        # Label to display invalid move messages
        self.invalid_move_label = tk.Label(self.root, text="", font=('Arial', 12, 'bold'), fg="red")
        self.invalid_move_label.place(x=center_x, y=self.size * self.cell_size + 80, anchor=tk.CENTER)
        
        # Label to display final move messages
        self.final_move_label = tk.Label(self.root, text="", font=('Arial', 12, 'bold'), fg="green")
        self.final_move_label.place(x=center_x, y=self.size * self.cell_size + 80, anchor=tk.CENTER)
        
        self.final_move_label_taken = tk.Label(self.root, text="", font=('Arial', 12, 'bold'), fg="#F16032")
        self.final_move_label_taken.place(x=center_x, y=self.size * self.cell_size + 80, anchor=tk.CENTER)

        self.canvas.bind("<Button-1>", self.on_click)

        # Enable menu options related to the game
        self.update_menu_state('game')

    def on_click(self, event):
        if self.board_locked:
            return  # Exit if the board is locked

        x = (event.x - self.offset) // self.cell_size
        y = (event.y - self.offset) // self.cell_size

        if 0 <= x < self.size and 0 <= y < self.size:
            action = self.game.place_or_remove_queen(y, x)
            self.update_board()

            # Clear previous messages
            self.invalid_move_label.config(text="")
            self.final_move_label.config(text="")

            try:
                if action:
                    # Valid move
                    self.moves_label.config(text=f"Moves: {self.game.moves_count}")
                    self.queens_left_label.config(text=f"♛ left: {self.game.queens_left}")

                    if self.game.queens_left == 0:
                        try:
                            if self.is_move_paths_taken(self.game.move_paths):
                                raise ValueError("The answer has already been taken! Try again.")
                            else:
                                end_time = time.time()
                                game_time = round(end_time - self.start_time, 2)
                                self.final_move_label.config(text=f"Congratulations {self.username.get()}! You have placed all  queens correctly. Time taken: {game_time} seconds.")
                                self.board_locked = True  # Lock the board

                                # Save the game record to Firebase
                                try:
                                    self.db.collection("nqueens").add({
                                        "username": self.username.get(),
                                        "moves_count": self.game.moves_count,
                                        "game_time": game_time,
                                        "move_paths": self.game.move_paths
                                    })
                                except Exception as e:
                                    print(f"Error saving to Firebase: {e}")
                                    self.final_move_label.config(text=f"Game completed, but could not save record: {e}")

                                # Check and reset solutions if all have been found
                                # self.check_and_reset_solutions()

                        except ValueError as e:
                            self.final_move_label_taken.config(text=str(e))
                            self.board_locked = True  # Lock the board

                else:
                    # Invalid move
                    self.invalid_move_label.config(text="   Invalid  Move:  The  queen  can  be  attacked  by  another  queen!")

            except Exception as e:
                print(f"An error occurred: {e}")
                self.invalid_move_label.config(text="An unexpected error occurred. Please try again.")



                
    def on_exit(self):
        if self.board_locked:
            # Unlock the board and perform any necessary cleanup
            self.board_locked = False
        self.master.destroy()  


    def is_move_paths_taken(self, current_move_paths):
        records = self.db.collection("nqueens").get()
        current_set = set(current_move_paths)

        for record in records:
            data = record.to_dict()
            existing_move_paths = data['move_paths']
            existing_set = set(existing_move_paths)

            if current_set == existing_set:
                return True

        return False                

    def update_board(self):
        self.canvas.delete("all")  # Clear previous board
        for i in range(self.size):
            for j in range(self.size):
                x1 = j * self.cell_size + self.offset
                y1 = i * self.cell_size + self.offset
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if self.game.board[i][j] == 1:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="♛", font=("Arial", 28), tags="queen")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#954535" if (i + j) % 2 == 0 else "#F5DEB3", outline="") 

    def clear_game_screen(self):
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.delete("all")
            self.canvas.pack_forget()

        if hasattr(self, 'queens_left_label') and self.queens_left_label:
            self.queens_left_label.destroy()

        if hasattr(self, 'moves_label') and self.moves_label:
            self.moves_label.destroy()

        if hasattr(self, 'invalid_move_label') and self.invalid_move_label:
            self.invalid_move_label.destroy()

        if hasattr(self, 'final_move_label') and self.final_move_label:
            self.final_move_label.destroy()

    def view_history(self):
        self.clear_all_screens()

        # Hide the start screen elements
        if hasattr(self, 'username_label'):
            self.username_label.place_forget()
        if hasattr(self, 'username_entry'):
            self.username_entry.place_forget()
        if hasattr(self, 'start_button'):
            self.start_button.place_forget()
        if hasattr(self, 'error_label'):
            self.error_label.place_forget()
        if hasattr(self, 'history_button'):
            self.history_button.place_forget()

        # Create a new frame to display the history
        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        history_label = tk.Label(self.history_frame, text="Game History", font=('Arial', 16, 'bold'))
        history_label.pack()

        # Create a frame to hold the Treeview and scrollbars
        tree_frame = tk.Frame(self.history_frame)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Create a Treeview widget to display history as a table
        columns = ("Player Name", "Move Count", "Game Time", "Moves")
        self.history_listbox = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Define column headings
        self.history_listbox.heading("Player Name", text="Player Name")
        self.history_listbox.heading("Move Count", text="Move Count")
        self.history_listbox.heading("Game Time", text="Game Time (s)")
        self.history_listbox.heading("Moves", text="Moves")

        # Define column widths with increased width for "Move Paths"
        self.history_listbox.column("Player Name", anchor=tk.W, width=150)
        self.history_listbox.column("Move Count", anchor=tk.CENTER, width=100)
        self.history_listbox.column("Game Time", anchor=tk.CENTER, width=100)
        self.history_listbox.column("Moves", anchor=tk.W, width=1800)

        # Add vertical and horizontal scrollbars for the Treeview
        scrollbar_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        scrollbar_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.history_listbox.xview)

        self.history_listbox.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Pack the scrollbars
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Pack the Treeview widget to expand and fill available space
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Insert data into Treeview
        records = self.db.collection("nqueens").get()
        for record in records:
            data = record.to_dict()
            self.history_listbox.insert("", "end", values=(data['username'], data['moves_count'], data['game_time'], data['move_paths']))

        # Add a back button
        self.back_button = tk.Button(self.history_frame, text="Back to Main Menu", command=self.back_to_start, font=('Arial', 12, 'bold'), fg="white", bg="#FF4040")
        self.back_button.pack(pady=50)

        # Update menu state to reflect that we're in the history screen
        self.update_menu_state('history')


    def back_to_start(self):
        # Clear the history frame if it exists
        if self.history_frame:
            self.history_frame.destroy()

        # Recreate the start screen
        self.create_start_screen()

    def clear_game_screen(self):
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.delete("all")
            self.canvas.pack_forget()

        if hasattr(self, 'queens_left_label') and self.queens_left_label:
            self.queens_left_label.destroy()

        if hasattr(self, 'moves_label') and self.moves_label:
            self.moves_label.destroy()

        if hasattr(self, 'invalid_move_label') and self.invalid_move_label:
            self.invalid_move_label.destroy()

        if hasattr(self, 'final_move_label') and self.final_move_label:
            self.final_move_label.destroy()

    def clear_all_screens(self):
        self.clear_game_screen()
        if self.history_frame:
            self.history_frame.destroy()
            self.history_frame = None
        if hasattr(self, 'history_listbox'):
            self.history_listbox.destroy()
            del self.history_listbox
        if hasattr(self, 'back_button'):
            self.back_button.destroy()
            del self.back_button
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("16-Queens Problem")
    root.resizable(False, False)
    app = NQueensUI(root, size=16, cell_size=40, offset=40)
    root.mainloop()
