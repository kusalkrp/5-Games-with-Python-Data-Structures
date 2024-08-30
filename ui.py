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
        self.canvas = None
        self.history_frame = None

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
        self.game = NQueensGame(self.size)
        self.start_time = time.time()

        # Create canvas and board
        self.canvas = tk.Canvas(self.root, width=self.size * self.cell_size + 2 * self.offset, height=self.size * self.cell_size + 2 * self.offset)
        self.canvas.pack()

        create_chessboard(self.canvas, self.size, self.cell_size, self.offset)
        add_labels(self.root, self.size, self.cell_size, self.offset)

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

        self.game = NQueensGame(self.size)
        self.start_time = time.time()

        # Create canvas and board
        self.canvas = tk.Canvas(self.root, width=self.size * self.cell_size + 2 * self.offset, height=self.size * self.cell_size + 2 * self.offset)
        self.canvas.pack()

        create_chessboard(self.canvas, self.size, self.cell_size, self.offset)
        add_labels(self.root, self.size, self.cell_size, self.offset)

        # Recalculate center x-coordinate for proper placement of labels
        center_x = (self.size * self.cell_size + 2 * self.offset) // 2

        # Create and place labels to display number of queens left and moves
        self.queens_left_label = tk.Label(self.root, text=f"♛ left: {self.game.queens_left}", font=('Arial', 14))
        self.queens_left_label.place(x=center_x - 150, y=self.size * self.cell_size + self.offset + 50)

        self.moves_label = tk.Label(self.root, text=f"Moves: {self.game.moves_count}", font=('Arial', 14))
        self.moves_label.place(x=center_x + 50, y=self.size * self.cell_size + self.offset + 50)

        # Label to display invalid move messages
        self.invalid_move_label = tk.Label(self.root, text="", font=('Arial', 12), fg="red")
        self.invalid_move_label.place(x=center_x, y=self.size * self.cell_size + 80, anchor=tk.CENTER)
        
        # Label to display final move messages
        self.final_move_label = tk.Label(self.root, text="", font=('Arial', 12), fg="green")
        self.final_move_label.place(x=center_x, y=self.size * self.cell_size + 80, anchor=tk.CENTER)

        self.canvas.bind("<Button-1>", self.on_click)

        # Enable menu options related to the game
        self.update_menu_state('game')

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
                self.final_move_label.config(text=f"All queens are placed! Well done, {self.username.get()}! Game Time: {game_time} seconds.")
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
            text="♛", font=('Arial', 28), fill="black"
        )

    def view_history(self):
        self.clear_all_screens()
        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(fill=tk.BOTH, expand=True)

        history_title = tk.Label(self.history_frame, text="Game History", font=('Arial', 16, 'bold'))
        history_title.pack(pady=10)

        # Use Text widget with a monospaced font for proper column alignment
        self.history_text = tk.Text(self.history_frame, font=('Courier', 11))
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Adding the table header with Courier font, size 14, and bold
        header_font = ('Times new roman', 14, 'bold')
        header = f"{'Player Name':<20}{'Moves':<10}{'Game Time (s)':<15}\n"
        self.history_text.insert(tk.END, header)
        self.history_text.tag_add("header", "1.0", "1.end")
        self.history_text.tag_config("header", font=header_font)

        self.history_text.insert(tk.END, "-" * 45 + "\n")  # Adding a separator

        # Fetching game data and inserting it into the Text widget
        game_data = db.collection('n_queens_game_data').stream()
        for game in game_data:
            game_info = game.to_dict()

            # Check if all necessary keys exist before accessing them
            player_name = game_info.get('player_name', 'Unknown')
            moves_count = game_info.get('moves_count', 'N/A')
            game_time = game_info.get('game_time', 'N/A')

            # Format and insert the game data into the Text widget
            entry = f"{player_name:<20}{moves_count:<10}{game_time:<15}\n"
            self.history_text.insert(tk.END, entry)

        # Disable editing the Text widget
        self.history_text.config(state=tk.DISABLED)

        self.back_button = tk.Button(self.history_frame, text="Back", font=('Arial', 12, 'bold'), fg="white", bg="#FF4040", command=self.back_to_start)
        self.back_button.pack(pady=10)

        # Enable "Main Menu" option on history screen
        self.update_menu_state('history')




    def back_to_start(self):
        self.clear_all_screens()
        self.create_start_screen()

    def clear_game_screen(self):
        if self.canvas:
            self.canvas.destroy()
            self.canvas = None
        if hasattr(self, 'invalid_move_label'):
            self.invalid_move_label.destroy()
            del self.invalid_move_label
        if hasattr(self, 'moves_label'):
            self.moves_label.destroy()
            del self.moves_label
        if hasattr(self, 'queens_left_label'):
            self.queens_left_label.destroy()
            del self.queens_left_label
        if hasattr(self, 'final_move_label'):
            self.final_move_label.destroy()
            del self.final_move_label
        self.root.update_idletasks()

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
    app = NQueensUI(root, size=8, cell_size=40, offset=20)
    root.mainloop()
