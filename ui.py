import tkinter as tk
from game_logic import NQueensGame
from board import create_chessboard, add_labels
from firebase_config import db
import re
import time

class NQueensUI:
    def __init__(self, root, size, cell_size, offset):
        self.root = root
        self.size = size
        self.cell_size = cell_size
        self.offset = offset

        # Set the window size to accommodate the chessboard from the start
        self.root.geometry(f"{size * cell_size + 2 * self.offset}x{size * cell_size + 2 * self.offset + 100}")
        self.root.resizable(False, False)

        self.username = tk.StringVar()

        # Create start screen
        self.create_start_screen()

    def create_start_screen(self):
        # Center the username entry in the window
        self.username_label = tk.Label(self.root, text="Enter your name:", font=('Arial', 12))
        self.username_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.username_entry = tk.Entry(self.root, textvariable=self.username, font=('Arial', 12))
        self.username_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Add button to start the game
        self.start_button = tk.Button(self.root, text="Start Game", font=('Arial', 12, 'bold'), fg="white", bg="#FF4040", command=self.validate_and_start_game)
        self.start_button.place(relx=0.5, rely=0.48, anchor=tk.CENTER)

        # Label to display error messages
        self.error_label = tk.Label(self.root, text="", font=('Arial', 10), fg="red")
        self.error_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        # Add "View History" button
        self.history_button = tk.Button(self.root, text="View History", font=('Arial', 12, 'bold'), fg="white", bg="#FF4040", command=self.view_history)
        self.history_button.place(relx=0.5, rely=0.62, anchor=tk.CENTER)

        # Add "Exit" button to exit the application
        self.exit_button = tk.Button(self.root, text="Exit", font=('Arial', 12, 'bold'), fg="white", bg="#FF4040", command=self.root.quit)
        self.exit_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def validate_and_start_game(self):
        username = self.username.get()

        # Validate that the username only contains letters and numbers
        if re.match("^[A-Za-z0-9]+$", username):
            self.error_label.config(text="")  # Clear any previous error message
            self.start_game()
        else:
            self.error_label.config(text="Invalid Input: Username can only contain letters and numbers.")

    def start_game(self):
        # Clear the existing widgets (username entry, start button, and error label)
        self.username_label.place_forget()
        self.username_entry.place_forget()
        self.start_button.place_forget()
        self.error_label.place_forget()
        self.history_button.place_forget()
        self.exit_button.place_forget()

        self.game = NQueensGame(self.size)
        self.start_time = time.time()

        # Create canvas and board
        self.canvas = tk.Canvas(self.root, width=self.size * self.cell_size + 2 * self.offset, height=self.size * self.cell_size + 2 * self.offset)
        self.canvas.pack()
        create_chessboard(self.canvas, self.size, self.cell_size, self.offset)
        add_labels(self.root, self.size, self.cell_size, self.offset)

        # Create a frame to hold the labels for queens left and moves
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=(5, 0))  # Add padding above the frame

        # Label to display number of queens left
        self.queens_left_label = tk.Label(self.info_frame, text=f"♛ left: {self.game.queens_left}", font=('Arial', 14))
        self.queens_left_label.pack(side=tk.LEFT, padx=5)  # Place label to the left

        # Label to display move count
        self.moves_label = tk.Label(self.info_frame, text=f"Moves: {self.game.moves_count}", font=('Arial', 14))
        self.moves_label.pack(side=tk.LEFT, padx=40)  # Place label to the left

        # Label to display invalid move messages
        self.invalid_move_label = tk.Label(self.root, text="", font=('Arial', 12), fg="red")
        self.invalid_move_label.pack(pady=(0, 10))  # Reduce the padding below the label

        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        x = (event.x - self.offset) // self.cell_size
        y = (event.y - self.offset) // self.cell_size

        if 0 <= x < self.size and 0 <= y < self.size:
            action = self.game.place_or_remove_queen(y, x)
            self.update_board()

            if action:
                self.invalid_move_label.config(text="")  # Clear any previous invalid move message
            else:
                self.invalid_move_label.config(text="Invalid Move: The queen can be attacked by another queen!")

            self.moves_label.config(text=f"Moves: {self.game.moves_count}")
            self.queens_left_label.config(text=f"♛ left: {self.game.queens_left}")

            if self.game.queens_left == 0:
                end_time = time.time()
                game_time = round(end_time - self.start_time, 2)
                self.invalid_move_label.config(text=f"All queens are placed! Well done, {self.username.get()}! Game Time: {game_time} seconds.")
                self.save_game_data(self.username.get(), self.game.moves_count, game_time)
                self.canvas.unbind("<Button-1>")  # Disable further clicks after completing the game

    def save_game_data(self, player_name, moves_count, game_time):
        # Save the game data to Firebase Firestore
        game_data = {
            'player_name': player_name,
            'moves_count': moves_count,
            'game_time': game_time
        }
        db.collection('n_queens_game_data').add(game_data)

    def update_board(self):
        self.canvas.delete("all")
        create_chessboard(self.canvas, self.size, self.cell_size, self.offset)
        for row in range(self.size):
            for col in range(self.size):
                if self.game.board[row][col] == 1:
                    self.draw_queen(col, row)

    def draw_queen(self, x, y):
        self.canvas.create_text(
            x * self.cell_size + self.cell_size // 2 + self.offset,
            y * self.cell_size + self.cell_size // 2 + self.offset,
            text="♛", font=('Arial', 24), fill="black"
        )

    def view_history(self):
        # Clear the start screen widgets
        self.username_label.place_forget()
        self.username_entry.place_forget()
        self.start_button.place_forget()
        self.error_label.place_forget()
        self.history_button.place_forget()
        self.exit_button.place_forget()

        # Create a frame to hold the history list and back button
        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(fill=tk.BOTH, expand=True)

        # Create a label for the history title
        history_title = tk.Label(self.history_frame, text="Game History", font=('Arial', 16, 'bold'))
        history_title.pack(pady=10)

        # Create a Listbox to display the game history
        self.history_listbox = tk.Listbox(self.history_frame, font=('Arial', 12))
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Retrieve and display game data from Firebase Firestore
        game_data = db.collection('n_queens_game_data').stream()
        for game in game_data:
            game_info = game.to_dict()
            self.history_listbox.insert(tk.END, f"Player: {game_info['player_name']}, Moves: {game_info['moves_count']}, Time: {game_info['game_time']}s")

        # Add a back button to return to the start screen
        self.back_button = tk.Button(self.history_frame, text="Back", font=('Arial', 12, 'bold'), fg="white", bg="#FF4040", command=self.back_to_start)
        self.back_button.pack(pady=10)

    def back_to_start(self):
        # Clear the history frame widgets
        self.history_frame.destroy()

        # Return to the start screen
        self.create_start_screen()
