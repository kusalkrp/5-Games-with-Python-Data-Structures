import random
import time
import tkinter as tk
import firebase_admin
from firebase_admin import credentials, firestore
from tkinter import messagebox, ttk

class PredictValueIndexGame:
    def __init__(self, master):
        # Initialize the main application window
        self.master = master
        self.master.title("Predict the Value Index Game")
        self.master.geometry("800x600")
        self.master.configure(bg="#ffffff")
        self.master.resizable(False, False)

        # Variables to store player's name, target value, search results, and selected algorithm
        self.player_name = tk.StringVar()
        self.target = None
        self.results = {}
        self.correct_index = None
        self.chosen_index = None

        # Initialize Firebase connection and create the UI frames
        self.initialize_firebase()
        self.create_frames()
        self.create_menu()
        self.show_frame("NameEntry")

    def initialize_firebase(self):
        # Initialize Firebase Firestore
        try:
            if not firebase_admin._apps:
                # Use a service account to authenticate
                cred = credentials.Certificate("pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json")
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            messagebox.showerror("Firebase Error", f"Failed to initialize Firebase: {e}")

    def create_frames(self):
        # Create different frames for the game
        self.frames = {
            "NameEntry": tk.Frame(self.master, bg="#ffffff"),
            "Game": tk.Frame(self.master, bg="#ffffff"),
            "Result": tk.Frame(self.master, bg="#ffffff"),
            "ViewResults": tk.Frame(self.master, bg="#ffffff")
        }

        # Create the content for each frame
        self.create_name_entry_frame()
        self.create_game_frame()
        self.create_result_frame()
        self.create_view_results_frame()

    def create_menu(self):
        # Create a menu bar for navigation
        menu_bar = tk.Menu(self.master)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="Start New Game", command=lambda: self.show_frame("NameEntry"))
        game_menu.add_command(label="View Results", command=self.view_results)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.quit)

        menu_bar.add_cascade(label="Menu", menu=game_menu)
        self.master.config(menu=menu_bar)

    def show_frame(self, frame_name):
        # Display the selected frame and hide the previous one
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)

    def create_name_entry_frame(self):
        # Create the frame where the player enters their name
        frame = self.frames["NameEntry"]

        tk.Label(frame, text="Enter Your Name:", font=("Arial", 18, "bold"), fg="#fa0000", bg="#ffffff").pack(pady=20)
        tk.Entry(frame, textvariable=self.player_name, font=("Arial", 14)).pack(pady=10)

        self.name_error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12), bg="#ffffff")
        self.name_error_label.pack(pady=5)

        tk.Button(frame, text="Next", command=self.start_game, font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=20)

    def create_game_frame(self):
        # Create the frame where the game takes place
        frame = self.frames["Game"]

        self.label_target = tk.Label(frame, text="", font=("Arial", 18, "bold"), bg="#ffffff")
        self.label_target.pack(pady=20)

        # Radio buttons for the player to choose an index
        self.var = tk.IntVar()
        self.radio_buttons = []
        for _ in range(4):
            rb = tk.Radiobutton(frame, variable=self.var, font=("Arial", 14), bg="#ffffff")
            self.radio_buttons.append(rb)
            rb.pack(anchor="w")

        tk.Button(frame, text="Submit", command=self.submit_answer, font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=20)

    def create_result_frame(self):
        # Create the frame that shows the result of the game
        frame = self.frames["Result"]

        self.result_label = tk.Label(frame, text="", font=("Arial", 18, "bold"), bg="#ffffff")
        self.result_label.pack(pady=20)

        tk.Button(frame, text="Play Again", command=lambda: self.show_frame("NameEntry"), font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=10)
        tk.Button(frame, text="Exit", command=self.master.quit, font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=10)

    def create_view_results_frame(self):
        # Create the frame that shows all the results from the database
        frame = self.frames["ViewResults"]

        columns = ["Player", "Target", "Correct Index", "Chosen Index",
                   "Binary Search Time", "Jump Search Time",
                   "Exponential Search Time", "Fibonacci Search Time", 
                   "Interpolation Search Time"]

        self.results_tree = ttk.Treeview(frame, columns=columns, show="headings")

        # Set column widths for better visibility
        column_widths = [100] * len(columns)  # Adjust the width if needed
        for col, width in zip(columns, column_widths):
            self.results_tree.column(col, width=width)

        # Set the headings
        for col in columns:
            self.results_tree.heading(col, text=col)

        self.results_tree.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Button(frame, text="Back to Menu", command=lambda: self.show_frame("NameEntry"), font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=10)

    def start_game(self):
        # Check if the player's name is empty
        if not self.player_name.get().strip():
            self.name_error_label.config(text="Name cannot be empty!")
            return

        # Start the game by selecting a target value and running all algorithms
        numbers = sorted(random.sample(range(1, 1000001), 5000))
        self.target = random.choice(numbers)

        # Run all algorithms and store their results
        self.results = {}
        algorithms = {
            "Binary Search": self.binary_search,
            "Jump Search": self.jump_search,
            "Exponential Search": self.exponential_search,
            "Fibonacci Search": self.fibonacci_search,
            "Interpolation Search": self.interpolation_search
        }

        for name, func in algorithms.items():
            start_time = time.perf_counter()
            index = func(numbers, self.target)
            end_time = time.perf_counter()
            self.results[name] = {"index": index, "time": end_time - start_time}

        # Update the game interface
        self.correct_index = self.results["Binary Search"]["index"]
        self.update_game()
        self.show_frame("Game")

    def update_game(self):
        # Update the game interface with the target value and possible indices
        self.label_target.config(text=f"Predict the index of {self.target}:")
        options = [self.correct_index] + random.sample(range(0, 5000), 3)  # Add 3 random options
        random.shuffle(options)  # Shuffle the options

        # Set the radio button labels to the options
        for i, rb in enumerate(self.radio_buttons):
            rb.config(text=f"Index {options[i]}", value=options[i])

    def submit_answer(self):
        # Submit the player's answer and check if it's correct
        self.chosen_index = self.var.get()
        result_text = (f"Correct index: {self.correct_index}\n"
                       f"Your answer: {self.chosen_index}\n"
                       )

        if self.chosen_index == self.correct_index:
            result_text += "\nCongratulations! You guessed correctly."
        else:
            result_text += "\nSorry, that's not correct."

        self.result_label.config(text=result_text)
        self.save_results()
        self.show_frame("Result")

    def save_results(self):
        # Save the results to Firebase
        result_data = {
            "Player": self.player_name.get(),
            "Target": self.target,
            "Correct Index": self.correct_index,
            "Chosen Index": self.chosen_index,
            "Binary Search Index": self.results["Binary Search"]["index"],
            "Binary Search Time": self.results["Binary Search"]["time"],
            "Jump Search Time": self.results["Jump Search"]["time"],
            "Exponential Search Time": self.results["Exponential Search"]["time"],
            "Fibonacci Search Time": self.results["Fibonacci Search"]["time"],
            "Interpolation Search Time": self.results["Interpolation Search"]["time"],
        }

        try:
            self.db.collection("PredictValueIndex").add(result_data)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save results: {e}")

    def view_results(self):
        # View all results saved in the Firebase Firestore
        try:
            self.results_tree.delete(*self.results_tree.get_children())  # Clear previous entries
            docs = self.db.collection("PredictValueIndex").stream()

            for doc in docs:
                data = doc.to_dict()
                self.results_tree.insert("", "end", values=[
                    data.get("Player"),
                    data.get("Target"),
                    data.get("Correct Index"),
                    data.get("Chosen Index"),
                    data.get("Binary Search Time"),
                    data.get("Jump Search Time"),
                    data.get("Exponential Search Time"),
                    data.get("Fibonacci Search Time"),
                    data.get("Interpolation Search Time")
                ])

            self.show_frame("ViewResults")

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to retrieve results: {e}")

    def binary_search(self, arr, x):
        # Implement binary search algorithm
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == x:
                return mid
            elif arr[mid] < x:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def jump_search(self, arr, x):
        # Implement jump search algorithm
        n = len(arr)
        step = int(n ** 0.5)
        prev = 0

        while arr[min(step, n) - 1] < x:
            prev = step
            step += int(n ** 0.5)
            if prev >= n:
                return -1

        for i in range(prev, min(step, n)):
            if arr[i] == x:
                return i
        return -1

    def exponential_search(self, arr, x):
        # Implement exponential search algorithm
        n = len(arr)
        if arr[0] == x:
            return 0
        i = 1
        while i < n and arr[i] <= x:
            i *= 2
        return self.binary_search(arr[:min(i, n)], x)

    def fibonacci_search(self, arr, x):
        # Implement fibonacci search algorithm
        n = len(arr)
        fib2, fib1 = 0, 1
        fib = fib2 + fib1
        while fib < n:
            fib2 = fib1
            fib1 = fib
            fib = fib2 + fib1

        offset = -1
        while fib > 1:
            i = min(offset + fib2, n - 1)
            if arr[i] < x:
                fib = fib1
                fib1 = fib2
                fib2 = fib - fib1
                offset = i
            elif arr[i] > x:
                fib = fib2
                fib1 -= fib2
                fib2 = fib - fib1
            else:
                return i
        if fib1 and arr[offset + 1] == x:
            return offset + 1
        return -1

    def interpolation_search(self, arr, x):
        # Implement interpolation search algorithm
        low, high = 0, len(arr) - 1
        while low <= high and x >= arr[low] and x <= arr[high]:
            if low == high:
                if arr[low] == x:
                    return low
                return -1
            pos = low + ((high - low) // (arr[high] - arr[low]) * (x - arr[low]))
            if arr[pos] == x:
                return pos
            elif arr[pos] < x:
                low = pos + 1
            else:
                high = pos - 1
        return -1


if __name__ == "__main__":
    root = tk.Tk()
    game = PredictValueIndexGame(root)
    root.mainloop()
