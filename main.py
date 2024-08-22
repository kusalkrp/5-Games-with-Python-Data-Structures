import tkinter as tk
# Import other game modules similarly
# from game2 import Game2
# from game3 import Game3
# from game4 import Game4
# from game5 import Game5

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Hub")
        self.master.geometry("300x400")
        
        tk.Label(master, text="Select a Game to Play:", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(master, text="Tower of Hanoi", command=self.launch_game1).pack(pady=10)
        tk.Button(master, text="Game 2", command=self.launch_game2).pack(pady=10)
        tk.Button(master, text="Game 3", command=self.launch_game3).pack(pady=10)
        tk.Button(master, text="Game 4", command=self.launch_game4).pack(pady=10)
        tk.Button(master, text="Game 5", command=self.launch_game5).pack(pady=10)
        
    def launch_game1(self):
        game_window = tk.Toplevel(self.master)
       # Launch the Tower of Hanoi game

    def launch_game2(self):
        game_window = tk.Toplevel(self.master)
        # Game2(game_window)  # Launch the second game

    def launch_game3(self):
        game_window = tk.Toplevel(self.master)
        # Game3(game_window)  # Launch the third game

    def launch_game4(self):
        game_window = tk.Toplevel(self.master)
        # Game4(game_window)  # Launch the fourth game

    def launch_game5(self):
        game_window = tk.Toplevel(self.master)
        # Game5(game_window)  # Launch the fifth game

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
