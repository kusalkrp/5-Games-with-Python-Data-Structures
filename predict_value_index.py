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
        self.selected_algorithm = tk.StringVar(value="Binary Search")

        # Dictionaries to store different frames and the current frame
        self.frames = {}
        self.current_frame = None

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
        self.frames["NameEntry"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["AlgorithmSelection"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["Game"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["Result"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["ViewResults"] = tk.Frame(self.master, bg="#ffffff")

        # Create the content for each frame
        self.create_name_entry_frame()
        self.create_algorithm_selection_frame()
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
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = self.frames[frame_name]
        self.current_frame.pack(fill="both", expand=True)

    def create_name_entry_frame(self):
        # Create the frame where the player enters their name
        frame = self.frames["NameEntry"]

        tk.Label(frame, text="Enter Your Name:", font=("Arial", 18, "bold"), fg="#fa0000", bg="#ffffff").pack(pady=20)
        tk.Entry(frame, textvariable=self.player_name, font=("Arial", 14)).pack(pady=10)

        self.name_error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12), bg="#ffffff")
        self.name_error_label.pack(pady=5)

        tk.Button(frame, text="Next", command=self.go_to_algorithm_selection, font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=20)

    def go_to_algorithm_selection(self):
        # Validate the player's name and proceed to algorithm selection
        if not self.player_name.get():
            self.name_error_label.config(text="Name cannot be empty")
            return
        self.name_error_label.config(text="")
        self.show_frame("AlgorithmSelection")

    def create_algorithm_selection_frame(self):
        # Create the frame where the player selects the search algorithm
        frame = self.frames["AlgorithmSelection"]

        tk.Label(frame, text="Select Algorithm:", font=("Arial", 18, "bold"), fg="#fa0000", bg="#ffffff").pack(pady=20)

        algorithms = ["Binary Search", "Jump Search", "Exponential Search", "Fibonacci Search", "Interpolation Search"]
        for algo in algorithms:
            tk.Radiobutton(frame, text=algo, variable=self.selected_algorithm, value=algo,
                           font=("Arial", 14), bg="#ffffff").pack(anchor="w", padx=20)

        tk.Button(frame, text="Start Game", command=self.start_game, font=("Arial", 12, "bold"),
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

        # Treeview to display the results in a table-like structure
        self.results_tree = ttk.Treeview(frame, columns=("Player", "Correct Answer", "Chosen Index", "Correct Index", "Algorithm", "Time"), show="headings")

        # Set column widths for better visibility
        self.results_tree.column("Player", width=50)
        self.results_tree.column("Correct Answer", width=50)
        self.results_tree.column("Chosen Index", width=50)
        self.results_tree.column("Correct Index", width=50)
        self.results_tree.column("Algorithm", width=50)
        self.results_tree.column("Time", width=120)

        # Set the headings
        self.results_tree.heading("Player", text="Player")
        self.results_tree.heading("Correct Answer", text="Correct Answer")
        self.results_tree.heading("Chosen Index", text="Chosen Index")
        self.results_tree.heading("Correct Index", text="Correct Index")
        self.results_tree.heading("Algorithm", text="Algorithm")
        self.results_tree.heading("Time", text="Time Taken (s)")

        self.results_tree.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Button(frame, text="Back to Menu", command=lambda: self.show_frame("NameEntry"), font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=10)

    def start_game(self):
        # Start the game by selecting a target value and running the selected algorithm
        numbers = sorted(random.sample(range(1, 1000001), 5000))
        self.target = random.choice(numbers)
        algorithm = self.selected_algorithm.get()

        # Mapping of algorithms to their corresponding functions
        algorithms = {
            "Binary Search": self.binary_search,
            "Jump Search": self.jump_search,
            "Exponential Search": self.exponential_search,
            "Fibonacci Search": self.fibonacci_search,
            "Interpolation Search": self.interpolation_search
        }

        # Time the execution of the selected search algorithm
        start_time = time.perf_counter()  # Start the timer using perf_counter
        index = algorithms[algorithm](numbers, self.target)
        end_time = time.perf_counter()  # End the timer using perf_counter
        elapsed_time = end_time - start_time  # Calculate elapsed time

        # Store the result of the search
        self.results[algorithm] = {"index": index, "time": elapsed_time}

        self.update_game()
        self.show_frame("Game")

    def update_game(self):
        # Update the game interface with the target value and possible indices
        self.label_target.config(text=f"Predict the index of {self.target}:")
        correct_index = self.results[self.selected_algorithm.get()]["index"]
        options = [correct_index] + random.sample(range(0, 5000), 3)  # Add 3 random options
        random.shuffle(options)  # Shuffle the options

        # Set the radio button labels to the options
        for i, rb in enumerate(self.radio_buttons):
            rb.config(text=f"Index {options[i]}", value=options[i])

    def submit_answer(self):
        # Submit the player's answer and check if it's correct
        chosen_index = self.var.get()
        algorithm = self.selected_algorithm.get()
        correct_index = self.results[algorithm]["index"]
        is_correct = chosen_index == correct_index

        # Show the result to the player
        self.result_label.config(text=f"Your answer: {chosen_index}\nCorrect answer: {correct_index}\nTime taken: {self.results[algorithm]['time']:.8f} seconds")
        self.show_frame("Result")

        # Store the result in Firebase
        self.save_result(chosen_index, correct_index)

    def save_result(self, chosen_index, correct_index):
        # Save the player's result to the Firebase Firestore database
        result_data = {
            "Player": self.player_name.get(),
            "Target": self.target,
            "Chosen Index": chosen_index,
            "Correct Index": correct_index,
            "Algorithm": self.selected_algorithm.get(),
            "Time Taken": self.results[self.selected_algorithm.get()]["time"],
            "Timestamp": firestore.SERVER_TIMESTAMP
        }
        try:
            self.db.collection("PredictValueIndex").add(result_data)
            print("Result saved to Firebase.")
        except Exception as e:
            print(f"Error saving result to Firebase: {e}")
            messagebox.showerror("Firebase Error", f"Failed to save result to Firebase: {e}")

    def view_results(self):
        # Retrieve all results from Firebase and display them in the View Results frame
        self.show_frame("ViewResults")
        try:
            results = self.db.collection("PredictValueIndex").stream()
            self.results_tree.delete(*self.results_tree.get_children())  # Clear previous entries

            for result in results:
                data = result.to_dict()
                self.results_tree.insert("", "end", values=(
                    data.get("Player", "N/A"),
                    data.get("Target", "N/A"),
                    data.get("Chosen Index", "N/A"),
                    data.get("Correct Index", "N/A"),
                    data.get("Algorithm", "N/A"),
                    f"{data.get('Time Taken', 0):.8f}"
                ))
        except Exception as e:
            print(f"Error retrieving results from Firebase: {e}")
            messagebox.showerror("Firebase Error", f"Failed to retrieve results from Firebase: {e}")

    # Implementations of search algorithms
    def binary_search(self, arr, target):
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def jump_search(self, arr, target):
        length = len(arr)
        jump = int(length ** 0.5)
        left, right = 0, 0
        while left < length and arr[left] <= target:
            right = min(length - 1, left + jump)
            if arr[left] <= target <= arr[right]:
                break
            left += jump
        if left >= length or arr[left] > target:
            return -1
        right = min(length - 1, right)
        for i in range(left, right + 1):
            if arr[i] == target:
                return i
        return -1

    def exponential_search(self, arr, target):
        if arr[0] == target:
            return 0
        index = 1
        while index < len(arr) and arr[index] <= target:
            index *= 2
        return self.binary_search(arr[:min(index, len(arr))], target)

    def fibonacci_search(self, arr, target):
        fib_m2 = 0
        fib_m1 = 1
        fib_m = fib_m2 + fib_m1
        while fib_m < len(arr):
            fib_m2 = fib_m1
            fib_m1 = fib_m
            fib_m = fib_m2 + fib_m1
        offset = -1
        while fib_m > 1:
            i = min(offset + fib_m2, len(arr) - 1)
            if arr[i] < target:
                fib_m = fib_m1
                fib_m1 = fib_m2
                fib_m2 = fib_m - fib_m1
                offset = i
            elif arr[i] > target:
                fib_m = fib_m2
                fib_m1 = fib_m1 - fib_m2
                fib_m2 = fib_m - fib_m1
            else:
                return i
        if fib_m1 and arr[offset + 1] == target:
            return offset + 1
        return -1

    def interpolation_search(self, arr, target):
        low, high = 0, len(arr) - 1
        while low <= high and target >= arr[low] and target <= arr[high]:
            if low == high:
                if arr[low] == target:
                    return low
                return -1
            pos = low + ((high - low) // (arr[high] - arr[low]) * (target - arr[low]))
            if arr[pos] == target:
                return pos
            if arr[pos] < target:
                low = pos + 1
            else:
                high = pos - 1
        return -1

# Initialize the game
root = tk.Tk()
game = PredictValueIndexGame(root)
root.mainloop()
