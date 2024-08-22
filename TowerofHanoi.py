import tkinter as tk

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

        self.create_frames()
        self.show_frame("NameEntry")

    def create_frames(self):
        # Create frames for different stages
        self.frames["NameEntry"] = tk.Frame(self.master)
        self.frames["DiskEntry"] = tk.Frame(self.master)
        self.frames["Game"] = tk.Frame(self.master)

        self.create_name_entry_frame()
        self.create_disk_entry_frame()
        self.create_game_frame()