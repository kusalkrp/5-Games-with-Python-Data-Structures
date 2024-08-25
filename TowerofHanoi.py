import time
import tkinter as tk
import firebase_admin
from firebase_admin import credentials, firestore
import random
  
class TowerOfHanoi:
    def __init__(self, master):
        self.master = master
        self.master.title("Tower of Hanoi")
        self.master.geometry("800x600")  # Increased window size
        
        # Prevent the window from being resized
        self.master.resizable(False, False)
        
        self.name = tk.StringVar()
        self.num_disks = tk.IntVar()
        self.num_moves = 0
        self.move_sequence = []
        self.start_time = None
        
        self.frames = {}
        self.current_frame = None
        self.drag_data = None  # Initialize drag_data here

        self.initialize_firebase()  # Add this line to initialize Firebase
        self.create_frames()
        self.show_frame("NameEntry")

    def initialize_firebase(self):
        # Use your own Firebase credentials
        cred = credentials.Certificate("pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        


    def create_frames(self):
        # Create frames for different stages
        self.frames["NameEntry"] = tk.Frame(self.master)
        self.frames["DiskEntry"] = tk.Frame(self.master)
        self.frames["Game"] = tk.Frame(self.master)

        self.create_name_entry_frame()
        self.create_disk_entry_frame()
        self.create_game_frame()
        
    def create_name_entry_frame(self):
        frame = self.frames["NameEntry"]

        tk.Label(frame, text="Enter Your Name:", font=("Arial", 14)).pack(pady=20)
        tk.Entry(frame, textvariable=self.name, font=("Arial", 14)).pack(pady=10)
        
        self.name_error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12))
        self.name_error_label.pack(pady=5)
        
        tk.Button(frame, text="Next", command=self.go_to_disk_entry_frame, font=("Arial", 12)).pack(pady=20)
        
    def create_disk_entry_frame(self):
        frame = self.frames["DiskEntry"]

        tk.Label(frame, text="Enter Number of Disks:", font=("Arial", 14)).pack(pady=20)
        # Validate that only positive integers are accepted
        validate_command = self.master.register(self.validate_disk_entry)
        self.disk_entry = tk.Entry(frame, textvariable=self.num_disks, font=("Arial", 14),
                                  validate="key", validatecommand=(validate_command, "%P"))
        self.disk_entry.pack(pady=10)
        
        self.disk_error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12))
        self.disk_error_label.pack(pady=5)
        
        tk.Button(frame, text="Start Game", command=self.start_game, font=("Arial", 12)).pack(pady=20)
        tk.Button(frame, text="Back", command=self.go_to_name_entry_frame, font=("Arial", 12)).pack(pady=10)
        
    def create_game_frame(self):
        frame = self.frames["Game"]
        
        # Create a menu bar
        menu_bar = tk.Menu(frame)
        frame.master.config(menu=menu_bar)  # Attach the menu bar to the main window
    
        # Create a 'Game' menu
        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menu", menu=game_menu)
    
        # Add 'Start New Game' and 'Exit' options
        game_menu.add_command(label="Start New Game", command=self.start_new_game)
        game_menu.add_command(label="Exit", command=self.go_back_to_main_menu)
        
        self.instructions_label = tk.Label(frame, text="*** Move all disks from rod A to rod C ***", font=("Arial", 12))
        self.instructions_label.pack(pady=5)
        self.instructions_label = tk.Label(frame, text="*** Move only one disk at a time ***", font=("Arial", 12))
        self.instructions_label.pack(pady=10)
        
        self.error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12))
        self.error_label.pack(pady=5)
        
        self.canvas = tk.Canvas(frame, width=600, height=300, bg='white')
        self.canvas.pack(pady=20)
        
        self.result_label = tk.Label(frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)
        
        self.start_new_game_button = tk.Button(frame, text="Start New Game", command=self.start_new_game, font=("Arial", 12))
        self.start_new_game_button.pack(pady=5)
        self.back_to_main_menu_button = tk.Button(frame, text="Back to Main Menu", command=self.go_back_to_main_menu, font=("Arial", 12))
        self.back_to_main_menu_button.pack(pady=20)
        
        self.rods = {'A': [], 'B': [], 'C': []}
        self.rod_positions = {'A': 100, 'B': 300, 'C': 500}
        self.disks = []

        # Draw the rods
        rod_height = 200
        rod_width = 10
        for _, x in self.rod_positions.items():
            self.canvas.create_rectangle(x - rod_width//2, 100, x + rod_width//2, 100 + rod_height, fill="black")
            
    def validate_disk_entry(self, value):
        """ Validate the disk entry to ensure it is a positive integer """
        if value == "":
            self.disk_error_label.config(text="")  # Clear any previous error messages
            return True  # Allow empty entry
        try:
            int_value = int(value)
            if int_value > 0:
                self.disk_error_label.config(text="")  # Clear any previous error messages
                return True
            else:
                self.disk_error_label.config(text="Number of disks must be greater than 0")
                return False
        except ValueError:
            self.disk_error_label.config(text="Please enter a valid number")
            return False


    def go_to_name_entry_frame(self):
            self.show_frame("NameEntry")

    def go_to_disk_entry_frame(self):
            if not self.name.get():
                self.name_error_label.config(text="Name cannot be empty")
                return
            self.name_error_label.config(text="")
            self.show_frame("DiskEntry")
            
    def start_game(self):
            num_disks = self.num_disks.get()
            if num_disks < 1:
                self.disk_error_label.config(text="Number of disks must be greater than 0")
                return

            self.disk_error_label.config(text="")
            self.start_time = time.time()
            self.num_moves = 0
            self.move_sequence = []
            self.rods = {'A': [], 'B': [], 'C': []}
            self.disks = []
            
            # Initialize disks with colors
            self.disk_colors = {}
            for i in range(num_disks, 0, -1):
                self.rods['A'].append(i)
                self.disk_colors[i] = self.generate_color_for_disk(i, num_disks)

            self.draw_disks()
            self.start_new_game_button.pack_forget()
            self.back_to_main_menu_button.pack_forget()
            self.show_frame("Game")
            
  
    
    def generate_color_for_disk(self, disk_size, num_disks):
        if num_disks <= 3:
            colors = ['red', 'blue', 'black', 'green']  # Four colors for 4 or fewer disks
            return colors[disk_size % len(colors)]
        else:
            return "#{:06x}".format(random.randint(0, 0xFFFFFF))  # Random color

    def draw_disks(self):
        self.canvas.delete("disk")  # Only delete disks, not rods
        self.disks.clear()
          
        for rod, disks in self.rods.items():
            x = self.rod_positions[rod]
            for i, disk in enumerate(disks):
                y = 300 - ((i + 1) * 20)  # Adjusted to match rod height
                color = self.disk_colors[disk]  # Use stored color
                outline_color = "yellow" if i == len(disks) - 1 else "black"  # Highlight top disk with yellow outline
                rect = self.canvas.create_rectangle(x - disk * 10, y, x + disk * 10, y + 20, fill=color, outline=outline_color, tags="disk")
                self.disks.append((rect, rod, disk))
                if i == len(disks) - 1:  # Only bind events to the top disk
                    self.canvas.tag_bind(rect, "<ButtonPress-1>", self.on_disk_press)
                    self.canvas.tag_bind(rect, "<B1-Motion>", self.on_disk_drag)
                    self.canvas.tag_bind(rect, "<ButtonRelease-1>", self.on_disk_release)
                    
                    
    def on_disk_press(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
    
        # Find the disk and rod associated with the item
        disk_index = next(i for i, d in enumerate(self.disks) if d[0] == item)
        rod = self.disks[disk_index][1]
    
        # Initialize drag_data
        self.drag_data = {
            "item": item,
            "x": event.x,
            "y": event.y,
        }
    
        # Check if the disk is the topmost disk on its rod
        if self.rods[rod][-1] != self.disks[disk_index][2]:
            self.error_label.config(text="Error: You can only move the top disk.")
            return
    
        # Clear the error message if the user selects the correct disk
        self.error_label.config(text="")
    
        self.canvas.tag_raise(item)
    
    def on_disk_drag(self, event):
        if not self.drag_data:
            return  # Do nothing if drag_data is not set
        
        item = self.drag_data["item"]
        x = event.x
        y = event.y
        dx = x - self.drag_data["x"]
        dy = y - self.drag_data["y"]
        self.canvas.move(item, dx, dy)
        self.drag_data["x"] = x
        self.drag_data["y"] = y
    
    def on_disk_release(self, event):
        try:
            if not self.drag_data:
                return  # Do nothing if drag_data is not set

            item = self.drag_data["item"]
            x = event.x
            rod = self.get_rod(x)

            # Identify the disk being moved
            disk_index = next(i for i, d in enumerate(self.disks) if d[0] == item)
            current_rod = self.disks[disk_index][1]
            disk_size = self.disks[disk_index][2]

            # Validate the rod
            if rod is None or rod == current_rod:
                self.reset_disk(item)
                return

            # Check if the move is valid (placing the disk on an empty rod or on a larger disk)
            if not self.rods[rod] or self.rods[rod][-1] > disk_size:
                self.rods[current_rod].pop()
                self.rods[rod].append(disk_size)
                self.disks[disk_index] = (item, rod, disk_size)
                self.move_sequence.append((current_rod, rod))
                self.num_moves += 1
                self.draw_disks()
                self.check_win()
                self.error_label.config(text="")  # Clear any previous error messages
            else:
                self.error_label.config(text="Invalid move: You cannot place a larger disk on a smaller one.")
                self.reset_disk(item)
        except KeyError:
            self.error_label.config(text="Unexpected error: Unable to move disk. Please try again.")
            self.reset_disk(None)
        except Exception as e:
            self.error_label.config(text=f"Unexpected error: {str(e)}")
            self.reset_disk(None)