import random
import time
import tkinter as tk
from tkinter import messagebox, ttk
import firebase_admin
from firebase_admin import credentials, firestore
from scipy.optimize import linear_sum_assignment

# Firebase setup
cred = credentials.Certificate('path_to_your_firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to generate random cost matrix
def generate_cost_matrix(n):
    return [[random.randint(20, 200) for _ in range(n)] for _ in range(n)]

# Function to find the optimal assignment using the Hungarian algorithm
def find_optimal_assignment(cost_matrix):
    start_time = time.time()
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    end_time = time.time()
    
    total_cost = sum(cost_matrix[row][col] for row, col in zip(row_ind, col_ind))
    execution_time = end_time - start_time
    
    return total_cost, execution_time, list(zip(row_ind, col_ind))

# Function to store results in Firebase
def store_results_in_firebase(cost_matrix, total_cost, execution_time, assignment):
    round_data = {
        'cost_matrix': cost_matrix,
        'total_cost': total_cost,
        'execution_time': execution_time,
        'assignment': assignment
    }
    
    db.collection('minimum_cost_game').add(round_data)

# Function to play the game
def play_game():
    try:
        n = int(task_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of tasks.")
        return

    if n <= 0:
        messagebox.showerror("Input Error", "The number of tasks must be greater than zero.")
        return
    
    cost_matrix = generate_cost_matrix(n)
    total_cost, execution_time, assignment = find_optimal_assignment(cost_matrix)
    
    # Display the results
    result_text = f"Total Minimum Cost: ${total_cost}\nTime Taken: {execution_time:.6f} seconds\nAssignment: {assignment}"
    result_label.config(text=result_text)
    
    # Display cost matrix in the UI
    for widget in matrix_frame.winfo_children():
        widget.destroy()  # Clear previous matrix

    for i in range(n):
        for j in range(n):
            ttk.Label(matrix_frame, text=f"${cost_matrix[i][j]}").grid(row=i, column=j, padx=5, pady=5)
    
    # Store the results in Firebase
    store_results_in_firebase(cost_matrix, total_cost, execution_time, assignment)

# Create the main UI window
root = tk.Tk()
root.title("Minimum Cost Task Assignment Game")

# Frame for task input
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, sticky="ew")

ttk.Label(input_frame, text="Number of Tasks (and Employees):").grid(row=0, column=0, padx=5, pady=5)
task_entry = ttk.Entry(input_frame, width=10)
task_entry.grid(row=0, column=1, padx=5, pady=5)

play_button = ttk.Button(input_frame, text="Play Game", command=play_game)
play_button.grid(row=0, column=2, padx=5, pady=5)

# Frame for displaying the cost matrix
matrix_frame = ttk.Frame(root, padding="10")
matrix_frame.grid(row=1, column=0, sticky="ew")

# Label for displaying results
result_label = ttk.Label(root, text="", padding="10")
result_label.grid(row=2, column=0, sticky="ew")

root.mainloop()
