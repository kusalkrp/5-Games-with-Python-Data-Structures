import time
import tkinter as tk
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
import random
from tkinter import ttk


class TowerOfHanoi:
    def __init__(self, master):
        self.master = master
        self.master.title("Tower of Hanoi")
        self.master.geometry("800x650")  # Increased window size
        self.master.configure(bg="#ffffff")
        # Prevent the window from being resized
        self.master.resizable(False, False)

        self.name = tk.StringVar()
        self.num_disks = tk.StringVar()
        self.num_disks_int = tk.IntVar()
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
        try:
            if not firebase_admin._apps:  # Check if Firebase is already initialized
                cred = credentials.Certificate(
                    "pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json"
                )
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
        except ValueError as e:
            print(f"Error initializing Firebase: {e}")

        self.db = firestore.client()

    def create_frames(self):
        # Create frames for different stages
        self.frames["NameEntry"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["DiskEntry"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["Game"] = tk.Frame(self.master, bg="#ffffff")

        self.create_name_entry_frame()
        self.create_disk_entry_frame()
        self.create_game_frame()

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = frame

    def create_name_entry_frame(self):
        frame = self.frames["NameEntry"]

        tk.Label(
            frame,
            text="Enter Your Name:",
            font=("Arial", 18, "bold"),
            fg="#fa0000",
            bg="#ffffff",
        ).pack(pady=20)
        tk.Entry(frame, textvariable=self.name, font=("Arial", 14)).pack(pady=10)

        self.name_error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12))
        self.name_error_label.pack(pady=5)

        tk.Button(
            frame,
            text="Next",
            command=self.go_to_disk_entry_frame,
            font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",
        ).pack(pady=20)

    def create_disk_entry_frame(self):
        frame = self.frames["DiskEntry"]

        tk.Label(
            frame,
            text="Enter Number of Disks:",
            font=("Arial", 18, "bold"),
            fg="#fa0000",
            bg="#ffffff",
        ).pack(pady=20)
        
        # Validate that only whole positive numbers are accepted
        validate_command = self.master.register(self.validate_disk_entry)
        self.disk_entry = tk.Entry(
            frame,
            textvariable=self.num_disks,
            font=("Arial", 14),
            validate="key",
            validatecommand=(validate_command, "%P"),  # Validate the text value
        )
        self.disk_entry.pack(pady=10)

        self.disk_error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12))
        self.disk_error_label.pack(pady=5)

        tk.Button(
            frame,
            text="Start Game",
            command=self.start_game,
            font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",
        ).pack(pady=20)
        tk.Button(
            frame,
            text="Back",
            command=self.go_to_name_entry_frame,
            font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",
        ).pack(pady=10)

    def create_game_frame(self):
        frame = self.frames["Game"]

        # Create a menu bar
        menu_bar = tk.Menu(frame)
        frame.master.config(menu=menu_bar)  # Attach the menu bar to the main window

        # Create a 'Game' menu
        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menu", menu=game_menu)

        # Add 'Start New Game', 'View Results', and 'Exit' options
        game_menu.add_command(label="Start New Game", command=self.start_new_game)
        game_menu.add_command(label="View Results", command=self.create_results_frame)
        game_menu.add_command(label="Exit", command=self.go_back_to_main_menu)

        # Instructions and Error Labels
        self.instructions_label = tk.Label(
            frame,
            text=" ----- Move all disks from rod A to rod C -----",
            font=("Arial", 15),
            bg="#ffffff",
            fg="blue",
        )
        self.instructions_label.pack(pady=5)
        self.instructions_label = tk.Label(
            frame,
            text="----- Move only one disk at a time -----",
            font=("Arial", 15),
            bg="#ffffff",
            fg="blue",
        )
        self.instructions_label.pack(pady=10)

        self.error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12))
        self.error_label.pack(pady=5)

        # Canvas for drawing
        self.canvas = tk.Canvas(frame, width=600, height=300, bg="#eee0d3")
        self.canvas.pack(pady=20)

        # Result label
        self.result_label = tk.Label(frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Buttons
        self.start_new_game_button = tk.Button(
            frame,
            text="Start New Game",
            command=self.start_new_game,
            font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",
        )
        self.start_new_game_button.pack(pady=5)
        self.back_to_main_menu_button = tk.Button(
            frame,
            text="Back to Main Menu",
            command=self.go_back_to_main_menu,
            font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",
        )
        self.back_to_main_menu_button.pack(pady=20)

        # Initialize rods
        self.rods = {"A": [], "B": [], "C": []}
        self.rod_positions = {"A": 100, "B": 300, "C": 500}
        self.disks = []

        # Draw the rods and their labels
        rod_height = 200
        rod_width = 10
        rod_labels = ["A", "B", "C"]  # Labels for the rods

        for idx, (rod_name, x) in enumerate(self.rod_positions.items()):
            # Draw the rod
            self.canvas.create_rectangle(
                x - rod_width // 2,
                100,
                x + rod_width // 2,
                100 + rod_height,
                fill="black",
            )

            # Add the label
            label_x = x  # X position for the label, centered on the rod
            label_y = 100 - 20  # Y position for the label, slightly below the rod
            self.canvas.create_text(
                label_x,
                label_y,
                text=rod_labels[idx],
                font=("Arial", 14, "bold"),
                fill="red",
            )

    def validate_disk_entry(self, num_disks):
        """Validate the disk entry to ensure it is a whole positive number."""
        # Clear any previous error messages when the user starts typing
        if hasattr(self, 'disk_error_label'):
            self.disk_error_label.config(text="")

        if num_disks == "":
            if hasattr(self, 'disk_error_label'):
                self.disk_error_label.config(text="Please enter the number of disks")
            return False

        try:
            value = float(num_disks)
            if value.is_integer() and int(value) > 0:
                return True
            else:
                raise ValueError
        except ValueError:
            if hasattr(self, 'disk_error_label'):
                self.disk_error_label.config(text="Please enter a valid whole positive number")
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
        
        num_disks_str = self.num_disks.get()
        if not self.validate_disk_entry(num_disks_str):
            return

        num_disks = int(float(num_disks_str))  # Convert validated string to integer
        self.num_disks_int.set(num_disks)
        # Clear any error messages
        self.disk_error_label.config(text="")

        self.disk_error_label.config(text="")
        self.start_time = time.time()
        self.num_moves = 0
        self.move_sequence = []
        self.rods = {"A": [], "B": [], "C": []}
        self.disks = []

        # Initialize disks with colors
        self.disk_colors = {}
        for i in range(num_disks, 0, -1):
            self.rods["A"].append(i)
            self.disk_colors[i] = self.generate_color_for_disk(i, num_disks)

        self.draw_disks()
        self.start_new_game_button.pack_forget()
        self.back_to_main_menu_button.pack_forget()
        self.show_frame("Game")

    def generate_color_for_disk(self, disk_size, num_disks):
        if num_disks <= 3:
            colors = [
                "red",
                "blue",
                "black",
                "green",
            ]  # Four colors for 4 or fewer disks
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
                outline_color = (
                    "yellow" if i == len(disks) - 1 else "black"
                )  # Highlight top disk with yellow outline
                rect = self.canvas.create_rectangle(
                    x - disk * 10,
                    y,
                    x + disk * 10,
                    y + 20,
                    fill=color,
                    outline=outline_color,
                    tags="disk",
                )
                self.disks.append((rect, rod, disk))
                if i == len(disks) - 1:  # Only bind events to the top disk
                    self.canvas.tag_bind(rect, "<ButtonPress-1>", self.on_disk_press)
                    self.canvas.tag_bind(rect, "<B1-Motion>", self.on_disk_drag)
                    self.canvas.tag_bind(
                        rect, "<ButtonRelease-1>", self.on_disk_release
                    )

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
                self.error_label.config(
                    text="Invalid move: You cannot place a larger disk on a smaller one."
                )
                self.reset_disk(item)
        except KeyError:
            self.error_label.config(
                text="Unexpected error: Unable to move disk. Please try again."
            )
            self.reset_disk(None)
        except Exception as e:
            self.error_label.config(text=f"Unexpected error: {str(e)}")
            self.reset_disk(None)

    def reset_disk(self, item):
        if item is None:
            return  # Do nothing if item is None

        disk_index = next(i for i, d in enumerate(self.disks) if d[0] == item)
        rod = self.disks[disk_index][1]
        disk_size = self.disks[disk_index][2]
        x = self.rod_positions[rod]
        y = 300 - (len(self.rods[rod]) * 20)
        self.canvas.coords(item, x - disk_size * 10, y, x + disk_size * 10, y + 20)

    def get_rod(self, x):
        for rod, pos in self.rod_positions.items():
            if abs(x - pos) < 50:
                return rod
        return None

    def check_win(self):
        if len(self.rods["C"]) == self.num_disks_int.get():
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            player_name = self.name.get()  # Get the player name from the entry field
            self.result_label.config(
                text=f"{player_name}, you've solved the puzzle in {self.num_moves} moves and {elapsed_time:.2f} seconds!"
            )
            self.save_game_result()  # Update method name
            self.start_new_game_button.pack(pady=10)
            self.back_to_main_menu_button.pack(pady=10)

    def start_new_game(self):
        self.result_label.config(text="")
        self.error_label.config(text="")
        self.disk_error_label.config(text="")
        self.name_error_label.config(text="")
        self.name.set("")
        self.num_disks.set("")
        self.num_disks.set(0)
        self.show_frame("NameEntry")

    def go_back_to_main_menu(self):
        self.master.destroy()

    def save_game_result(self):
        player_name = self.name.get()
        num_disks = self.num_disks_int.get() 
        moves = self.num_moves
        time_taken = round(time.time() - self.start_time, 2)
        game_id = str(uuid.uuid4())  # Generate a unique ID for the game session

        move_sequence_str = ",".join(["".join(move) for move in self.move_sequence])

        game_data = {
            "game_id": game_id,
            "player_name": player_name,  # Store player name for querying
            "num_disks": num_disks,
            "moves": moves,
            "time_taken": time_taken,
            "move_sequence": move_sequence_str,  # Store the move sequence as a string
        }

        # Save the game result to Firebase with a unique document ID
        self.db.collection("TowerofHanoi").document(game_id).set(game_data)

        print(f"Game result saved to Firebase with game ID: {game_id}")

    def get_all_results(self):
        # Retrieve all documents from the 'TowerofHanoi' collection
        docs = self.db.collection("TowerofHanoi").stream()

        # Convert documents to dictionaries
        results = [doc.to_dict() for doc in docs]

        return results

    def create_results_frame(self):
        frame = tk.Frame(self.master)

        tk.Label(frame, text="Results for All Players:", font=("Arial", 14)).pack(pady=20)

        # Create Treeview
        columns = ("player_name", "num_disks", "moves", "move_sequence",  "time_taken")
        self.results_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.results_tree.pack(pady=10, fill="both", expand=True)

        # Define column headings
        self.results_tree.heading("player_name", text="Name", anchor="w")
        self.results_tree.heading("num_disks", text="Disks", anchor="w")
        self.results_tree.heading("moves", text="Moves", anchor="w")
        self.results_tree.heading("move_sequence", text="Movements", anchor="w")
        self.results_tree.heading("time_taken", text="Time Taken", anchor="w")

        # Define column widths
        self.results_tree.column("player_name", width=100, anchor="w")
        self.results_tree.column("num_disks", width=30, anchor="w")
        self.results_tree.column("moves", width=30, anchor="w")
        self.results_tree.column("move_sequence", width=400, anchor="w")
        self.results_tree.column("time_taken", width=60, anchor="w")

        tk.Button(
            frame,
            text="Show All Results",
            command=self.show_all_results,
            font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",
        ).pack(pady=20)
        
        tk.Button(
            frame,
            text="Start New Game",
            command=self.go_to_name_entry_frame,
            font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",
        ).pack(pady=10)
        
        self.frames["Results"] = frame  # Add to frames dictionary
        self.show_frame("Results")  # Show this frame

    def show_all_results(self):
        # Clear existing data in the Treeview
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
    
        results = self.get_all_results()

        if results:
            for result in results:
                self.results_tree.insert("", "end", values=(
                    result['player_name'],
                    result['num_disks'],
                    result['moves'],
                    result['move_sequence'],
                    result['time_taken']
                ))
        else:
            # If no results, you can optionally add a message or handle this case
            self.results_tree.insert("", "end", values=("No results found", "", "", "", ""))


if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoi(root)
    root.mainloop()
