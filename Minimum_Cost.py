import random
import time
import tkinter as tk
from tkinter import ttk
import firebase_admin
from firebase_admin import credentials, firestore
from scipy.optimize import linear_sum_assignment

# Initialize Firebase
cred = credentials.Certificate('pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class MinimumCostTaskAssignmentGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Minimum Cost Task Assignment Game")
        self.master.geometry("800x650")
        self.master.configure(bg="white")
        self.master.resizable(False, False)

        self.user_name = tk.StringVar()
        self.num_tasks = tk.IntVar()
        self.cost_matrix = []
        self.assignment = []
        self.total_cost = 0
        self.execution_time = 0

        self.frames = {}
        self.create_frames()
        self.create_menu()
        self.show_frame("Name")  # Show the first frame

    def create_frames(self):
        for F in ("Name", "Task", "Game", "Result", "Menu", "Matrix", "DatabaseResults"):
            frame = ttk.Frame(self.master, padding="10")
            frame.configure(style="TFrame")
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
    
        # Configure grid weights to make frames expand to fill the window
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
    
        self.create_name_frame()
        self.create_task_frame()
        self.create_game_frame()
       
        self.create_matrix_frame()
        self.create_database_results_frame()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=game_menu)
        game_menu.add_command(label="Start New Game", command=lambda: self.show_frame("Name"))
        game_menu.add_command(label="View Game Results", command=lambda: self.show_frame("DatabaseResults"))
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.quit)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def create_name_frame(self):
        frame = self.frames["Name"]

        ttk.Label(frame, text="Enter Your Name:", background="white").pack(pady=10)
        self.user_entry = ttk.Entry(frame, textvariable=self.user_name, width=30)
        self.user_entry.pack(pady=10)

        self.name_error_label = ttk.Label(frame, text="", foreground="red", background="white")
        self.name_error_label.pack(pady=5)

        tk.Button(
            frame,
            text="Next",
            command=self.validate_name,
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

    def create_task_frame(self):
        frame = self.frames["Task"]

        ttk.Label(frame, text="Enter Number of Tasks:", background="white").pack(pady=10)
        self.task_entry = ttk.Entry(frame, textvariable=self.num_tasks, width=10)
        self.task_entry.pack(pady=10)

        self.task_error_label = ttk.Label(frame, text="", foreground="red", background="white")
        self.task_error_label.pack(pady=5)

        tk.Button(
            frame,
            text="Start Game",
            command=self.validate_tasks,
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

    def create_game_frame(self):
        frame = self.frames["Game"]
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.result_frame = ttk.Frame(frame)
        self.result_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.result_text_widget = tk.Text(self.result_frame, wrap="word", font=("Arial", 12), height=5)
        self.result_text_widget.grid(row=0, column=0, sticky="ew")

        # Create a Treeview widget for the optimal assignment
        columns = ("Task", "Employee")
        self.assignment_tree = ttk.Treeview(self.result_frame, columns=columns, show="headings")
        self.assignment_tree.heading("Task", text="Task")
        self.assignment_tree.heading("Employee", text="Employee")
        self.assignment_tree.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        tk.Button(
        frame,
        text="Show Cost Matrix",
        command=lambda: self.show_frame("Matrix"),
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
    ).grid(row=1, column=0, pady=20)

        tk.Button(
        frame,
        text="Start New Game",
        command=lambda: self.show_frame("Name"),
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
    ).grid(row=2, column=0, pady=20)

    def create_matrix_frame(self):
        frame = self.frames["Matrix"]
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.matrix_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.matrix_frame, anchor="nw")

        tk.Button(
            frame,
            text="Back to Game",
            command=lambda: self.show_frame("Game"),
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
        ).grid(row=1, column=0, pady=20)

    def create_database_results_frame(self):
        frame = self.frames["DatabaseResults"]

        self.database_results_text = tk.Text(frame, wrap="word", font=("Arial", 12))
        self.database_results_text.pack(expand=True, fill="both", padx=10, pady=10)

        tk.Button(
            frame,
            text="Fetch Results",
            command=self.fetch_results_from_database,
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
            text="Back to Menu",
            command=lambda: self.show_frame("Menu"),
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

    def validate_name(self):
        name = self.user_name.get().strip()
        if not name:
            self.name_error_label.config(text="Name cannot be empty or spaces only.")
        else:
            self.name_error_label.config(text="")
            self.show_frame("Task")

    def validate_tasks(self):
        task_input = self.task_entry.get().strip()
        try:
            n = int(task_input)
            if n <= 0:
                raise ValueError("The number of tasks must be greater than 0.")
            self.task_error_label.config(text="")
            self.start_game()
        except ValueError:
            self.task_error_label.config(text="Please enter a valid positive integer for the number of tasks.")

    def start_game(self):
        self.generate_cost_matrix(self.num_tasks.get())
        self.find_optimal_assignment()
        self.save_result_to_database()
        self.display_results(self.num_tasks.get())
        self.show_frame("Game")

    def generate_cost_matrix(self, n):
        self.cost_matrix = [[random.randint(20, 200) for _ in range(n)] for _ in range(n)]

    def find_optimal_assignment(self):
        start_time = time.perf_counter()
        row_ind, col_ind = linear_sum_assignment(self.cost_matrix)
        end_time = time.perf_counter()

        self.total_cost = sum(self.cost_matrix[row][col] for row, col in zip(row_ind, col_ind))
        self.execution_time = end_time - start_time
        self.assignment = list(zip(row_ind, col_ind))

    def display_results(self, n):
        # Clear the previous content
        self.result_text_widget.delete(1.0, tk.END)

        # Insert the result text
        result_text = (
            f"User: {self.user_name.get()}\n"
            f"Total Minimum Cost: ${self.total_cost}\n"
            f"Time Taken: {self.execution_time:.6f} seconds\n"
            "Optimal Assignment:\n"
        )
        self.result_text_widget.insert(tk.END, result_text)

        # Apply formatting
        self.result_text_widget.tag_configure("header", font=("Arial", 14, "bold"), foreground="blue")
        self.result_text_widget.tag_configure("body", font=("Arial", 12))

        # Add tags to the text
        self.result_text_widget.tag_add("header", "1.0", "1.0 lineend")
        self.result_text_widget.tag_add("body", "2.0", tk.END)

        # Clear the previous Treeview content
        for item in self.assignment_tree.get_children():
            self.assignment_tree.delete(item)

        # Insert the assignment data
        for task, employee in self.assignment:
            self.assignment_tree.insert("", "end", values=(f"Task {task+1}", f"Employee {employee+1}"))

        # Increase the height of the Treeview
        self.assignment_tree.configure(height=20)

        # Show the result frame
        self.show_frame("Game")
        # Clear the matrix frame
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Create labels for the x-axis (tasks)
        for j in range(n):
            label = ttk.Label(self.matrix_frame, text=f"T{j+1}", background="white", font=("Arial", 10, "bold"))
            label.grid(row=0, column=j+1, padx=5, pady=5)

        # Create labels for the y-axis (employees)
        for i in range(n):
            label = ttk.Label(self.matrix_frame, text=f"Emp{i+1}", background="white", font=("Arial", 10, "bold"))
            label.grid(row=i+1, column=0, padx=5, pady=5)

        # Create the cost matrix with alternating background colors
        for i in range(n):
            for j in range(n):
                label = ttk.Label(self.matrix_frame, text=f"${self.cost_matrix[i][j]}", background="white")
                label.grid(row=i+1, column=j+1, padx=5, pady=5)
                if (i + j) % 2 == 0:
                    label.configure(background="#f0f0f0")
                else:
                    label.configure(background="#d0d0d0")

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Clear the matrix frame
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Create labels for the x-axis (tasks)
        for j in range(n):
            label = ttk.Label(self.matrix_frame, text=f"T{j+1}", background="white", font=("Arial", 10, "bold"))
            label.grid(row=0, column=j+1, padx=5, pady=5)

        # Create labels for the y-axis (employees)
        for i in range(n):
            label = ttk.Label(self.matrix_frame, text=f"Emp{i+1}", background="white", font=("Arial", 10, "bold"))
            label.grid(row=i+1, column=0, padx=5, pady=5)

        # Create the cost matrix with alternating background colors
        for i in range(n):
            for j in range(n):
                label = ttk.Label(self.matrix_frame, text=f"${self.cost_matrix[i][j]}", background="white")
                label.grid(row=i+1, column=j+1, padx=5, pady=5)
                if (i + j) % 2 == 0:
                    label.configure(background="#f0f0f0")
                else:
                    label.configure(background="#d0d0d0")

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def fetch_results_from_database(self):
        self.database_results_text.delete(1.0, tk.END)
        results = db.collection('minimum_cost_game_results').order_by('timestamp').stream()
        for result in results:
            data = result.to_dict()
            result_text = (
                f"User: {data['user_name']}\n"
                f"Number of Tasks: {data['num_tasks']}\n"
                f"Total Minimum Cost: ${data['total_cost']}\n"
                f"Time Taken: {data['execution_time']:.6f} seconds\n"
                f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['timestamp']))}\n"
                "----------------------------------------\n"
            )
            self.database_results_text.insert(tk.END, result_text)

    def save_result_to_database(self):
        data = {
            'user_name': self.user_name.get(),
            'num_tasks': self.num_tasks.get(),
            'total_cost': self.total_cost,
            'execution_time': self.execution_time,
            'timestamp': time.time()
        }
        db.collection('minimum_cost_game_results').add(data)

if __name__ == "__main__":
    root = tk.Tk()
    game = MinimumCostTaskAssignmentGame(root)
    root.mainloop()