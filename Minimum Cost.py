import random
import time
import tkinter as tk
from tkinter import messagebox, ttk
import firebase_admin
from firebase_admin import credentials, firestore
from scipy.optimize import linear_sum_assignment

class MinimumCostTaskAssignmentApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Minimum Cost Task Assignment Game")
        self.master.geometry("600x600")
        self.master.configure(bg="#ffffff")
        self.master.resizable(False, False)

        # Firebase initialization
        self.initialize_firebase()

        self.create_widgets()

    def initialize_firebase(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate('C:/Users/nilupul.r/hello/.venv/pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json')
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except ValueError as e:
            print(f"Error initializing Firebase: {e}")

    def create_widgets(self):
        # Frame for user input
        self.input_frame = ttk.Frame(self.master, padding="10")
        self.input_frame.grid(row=0, column=0, sticky="ew")

        ttk.Label(self.input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Number of Tasks (and Employees):").grid(row=1, column=0, padx=5, pady=5)
        self.task_entry = ttk.Entry(self.input_frame, width=10)
        self.task_entry.grid(row=1, column=1, padx=5, pady=5)

        play_button = ttk.Button(self.input_frame, text="Play Game", command=self.play_game)
        play_button.grid(row=1, column=2, padx=5, pady=5)

        # Frame for displaying the cost matrix
        self.matrix_frame = ttk.Frame(self.master, padding="10")
        self.matrix_frame.grid(row=1, column=0, sticky="ew")

        # Label for displaying results
        self.result_label = ttk.Label(self.master, text="", padding="10")
        self.result_label.grid(row=2, column=0, sticky="ew")

    def generate_cost_matrix(self, n):
        return [[random.randint(20, 200) for _ in range(n)] for _ in range(n)]

    def find_optimal_assignment(self, cost_matrix):
        start_time = time.time()
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        end_time = time.time()
        
        total_cost = sum(cost_matrix[row][col] for row, col in zip(row_ind, col_ind))
        execution_time = end_time - start_time
        
        return total_cost, execution_time, list(zip(row_ind, col_ind))

    def store_results_in_firebase(self, name, cost_matrix, total_cost, execution_time, assignment):
        round_data = {
            'name': name,
            'cost_matrix': cost_matrix,
            'total_cost': total_cost,
            'execution_time': execution_time,
            'assignment': assignment
        }
        self.db.collection('minimum_cost_game').add(round_data)
        print("Game result saved to Firebase.")

    def play_game(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Please enter your name.")
            return

        try:
            n = int(self.task_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of tasks.")
            return

        if n <= 0:
            messagebox.showerror("Input Error", "The number of tasks must be greater than zero.")
            return
        
        cost_matrix = self.generate_cost_matrix(n)
        total_cost, execution_time, assignment = self.find_optimal_assignment(cost_matrix)
        
        # Display the results
        result_text = f"Total Minimum Cost: ${total_cost}\nTime Taken: {execution_time:.6f} seconds\nAssignment: {assignment}"
        self.result_label.config(text=result_text)
        
        # Display cost matrix in the UI
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()  # Clear previous matrix

        for i in range(n):
            for j in range(n):
                ttk.Label(self.matrix_frame, text=f"${cost_matrix[i][j]}").grid(row=i, column=j, padx=5, pady=5)
        
        # Store the results in Firebase
        self.store_results_in_firebase(name, cost_matrix, total_cost, execution_time, assignment)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinimumCostTaskAssignmentApp(root)
    root.mainloop()
