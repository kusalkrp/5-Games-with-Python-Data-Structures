import tkinter as tk
from TowerOfHanoi import TowerOfHanoi
from PIL import Image, ImageTk, ImageDraw
import os
#from ShortestPath import ShortestPath  # Import the second game module

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Hub")
        self.master.geometry("320x500")
        self.master.resizable(False, False)  # Disable window resizing

        # Set background color
        self.master.configure(bg="#ffffff")

        tk.Label(master, text="Select a Game to Play:", font=("Arial", 18, "bold"), fg="#fa0000", bg="#ffffff").pack(pady=20)

        # Load images for each game with error handling
        self.game_images = {
            "Tower of Hanoi": self.load_image("./images/towerofhanoi.png"),
            "ShortestPath": self.load_image("./images/shortestpath.webp"),
            "Minimum Cost": self.load_image("./images/minimumcost.png"),
            "Sixteen Queen Puzzle": self.load_image("./images/queenpuzzle.png"),
            "Predict Index": self.load_image("./images/predictindex.png"),
        }

        # Create a frame to hold the list of games
        game_list_frame = tk.Frame(master, bg="#ffffff")
        game_list_frame.pack(pady=10)

        # Add games to the list with grid layout for proper alignment
        self.add_game_option(game_list_frame, "Tower of Hanoi", 0, self.launch_game1)
        self.add_game_option(game_list_frame, "ShortestPath", 1, self.launch_game2)
        self.add_game_option(game_list_frame, "Minimum Cost", 2, self.launch_game3)
        self.add_game_option(game_list_frame, "Sixteen Queen Puzzle", 3, self.launch_game4)
        self.add_game_option(game_list_frame, "Predict Index", 4, self.launch_game5)
        
    def load_image(self, filename):
        try:
            image_path = os.path.join(os.getcwd(), filename)
            image = Image.open(image_path).resize((50, 50))
            
            # Create a mask to make the image rounded
            mask = Image.new("L", image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + image.size, fill=255)

            rounded_image = Image.new("RGBA", image.size)
            rounded_image.paste(image, (0, 0), mask)

            return ImageTk.PhotoImage(rounded_image)
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
            return None

    def add_game_option(self, parent, game_name, row, command):
        img_label = tk.Label(parent, image=self.game_images.get(game_name), bg="#ffffff")
        img_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        button = tk.Button(parent, text=game_name, command=command, font=("Arial", 12, "bold"), bg="#68adee", fg="#ffffff", relief="flat", width=17, anchor="w", padx=10)
        button.grid(row=row, column=1, padx=10, pady=5, sticky="w")

    def launch_game1(self):
        game_window = tk.Toplevel(self.master)
        TowerOfHanoi(game_window)  
    

    def launch_game2(self):
        game_window = tk.Toplevel(self.master)
      

    def launch_game3(self):
        game_window = tk.Toplevel(self.master)
      

    def launch_game4(self):
        game_window = tk.Toplevel(self.master)
       

    def launch_game5(self):
        game_window = tk.Toplevel(self.master)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
