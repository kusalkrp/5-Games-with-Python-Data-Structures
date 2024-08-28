import random
import time
import tkinter as tk
import firebase_admin
from firebase_admin import credentials, firestore
from tkinter import messagebox

class PredictValueIndexGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Predict the Value Index Game")
        self.master.geometry("800x600")
        self.master.configure(bg="#ffffff")
        self.master.resizable(False, False)

        self.player_name = tk.StringVar()
        self.target = None
        self.results = {}
        self.selected_algorithm = tk.StringVar(value="Binary Search")

        self.frames = {}
        self.current_frame = None

        self.initialize_firebase()
        self.create_frames()
        self.create_menu()  # Add menu creation method
        self.show_frame("NameEntry")

    def initialize_firebase(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate("pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json")
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            messagebox.showerror("Firebase Error", f"Failed to initialize Firebase: {e}")

    def create_frames(self):
        self.frames["NameEntry"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["AlgorithmSelection"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["Game"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["Result"] = tk.Frame(self.master, bg="#ffffff")

        self.create_name_entry_frame()
        self.create_algorithm_selection_frame()
        self.create_game_frame()
        self.create_result_frame()

    def create_menu(self):
        # Create a menu bar
        menu_bar = tk.Menu(self.master)

        # Create "Game" menu
        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="Start New Game", command=lambda: self.show_frame("NameEntry"))
        game_menu.add_command(label="View Results", command=self.view_results)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.quit)

        # Add "Game" menu to the menu bar
        menu_bar.add_cascade(label="Menu", menu=game_menu)

        # Set the menu bar on the root window
        self.master.config(menu=menu_bar)

    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = self.frames[frame_name]
        self.current_frame.pack(fill="both", expand=True)

    def create_name_entry_frame(self):
        frame = self.frames["NameEntry"]

        tk.Label(frame, text="Enter Your Name:", font=("Arial", 18, "bold"), fg="#fa0000", bg="#ffffff").pack(pady=20)
        tk.Entry(frame, textvariable=self.player_name, font=("Arial", 14)).pack(pady=10)

        self.name_error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12), bg="#ffffff")
        self.name_error_label.pack(pady=5)

        tk.Button(frame, text="Next", command=self.go_to_algorithm_selection, font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=20)

    def go_to_algorithm_selection(self):
        if not self.player_name.get():
            self.name_error_label.config(text="Name cannot be empty")
            return
        self.name_error_label.config(text="")
        self.show_frame("AlgorithmSelection")

    def create_algorithm_selection_frame(self):
        frame = self.frames["AlgorithmSelection"]

        tk.Label(frame, text="Select Algorithm:", font=("Arial", 18, "bold"), fg="#fa0000", bg="#ffffff").pack(pady=20)

        algorithms = ["Binary Search", "Jump Search", "Exponential Search", "Fibonacci Search", "Interpolation Search"]
        for algo in algorithms:
            tk.Radiobutton(frame, text=algo, variable=self.selected_algorithm, value=algo,
                           font=("Arial", 14), bg="#ffffff").pack(anchor="w", padx=20)

        tk.Button(frame, text="Start Game", command=self.start_game, font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=20)

    def create_game_frame(self):
        frame = self.frames["Game"]

        self.label_target = tk.Label(frame, text="", font=("Arial", 18, "bold"), bg="#ffffff")
        self.label_target.pack(pady=20)

        self.var = tk.IntVar()
        self.radio_buttons = []
        for _ in range(4):
            rb = tk.Radiobutton(frame, variable=self.var, font=("Arial", 14), bg="#ffffff")
            self.radio_buttons.append(rb)
            rb.pack(anchor="w")

        tk.Button(frame, text="Submit", command=self.submit_answer, font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=20)

    def create_result_frame(self):
        frame = self.frames["Result"]

        self.result_label = tk.Label(frame, text="", font=("Arial", 18, "bold"), bg="#ffffff")
        self.result_label.pack(pady=20)

        tk.Button(frame, text="Play Again", command=lambda: self.show_frame("NameEntry"), font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=10)
        tk.Button(frame, text="Exit", command=self.master.quit, font=("Arial", 12, "bold"),
                  bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2).pack(pady=10)

    def start_game(self):
        numbers = sorted(random.sample(range(1, 1000001), 5000))
        self.target = random.choice(numbers)
        algorithm = self.selected_algorithm.get()

        algorithms = {
            "Binary Search": self.binary_search,
            "Jump Search": self.jump_search,
            "Exponential Search": self.exponential_search,
            "Fibonacci Search": self.fibonacci_search,
            "Interpolation Search": self.interpolation_search
        }

        start_time = time.time()
        index = algorithms[algorithm](numbers, self.target)
        elapsed_time = time.time() - start_time
        self.results[algorithm] = {"index": index, "time": elapsed_time}

        self.update_game()
        self.show_frame("Game")

    def update_game(self):
        self.label_target.config(text=f"Predict the index of {self.target}:")
        correct_index = self.results[self.selected_algorithm.get()]["index"]
        options = [correct_index] + random.sample(range(0, 5000), 3)
        random.shuffle(options)
        for i, option in enumerate(options):
            self.radio_buttons[i].config(text=f"Index {option}", value=option)
        self.var.set(options[0])

    def submit_answer(self):
        choice = self.var.get()
        correct_index = self.results[self.selected_algorithm.get()]["index"]

        if choice == correct_index:
            messagebox.showinfo("Correct!", f"Well done, {self.player_name.get()}! You guessed correctly.")
            correct = True
        else:
            messagebox.showwarning("Incorrect", f"Sorry, {self.player_name.get()}. The correct index was {correct_index}.")
            correct = False

        self.save_result_to_firebase(choice, correct_index)
        self.update_result(correct, correct_index)
        self.show_frame("Result")

    def save_result_to_firebase(self, choice, correct_index):
        try:
            self.db.collection('predict_value_index').add({
                'player_name': self.player_name.get(),
                'correct_answer': self.target,
                'chosen_index': choice,
                'correct_index': correct_index,
                'search_method': self.selected_algorithm.get(),
                'time_taken': self.results[self.selected_algorithm.get()]["time"]
            })
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save data to Firebase: {e}")

    def update_result(self, correct, correct_index):
        if correct:
            self.result_label.config(text="Congratulations, you were correct!")
        else:
            self.result_label.config(text=f"Sorry, the correct index was {correct_index}.")

    def view_results(self):
        # This method will be called from the menu bar to view results
        messagebox.showinfo("View Results", "Functionality to view results can be implemented here.")
        # Add your logic to fetch and display results here

    # Search algorithms
    @staticmethod
    def binary_search(arr, x):
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

    @staticmethod
    def jump_search(arr, x):
        n = len(arr)
        step = int(n ** 0.5)
        prev = 0
        while arr[min(step, n)-1] < x:
            prev = step
            step += int(n ** 0.5)
            if prev >= n:
                return -1
        for i in range(prev, min(step, n)):
            if arr[i] == x:
                return i
        return -1

    @staticmethod
    def exponential_search(arr, x):
        if arr[0] == x:
            return 0
        i = 1
        while i < len(arr) and arr[i] <= x:
            i *= 2
        return PredictValueIndexGame.binary_search(arr[:min(i, len(arr))], x)

    @staticmethod
    def fibonacci_search(arr, x):
        fib_mm2 = 0  
        fib_mm1 = 1  
        fib_m = fib_mm1 + fib_mm2  
        n = len(arr)
        while fib_m < n:
            fib_mm2 = fib_mm1
            fib_mm1 = fib_m
            fib_m = fib_mm1 + fib_mm2
        offset = -1
        while fib_m > 1:
            i = min(offset + fib_mm2, n-1)
            if arr[i] < x:
                fib_m = fib_mm1
                fib_mm1 = fib_mm2
                fib_mm2 = fib_m - fib_mm1
                offset = i
            elif arr[i] > x:
                fib_m = fib_mm2
                fib_mm1 -= fib_mm2
                fib_mm2 = fib_m - fib_mm1
            else:
                return i
        if fib_mm1 and arr[offset+1] == x:
            return offset + 1
        return -1

    @staticmethod
    def interpolation_search(arr, x):
        low = 0
        high = len(arr) - 1
        while low <= high and arr[low] <= x <= arr[high]:
            pos = low + ((x - arr[low]) * (high - low)) // (arr[high] - arr[low])
            if arr[pos] == x:
                return pos
            elif arr[pos] < x:
                low = pos + 1
            else:
                high = pos - 1
        return -1

def main():
    root = tk.Tk()
    app = PredictValueIndexGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
