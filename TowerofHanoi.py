import tkinter as tk
import firebase_admin
from firebase_admin import credentials, firestore

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