import tkinter as tk


class ShortestPath:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Path Game")
        self.root.geometry("800x600")
        
        # Initialize variables
        self.username = tk.StringVar()

        # Create frames
        self.main_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)

        # Setup the main frame UI
        self.setup_main_frame()

    def setup_main_frame(self):
        self.main_frame.pack(fill='both', expand=True)

        # Add a label for the username
        tk.Label(self.main_frame, text="Enter your name:").pack(pady=20)

        # Add an entry widget for username
        tk.Entry(self.main_frame, textvariable=self.username).pack(pady=10)

        # Add a start button
        tk.Button(self.main_frame, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        """Start the game and navigate to the game frame."""
        user_name = self.username.get()

        if user_name.strip():
            # Hide the main frame
            self.main_frame.pack_forget()

            # Setup game frame
            self.setup_game_frame()
        else:
            tk.messagebox.showwarning("Input Error", "Please enter your name!")

    def setup_game_frame(self):
        """Setup the game frame where the game will be played."""
        self.game_frame.pack(fill='both', expand=True)

        # Display a welcome message with the username
        tk.Label(self.game_frame, text=f"Welcome {self.username.get()}!", font=('Arial', 18)).pack(pady=50)

        # Add a placeholder for game components
        tk.Label(self.game_frame, text="Game components will go here.", font=('Arial', 14)).pack(pady=10)

        # Add a button to go back to the main frame
        tk.Button(self.game_frame, text="Back", command=self.go_back).pack(pady=20)

    def go_back(self):
        """Go back to the main frame to restart or change user."""
        self.game_frame.pack_forget()
        self.setup_main_frame()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ShortestPath(root)
    root.mainloop()
