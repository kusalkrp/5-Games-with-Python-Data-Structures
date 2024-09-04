import numpy as np
import time
import copy
import tkinter as tk
from tkinter import simpledialog, messagebox
from firebase_admin import credentials, firestore, initialize_app
from tkinter import ttk, messagebox
# Firebase setup
cred = credentials.Certificate('pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json')
initialize_app(cred)
db = firestore.client()

class TaskAssignmentGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Assignment Game")
        self.root.geometry("800x650")
        self.root.config(bg="white")

        self.create_menu()
        self.create_name_frame()

    def create_menu(self):
        menu_bar = tk.Menu(self.root, bg="#e74755", fg="white")
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg="#e74755")
        menu_bar.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="Start New Game", command=self.show_name_frame)
        file_menu.add_command(label="View Results", command=self.view_results)
        file_menu.add_command(label="Exit", command=self.root.quit)

    def create_name_frame(self):
        self.name_frame = tk.Frame(self.root, bg="white")
        self.name_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.name_frame, text="Enter Your Name:",font=("Arial", 12, "bold"), bg="white").pack(pady=20)
        self.name_entry = tk.Entry(self.name_frame)
        self.name_entry.pack(pady=10)

        self.warning_label = tk.Label(self.name_frame, text="", fg="red", bg="white")
        self.warning_label.pack(pady=10)

        tk.Button(self.name_frame, text="Next",  command=self.validate_name,            font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",).pack(pady=20)

    def create_task_frame(self):
        self.name_frame.pack_forget()
        self.task_frame = tk.Frame(self.root, bg="white")
        self.task_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.task_frame, text="Enter Number of Tasks:", font=("Arial", 12, "bold"), bg="white").pack(pady=20)
        self.task_entry = tk.Entry(self.task_frame)
        self.task_entry.pack(pady=10)

        self.task_warning_label = tk.Label(self.task_frame, text="", fg="red", bg="white")
        self.task_warning_label.pack(pady=10)

        tk.Button(self.task_frame, text="Start Game",  command=self.validate_tasks,            font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",).pack(pady=20)
        
    def create_guessing_window(self, cost_matrix, correct_assignment):
        self.guessing_window = tk.Toplevel(self.root)
        self.guessing_window.title("Guess the Optimal Assignment")
        self.guessing_window.geometry("1500x650")
        self.guessing_window.config(bg="white")

        tk.Label(self.guessing_window, text="Select the minimum cost value in each row:", bg="white", font=("Arial", 16)).pack(pady=10)

        rows, cols = cost_matrix.shape

        # Create a frame for the matrix with scrollbars
        matrix_frame = tk.Frame(self.guessing_window, bg="white")
        matrix_frame.pack(fill=tk.BOTH, expand=True)

        vsb = tk.Scrollbar(matrix_frame, orient="vertical")
        vsb.pack(side='right', fill='y')

        hsb = tk.Scrollbar(matrix_frame, orient="horizontal")
        hsb.pack(side='bottom', fill='x')

        canvas = tk.Canvas(matrix_frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        canvas.pack(side='left', fill='both', expand=True)

        vsb.config(command=canvas.yview)
        hsb.config(command=canvas.xview)

        # Create a frame inside the canvas
        matrix_canvas = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=matrix_canvas, anchor='nw')

        # Adding column headers
        tk.Label(matrix_canvas, text="", bg="white").grid(row=0, column=0, padx=5, pady=5)
        for j in range(cols):
            tk.Label(matrix_canvas, text=f"Task {j+1}", bg="white", font=("Arial", 12), relief="solid", width=10, anchor="center").grid(row=0, column=j+1, padx=1, pady=1)

        # Dictionary to hold the player's guesses and IntVars for each row
        self.player_guesses = {}
        self.row_vars = {}

        # Adding row headers and matrix cells
        for i in range(rows):
            tk.Label(matrix_canvas, text=f"Emp {i+1}", bg="white", font=("Arial", 12), relief="solid", width=10, anchor="center").grid(row=i+1, column=0, padx=1, pady=1)

            # Create an IntVar for this row to hold the selected task
            row_var = tk.IntVar()
            self.row_vars[i] = row_var

            for j in range(cols):
                value = cost_matrix[i, j]
                radio_button = tk.Radiobutton(matrix_canvas, text=f"${value:.2f}", variable=row_var, value=j,
                                            font=("Arial", 12), relief="solid", width=10, anchor="center")
                radio_button.grid(row=i+1, column=j+1, padx=1, pady=1)

        # Update canvas scroll region
        matrix_canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        tk.Button(self.guessing_window, text="Submit Guess", command=lambda: self.check_guesses(cost_matrix, correct_assignment), font=("Arial", 12, "bold"),
                bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2, width=20, height=1,
                activebackground="#e74755", activeforeground="white").pack(pady=10)


    def submit_guess(self):
        try:
            start_time = time.time()
            # Ensure cost_matrix and correct_assignment are accessible here
            self.check_guesses(self.cost_matrix, self.correct_assignment)
            end_time = time.time()
            elapsed_time = end_time - start_time
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return


    def check_guesses(self, cost_matrix, correct_assignment):
        player_assignment = []
        total_cost = 0
        elapsed_time = 0  # Define elapsed_time variable

        for i in range(cost_matrix.shape[0]):
            j = self.player_guesses.get(i)
            if j is not None:
                player_assignment.append({'row': i, 'col': j})
                total_cost += cost_matrix[i, j]

        correct_total_cost = self.calc_costs(cost_matrix, [(a['row'], a['col']) for a in correct_assignment])
        is_correct = total_cost == correct_total_cost

        # Pass elapsed_time to create_result_frame
        self.create_result_frame(cost_matrix, player_assignment, total_cost, elapsed_time, is_correct)
        self.guessing_window.destroy()

    def create_result_frame(self, cost_matrix, correct_assignment, total_cost, elapsed_time, is_correct):
        # Hide previous frames
        if hasattr(self, 'name_frame'):
            self.name_frame.pack_forget()
        if hasattr(self, 'task_frame'):
            self.task_frame.pack_forget()
        if hasattr(self, 'guessing_window'):
            self.guessing_window.destroy()  # Close the guessing window if it's open

        # Create result frame
        self.result_frame = tk.Frame(self.root, bg="white")
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        # Text widget for result summary
        self.result_text_widget = tk.Text(self.result_frame, height=4, width=80, wrap=tk.WORD, bg="white", font=("Arial", 12))
        self.result_text_widget.pack(padx=20, pady=20)
        
        start_time = time.time()
        row_ind, col_ind = self.hungarian_algorithm(cost_matrix)
        end_time = time.time()

        correct_assignment = list(zip(row_ind, col_ind))
        total_cost = self.calc_costs(cost_matrix, correct_assignment)
        elapsed_time = end_time - start_time

        # Convert numpy types to native Python types
        correct_assignment_list = [{'row': int(r), 'col': int(c)} for r, c in correct_assignment]  # List of dictionaries
        total_cost = float(total_cost)
        
        # Insert the result text
        result_text = (
            f"Total Minimum Cost: ${total_cost:.2f}\n"
            f"Time Taken: {elapsed_time:.8f} seconds\n"
            f"Result: {'You Guessed Correct!' if is_correct else 'You Guessed Wrong!'}"
        )
        self.result_text_widget.insert(tk.END, result_text)
        
        db.collection('minimum_cost_game_results').add({
                'player_name': self.player_name,  # Save the player's name
                'num_tasks': int(self.num_tasks),
                'total_cost': total_cost,
                'time_taken': elapsed_time
            })
        # Apply formatting
        self.result_text_widget.tag_configure("header", font=("Arial", 14, "bold"), foreground="blue")
        self.result_text_widget.tag_configure("body", font=("Arial", 12))

        # Add tags to the text
        self.result_text_widget.tag_add("header", "1.0", "1.0 lineend")
        self.result_text_widget.tag_add("body", "2.0", tk.END)

        # Apply font color to the result text
        if is_correct:
            self.result_text_widget.tag_configure("result", foreground="green")
        else:
            self.result_text_widget.tag_configure("result", foreground="red")
        self.result_text_widget.tag_add("result", "3.0", "3.0 lineend")

        # Treeview for correct assignments
        tk.Label(self.result_frame, text="Correct Assignment:", bg="white", font=("Arial", 14, "bold")).pack(pady=10)

        self.assignment_tree = ttk.Treeview(self.result_frame, columns=("Task", "Employee"), show="headings", height=10)
        self.assignment_tree.heading("Task", text="Task")
        self.assignment_tree.heading("Employee", text="Employee")
        self.assignment_tree.pack(pady=10)

        # Format the correct assignment list
        for a in correct_assignment_list:
            task = a['row'] + 1
            employee = a['col'] + 1
            self.assignment_tree.insert("", "end", values=(f"Task {task}", f"Employee {employee}"))

        # Buttons for navigation
        tk.Button(self.result_frame, text="Start New Game", command=self.show_name_frame, font=("Arial", 12, "bold"), bg="#f86b53", fg="white", padx=10, pady=5, relief="raised", borderwidth=2, width=20, height=1, activebackground="#e74755", activeforeground="white").pack(pady=20)

    def validate_name(self):
        self.player_name = self.name_entry.get().strip()  # Store the player's name
        if not self.player_name:
            self.warning_label.config(text="Name cannot be empty.")
        else:
            self.create_task_frame()
    def validate_tasks(self):
        try:
            self.num_tasks = int(self.task_entry.get().strip())
            if self.num_tasks <= 0:
                raise ValueError("Number of tasks must be a positive integer.")
        except ValueError:
            self.task_warning_label.config(text="Please enter a valid positive integer for the number of tasks.")
        else:
            self.run_game(self.num_tasks)

    def run_game(self, num_tasks):
        try:
            # Generate random cost matrix
            cost_matrix = np.random.randint(20, 201, size=(num_tasks, num_tasks))
            print(f"Cost matrix:\n{cost_matrix}")  # Debug output

            row_ind, col_ind = self.hungarian_algorithm(cost_matrix)
            correct_assignment = list(zip(row_ind, col_ind))
            # Convert numpy types to native Python types
            correct_assignment_list = [{'row': int(r), 'col': int(c)} for r, c in correct_assignment]  # List of dictionaries

            # Display guessing window
            self.create_guessing_window(cost_matrix, correct_assignment_list)
                        # Record results in Firebase
                        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")




    def hungarian_step(self, mat):
        for row_num in range(mat.shape[0]):
            mat[row_num] = mat[row_num] - np.min(mat[row_num])
        for col_num in range(mat.shape[1]):
            mat[:, col_num] = mat[:, col_num] - np.min(mat[:, col_num])
        return mat

    def min_zeros(self, zero_mat, mark_zero):
        min_row = [99999, -1]
        for row_num in range(zero_mat.shape[0]):
            if np.sum(zero_mat[row_num] == True) > 0 and min_row[0] > np.sum(zero_mat[row_num] == True):
                min_row = [np.sum(zero_mat[row_num] == True), row_num]
        zero_index = np.where(zero_mat[min_row[1]] == True)[0][0]
        mark_zero.append((min_row[1], zero_index))
        zero_mat[min_row[1], :] = False
        zero_mat[:, zero_index] = False

    def mark_matrix(self, mat):
        cur_mat = mat
        zero_bool_mat = (cur_mat == 0)
        zero_bool_mat_copy = zero_bool_mat.copy()
        marked_zero = []
        while (True in zero_bool_mat_copy):
            self.min_zeros(zero_bool_mat_copy, marked_zero)
        marked_zero_row = []
        marked_zero_col = []
        for i in range(len(marked_zero)):
            marked_zero_row.append(marked_zero[i][0])
            marked_zero_col.append(marked_zero[i][1])
        non_marked_row = list(set(range(cur_mat.shape[0])) - set(marked_zero_row))
        marked_cols = []
        check_switch = True
        while check_switch:
            check_switch = False
            for i in range(len(non_marked_row)):
                row_array = zero_bool_mat[non_marked_row[i], :]
                for j in range(row_array.shape[0]):
                    if row_array[j] == True and j not in marked_cols:
                        marked_cols.append(j)
                        check_switch = True
            for row_num, col_num in marked_zero:
                if row_num not in non_marked_row and col_num in marked_cols:
                    non_marked_row.append(row_num)
                    check_switch = True
        marked_rows = list(set(range(mat.shape[0])) - set(non_marked_row))
        return marked_zero, marked_rows, marked_cols

    def adjust_matrix(self, mat, cover_rows, cover_cols):
        cur_mat = mat
        non_zero_element = []
        for row in range(len(cur_mat)):
            if row not in cover_rows:
                for i in range(len(cur_mat[row])):
                    if i not in cover_cols:
                        non_zero_element.append(cur_mat[row][i])
        min_num = min(non_zero_element) if non_zero_element else 0

        for row in range(len(cur_mat)):
            if row not in cover_rows:
                for i in range(len(cur_mat[row])):
                    if i not in cover_cols:
                        cur_mat[row, i] = cur_mat[row, i] - min_num
        for row in range(len(cover_rows)):
            for col in range(len(cover_cols)):
                cur_mat[cover_rows[row], cover_cols[col]] = cur_mat[cover_rows[row], cover_cols[col]] + min_num

        return cur_mat

    def hungarian_algorithm(self, cost_matrix):
        n = cost_matrix.shape[0]
        cur_mat = copy.deepcopy(cost_matrix)

        cur_mat = self.hungarian_step(cur_mat)

        count_zero_lines = 0
        assignment = []

        while count_zero_lines < n:
            ans_pos, marked_rows, marked_cols = self.mark_matrix(cur_mat)
            count_zero_lines = len(marked_rows) + len(marked_cols)

            if count_zero_lines < n:
                cur_mat = self.adjust_matrix(cur_mat, marked_rows, marked_cols)

        row_ind = [pos[0] for pos in ans_pos]
        col_ind = [pos[1] for pos in ans_pos]

        return row_ind, col_ind

    def calc_costs(self, cost_matrix, assignment):
        total = 0
        for a in assignment:
            if a[0] < cost_matrix.shape[0] and a[1] < cost_matrix.shape[1]:  # Validate indices
                total += cost_matrix[a[0], a[1]]
        return total

    def show_cost_matrix(self, cost_matrix, assignment):
        cost_matrix_window = tk.Toplevel(self.root)
        cost_matrix_window.title("Cost Matrix")
        cost_matrix_window.geometry("800x800")
        cost_matrix_window.config(bg="white")

        tk.Label(cost_matrix_window, text="Cost Matrix:", bg="white", font=("Arial", 16)).pack(pady=10)

        rows, cols = cost_matrix.shape

        # Create a frame for the matrix with scrollbars
        matrix_frame = tk.Frame(cost_matrix_window, bg="white")
        matrix_frame.pack(fill=tk.BOTH, expand=True)

        vsb = tk.Scrollbar(matrix_frame, orient="vertical")
        vsb.pack(side='right', fill='y')

        hsb = tk.Scrollbar(matrix_frame, orient="horizontal")
        hsb.pack(side='bottom', fill='x')

        canvas = tk.Canvas(matrix_frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        canvas.pack(side='left', fill='both', expand=True)

        vsb.config(command=canvas.yview)
        hsb.config(command=canvas.xview)

        # Create a frame inside the canvas
        matrix_canvas = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=matrix_canvas, anchor='nw')

        # Adding column headers
        tk.Label(matrix_canvas, text="", bg="white").grid(row=0, column=0, padx=5, pady=5)
        for j in range(cols):
            tk.Label(matrix_canvas, text=f"Task {j+1}", bg="white", font=("Arial", 12), relief="solid", width=10, anchor="center").grid(row=0, column=j+1, padx=1, pady=1)

        # Adding row headers and matrix cells
        for i in range(rows):
            tk.Label(matrix_canvas, text=f"Emp {i+1}", bg="white", font=("Arial", 12), relief="solid", width=10, anchor="center").grid(row=i+1, column=0, padx=1, pady=1)
            for j in range(cols):
                is_highlighted = any(a['row'] == i and a['col'] == j for a in assignment)
                color = "#d0d0d0" if (i + j) % 2 == 0 else "#f0f0f0"
                if is_highlighted:
                    color = "#ffeb3b"  # Highlight color

                label = tk.Label(matrix_canvas, text=f"${cost_matrix[i, j]:.2f}", bg=color, font=("Arial", 12), relief="solid", width=10, anchor="center")
                label.grid(row=i+1, column=j+1, padx=1, pady=1)

        # Update canvas scroll region
        matrix_canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        tk.Button(cost_matrix_window, text="Close", command=cost_matrix_window.destroy, font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white",).pack(pady=10)

    def view_results(self):
        results_window = tk.Toplevel(self.root)
        results_window.title("Game Results")
        results_window.geometry("800x650")
        results_window.config(bg="white")

        tk.Label(results_window, text="Game History:", font=("Arial", 14), bg="white").pack(pady=20)

        # Create Treeview
        columns = ("player_name", "num_tasks", "total_cost", "time_taken")
        results_tree = ttk.Treeview(results_window, columns=columns, show="headings")
        results_tree.pack(pady=10, fill="both", expand=True)

        # Define column headings
        results_tree.heading("player_name", text="Player Name", anchor="w")
        results_tree.heading("num_tasks", text="Number of Tasks", anchor="w")
        results_tree.heading("total_cost", text="Total Cost", anchor="w")
        results_tree.heading("time_taken", text="Time Taken", anchor="w")

        # Define column widths
        results_tree.column("player_name", width=150, anchor="w")
        results_tree.column("num_tasks", width=150, anchor="w")
        results_tree.column("total_cost", width=150, anchor="w")
        results_tree.column("time_taken", width=150, anchor="w")

        # Fetch results from Firebase
        try:
            results = db.collection('minimum_cost_game_results').stream()
            for result in results:
                data = result.to_dict()
                player_name = data.get('player_name', 'Unknown')  # Use 'Unknown' if player_name is missing
                num_tasks = data.get('num_tasks', 'N/A')
                total_cost = f"${data.get('total_cost', 0.0):.2f}"
                time_taken = f"{data.get('time_taken', 0.0):.8f} seconds"

                results_tree.insert("", "end", values=(
                    player_name,
                    num_tasks,
                    total_cost,
                    time_taken
                ))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching results: {str(e)}")

    def show_name_frame(self):
        if hasattr(self, 'task_frame'):
            self.task_frame.pack_forget()
        if hasattr(self, 'result_frame'):
            self.result_frame.pack_forget()
        if hasattr(self, 'cost_matrix_window'):
            self.cost_matrix_window.destroy()

        self.name_frame.pack(fill=tk.BOTH, expand=True)

# Tkinter main loop
if __name__ == "__main__":
    root = tk.Tk()
    game = TaskAssignmentGame(root)
    root.mainloop()
