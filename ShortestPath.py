import tkinter as tk
from tkinter import messagebox


class ShortestPath:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Path Game")
        self.root.geometry("800x600")
        
        self.username = tk.StringVar()

        self.main_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)

        self.setup_main_frame()

    def setup_main_frame(self):
        self.main_frame.pack(fill='both', expand=True)

        tk.Label(self.main_frame, text="Enter your name:").pack(pady=20)

        tk.Entry(self.main_frame, textvariable=self.username).pack(pady=10)

        tk.Button(self.main_frame, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        user_name = self.username.get()

        if user_name.strip():
            self.main_frame.pack_forget()

            self.setup_game_frame()
        else:
            tk.messagebox.showwarning("Input Error", "Please enter your name!")

    def setup_game_frame(self):
        self.game_frame.pack(fill='both', expand=True)

        tk.Label(self.game_frame, text=f"Welcome {self.username.get()}!", font=('Arial', 18)).pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShortestPath(root)
    root.mainloop()
