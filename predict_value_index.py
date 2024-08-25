import random
import time
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect('game_results.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results (
             player_name TEXT, 
             correct_answer INTEGER, 
             chosen_index INTEGER, 
             search_method TEXT, 
             time_taken REAL)''')
conn.commit()

# Search algorithms
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

def exponential_search(arr, x):
    if arr[0] == x:
        return 0
    i = 1
    while i < len(arr) and arr[i] <= x:
        i = i * 2
    return binary_search(arr[:min(i, len(arr))], x)

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

# GUI Implementation
def start_game():
    numbers = sorted(random.sample(range(1, 1000001), 5000))
    target = random.choice(numbers)
    algorithms = {
        "Binary Search": binary_search,
        "Jump Search": jump_search,
        "Exponential Search": exponential_search,
        "Fibonacci Search": fibonacci_search,
        "Interpolation Search": interpolation_search
    }
    
    results = {}
    for name, algorithm in algorithms.items():
        start_time = time.time()
        index = algorithm(numbers, target)
        elapsed_time = time.time() - start_time
        results[name] = {"index": index, "time": elapsed_time}

    options = [results["Binary Search"]["index"]] + random.sample(range(0, 5000), 3)
    random.shuffle(options)

    def submit_answer():
        choice = int(var.get())
        player_name = entry_name.get()
        if choice == results["Binary Search"]["index"]:
            messagebox.showinfo("Correct!", f"Well done, {player_name}! You guessed correctly.")
            c.execute("INSERT INTO results (player_name, correct_answer, chosen_index, search_method, time_taken) VALUES (?, ?, ?, ?, ?)",
                      (player_name, target, choice, "Binary Search", results["Binary Search"]["time"]))
            conn.commit()
        else:
            messagebox.showwarning("Incorrect", f"Sorry, {player_name}. The correct index was {results['Binary Search']['index']}.")
        root.destroy()

    root = tk.Tk()
    root.title("Predict the Value Index")
    
    tk.Label(root, text="Enter your name:").pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text=f"Predict the index of {target}:").pack()
    var = tk.StringVar(value=options[0])
    for option in options:
        tk.Radiobutton(root, text=f"Index {option}", variable=var, value=option).pack()

    tk.Button(root, text="Submit", command=submit_answer).pack()

    root.mainloop()

start_game()
