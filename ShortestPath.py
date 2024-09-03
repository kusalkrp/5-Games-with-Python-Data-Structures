import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import sqlite3
import time
import heapq
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import json
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from tkinter import ttk

class ShortestPath:
    def __init__(self, master):
        self.master = master
        self.master.title("Shortest Path Game")
        self.master.geometry("1510x1000")  
        self.master.configure(bg="#ffffff")
        self.master.resizable(False, False)
        
        self.player_name = tk.StringVar()
        self.cities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.graph = {}
        self.matrix_labels = []
        self.start_city_var = None
        self.canvas = None
        self.graph_plot = None
        print("start")
        self.distance_entries = {}
        self.path_entries = {}
        self.start_time = None

        self.frames = {}
        self.current_frame = None

        self.initialize_firebase()
        self.create_frames()
        # self.create_menu()
        self.show_frame("NameEntry")
        
    def initialize_firebase(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(r'pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json')  #add path
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            messagebox.showerror("Firebase Error", f"Failed to initialize Firebase: {e}")
            
    def create_frames(self):
        self.frames["NameEntry"] = tk.Frame(self.master, bg="#ffffff")
        self.frames["Play"] = tk.Frame(self.master, bg="#ffffff")

        self.create_name_entry_frame()
        self.create_play_game_frame()
        
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
        tk.Entry(frame, textvariable=self.player_name, font=("Arial", 14)).pack(pady=10)

        self.player_name_error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12))
        self.player_name_error_label.pack(pady=5)

        tk.Button(
            frame,
            text="Next",
            command=self.go_to_game_frame,
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
    
    def create_play_game_frame(self):
        frame = self.frames["Play"]

        # Create a menu bar
        menu_bar = tk.Menu(frame)
        frame.master.config(menu=menu_bar)  # Attach the menu bar to the main window

        # Create a 'Game' menu
        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menu", menu=game_menu)

        # Add 'Start New Game', 'View Results', and 'Exit' options
        game_menu.add_command(label="Start New Game", command=self.start_new_game)
        game_menu.add_command(label="View Results", command=self.create_view_results_frame)
        game_menu.add_command(label="Exit", command=self.exit)
        self.start_city_var = tk.StringVar(frame)
        
        style = ttk.Style()

        # Configure the style for a custom frame
        style.configure('Custom.TFrame', background='#ffffff')
        
        lbl_frame = ttk.Frame(frame, width=100, height=100, borderwidth=10, style='Custom.TFrame')
        lbl_frame.pack(side="top")

        # Instructions and Error Labels
        self.instructions_label = tk.Label(
            lbl_frame,
            text="The starting city is: ",
            font=("Arial", 15),
            bg="#ffffff",
            fg="blue",
        )

        self.instructions_label.pack(pady=5, side="left")
        self.instructions_label_city = tk.Label(
            lbl_frame,
            textvariable=self.start_city_var,
            font=("Arial", 15),
            bg="#ffffff",
            fg="blue",
        )
        self.instructions_label_city.pack(pady=5, side="left")

        self.error_label = tk.Label(lbl_frame, text="", fg="red", font=("Arial", 12))
        self.error_label.pack(pady=5)

        tb_input = ttk.Frame(frame, width=1500, height=700, borderwidth=10, style='Custom.TFrame')
        tb_input.pack_propagate(False)
        tb_input.place(x=0, y=70)
        
        table_frame = ttk.Frame(tb_input, width=100, height=100, borderwidth=10, style='Custom.TFrame')
        table_frame.pack(side="left")

        for i, city in enumerate(self.cities):
            # Row and column headers with enhanced styles
            tk.Label(table_frame, text=city, borderwidth=2, relief="solid", padx=15, pady=10, 
                    font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333333").grid(row=len(self.cities) + 1, column=i + 1, sticky="nsew")
            tk.Label(table_frame, text=city, borderwidth=2, relief="solid", padx=15, pady=10, 
                    font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333333").grid(row=i + 1, column=0, sticky="nsew")

        # Matrix labels with enhanced styles and diagonal logic
        self.matrix_labels = [[tk.Label(table_frame, text="", borderwidth=1, relief="solid", padx=15, pady=10, 
                                font=("Arial", 12), bg="#ffffff", fg="#333333") for _ in self.cities] for _ in self.cities]

        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                if j < i:
                    # Normal values on the left side of the diagonal
                    self.matrix_labels[i][j].grid(row=i + 1, column=j + 1, sticky="nsew")
                elif j == i:
                    # Diagonal cells
                    self.matrix_labels[i][j].config(bg="#cccccc")  # Highlight diagonal (optional)
                    self.matrix_labels[i][j].grid(row=i + 1, column=j + 1, sticky="nsew")
                else:
                    # Hide values on the right side of the diagonal
                    self.matrix_labels[i][j].config(text="", bg="#000000", fg="#000000")  # Set background to indicate it's hidden
                    self.matrix_labels[i][j].grid(row=i + 1, column=j + 1, sticky="nsew")

        input_frame = ttk.Frame(tb_input, width=900, height=600, borderwidth=10, style='Custom.TFrame')
        input_frame.pack_propagate(False)
        input_frame.pack(side="right")

        self.distance_entries = {}
        self.path_entries = {}
        self.distance_error_labels = {}  # To store error labels for distance inputs
        self.path_error_labels = {}  # To store error labels for path inputs

        for i, city in enumerate(self.cities):
            # Create a container frame for each row to align all widgets horizontally
            row_frame_val = tk.Frame(input_frame, bg="#ffffff")
            row_frame_val.pack(fill="x", padx=5, pady=2)
            
            row_frame_error = tk.Frame(input_frame, bg="#ffffff")
            row_frame_error.pack(fill="x", padx=5, pady=2)

            # Distance entry label
            tk.Label(row_frame_val, text=f"Distance to {city}:", font=("Arial", 13, "bold"), fg="#587cd6", bg="#ffffff").pack(side="left", padx=5)
    
            # Distance entry field
            self.distance_entries[city] = tk.Entry(row_frame_val, font=("Arial", 13), width=10)
            self.distance_entries[city].pack(side="left", padx=5)

            # Error label for distance entry
            self.distance_error_labels[city] = tk.Label(row_frame_error, text="", fg="red", font=("Arial", 13), bg="#ffffff")
            self.distance_error_labels[city].pack(side="left", padx=5)
    
            # Path entry field
            self.path_entries[city] = tk.Entry(row_frame_val, font=("Arial", 13))
            self.path_entries[city].pack(side="right", padx=5)
            
            # Path entry label
            tk.Label(row_frame_val, text=f"Path to {city} (comma-separated):", font=("Arial", 13, "bold"), fg="#587cd6", bg="#ffffff").pack(side="right", padx=5)

            # Error label for path entry
            self.path_error_labels[city] = tk.Label(row_frame_error, text="", fg="red", font=("Arial", 13), bg="#ffffff")
            self.path_error_labels[city].pack(side="right", padx=5)

        btn_frame = ttk.Frame(frame, width=500, height=100, borderwidth=10, style='Custom.TFrame')
        btn_frame.pack_propagate(False)
        btn_frame.place(x=500, y=850)
        
        # Buttons
        self.start_game_button = tk.Button(
            btn_frame,
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
        )
        self.start_game_button.pack(pady=15, side="left")
        
        self.check_answer_button = tk.Button(
            btn_frame,
            text="Submit",
            command=self.check_answer,
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
        self.check_answer_button.pack(pady=15, side="right")
        
        
        self.win_label = tk.Label(frame, text="", fg="blue", font=("Arial", 13), bg="#ffffff")
        self.win_label.place(x=450, y=800)
            
    def go_to_game_frame(self):
        if not self.player_name.get():
            self.player_name_error_label.config(text="Name cannot be empty")
            return
        self.player_name_error_label.config(text="")
        self.show_frame("Play")
        
    def start_game(self):
        self.graph = self.generate_random_graph()
        self.display_graph()
        self.start_time = time.time()

        # Randomly select a starting city and set it in the dropdown
        selected_city = random.choice(self.cities)
        self.start_city_var.set(selected_city)
        
    def generate_random_graph(self):
        graph = {city: {} for city in self.cities}
        for i in range(len(self.cities)):
            for j in range(i + 1, len(self.cities)):  # Ensure no duplicate edges
                if i != j:
                    # 30% chance of a path between city i and city j
                    if random.random() < 0.3:
                        distance = random.randint(5, 50)
                        graph[self.cities[i]][self.cities[j]] = distance
                        graph[self.cities[j]][self.cities[i]] = distance

        for city in self.cities:
            if not graph[city]:  # If the city has no edges
                # Randomly connect this city to another city
                while True:
                    other_city = random.choice(self.cities)
                    if other_city != city:
                        # Add a connection
                        distance = random.randint(5, 50)
                        graph[city][other_city] = distance
                        graph[other_city][city] = distance
                        break
        return graph
                        
    def display_graph(self):
        for i, city1 in enumerate(self.cities):
            for j, city2 in enumerate(self.cities):
                if city1 in self.graph and city2 in self.graph[city1]:
                    self.matrix_labels[i][j].config(text=str(self.graph[city1][city2]))
                else:
                    self.matrix_labels[i][j].config(text="")
                    
    def validate_inputs(self):
        valid = True
        # Validate distance entries
        for city, entry in self.distance_entries.items():
            distance = entry.get()
            try:
                # Check if the distance is a non-negative integer or float
                if not (distance.isdigit() or float(distance) >= 0):
                    raise ValueError("Invalid distance")
                self.distance_error_labels[city].config(text="")  # Clear error message if valid
            except ValueError:
                self.distance_error_labels[city].config(text="Please enter a valid non-negative number")
                valid = False

        # Validate path entries
        for city, entry in self.path_entries.items():
            path = entry.get().split(',')
            # Check if each city in the path is in the list of cities
            if not all(p.strip() in self.cities for p in path):
                self.path_error_labels[city].config(text="Invalid city in path")
                valid = False
            else:
                self.path_error_labels[city].config(text="")  # Clear error message if valid

        return valid
    
    
    def bellman_ford(self, graph, start):
        distances = {city: float('inf') for city in graph}
        distances[start] = 0
        predecessors = {city: None for city in graph}

        for _ in range(len(graph) - 1):
            for u in graph:
                for v in graph[u]:
                    if distances[u] + graph[u][v] < distances[v]:
                        distances[v] = distances[u] + graph[u][v]
                        predecessors[v] = u

        # Check for negative weight cycles
        for u in graph:
            for v in graph[u]:
                if distances[u] + graph[u][v] < distances[v]:
                    return None, None
        return distances, predecessors
    
    #dijkstra algo
    def dijkstra(self, graph, start):
        distances = {city: float('inf') for city in graph}
        distances[start] = 0
        predecessors = {city: None for city in graph}
        priority_queue = [(0, start)]
        visited = set()

        while priority_queue:
            current_distance, current_city = heapq.heappop(priority_queue)

            if current_city in visited:
                continue
            visited.add(current_city)

            for neighbor, weight in graph[current_city].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_city
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, predecessors                
                
    def check_answer(self):
        #validation statment
        if not self.validate_inputs():
            print("Invalid input detected")
            return
        player_name = self.player_name.get()
        start_city = self.start_city_var.get()

        if not player_name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        start_time_bell = time.perf_counter()
        bellman_result, bellman_predecessors = self.bellman_ford(self.graph, start_city)
        print('bell ans ' + json.dumps(bellman_result))
        print('bell pred ' + json.dumps(bellman_predecessors))
        bellman_time = time.perf_counter() - start_time_bell
        print('Bellman-Ford Execution Time:', bellman_time)

        start_time_dij = time.perf_counter()
        dijkstra_result, dijkstra_predecessors = self.dijkstra(self.graph, start_city)
        print('dijk ans ' + json.dumps(dijkstra_result))
        print('dijk pred ' + json.dumps(dijkstra_predecessors))
        dijkstra_time = time.perf_counter() - start_time_dij
        print('Dijkstra Execution Time:', dijkstra_time)



        if bellman_result and dijkstra_result:
            correct_answer = dijkstra_result  # Since graph has no negative weights
            correct_paths = {city: self.reconstruct_path(dijkstra_predecessors, start_city, city) for city in self.cities if city != start_city}
            print("correct_paths= "+json.dumps(correct_paths))

            # Retrieve the player's answers from the entry fields
            player_answer = {}
            player_paths = {}
            all_correct = True

            for city in self.cities:
                # if city != start_city:
                    distance_str = self.distance_entries[city].get()
                    path_str = self.path_entries[city].get()
                    print(" ans " + json.dumps(distance_str))
                    print(" str " + json.dumps(path_str))

                    # Check if distance_str or path_str is null or empty
                    if not distance_str or not path_str:
                        messagebox.showerror("Error", f"Invalid input for {city}. Distance and path cannot be empty.")
                        all_correct = False
                        continue  # Skip further processing for this city

                    try:
                        player_answer[city] = int(distance_str)
                        player_paths[city] = path_str.split(",")
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid input for {city}. Please enter a valid distance and path.")
                        all_correct = False
                        continue  # Skip further processing for this city

            # Validate the player's answers
            for city in player_answer:
                # Check distances
                if player_answer[city] != correct_answer[city]:
                    all_correct = False
                    self.distance_error_labels[city].config(text=f"Incorrect distance for {city}. Correct distance is {correct_answer[city]}.", fg="green")

                # Check paths
                if city != start_city:
                    correct_path_str = ','.join(correct_paths[city])
                player_path_str = ','.join(player_paths[city])
                print("player_path_str= "+ json.dumps(player_path_str))
                print("player_paths= "+json.dumps(player_paths))
                if city != start_city:
                    if player_paths[city] != correct_paths[city]:
                        all_correct = False
                        self.path_error_labels[city].config(text=f"Incorrect path for {city}. Correct path is {correct_path_str}.", fg="green")
                if city == start_city:
                    if player_paths[city] != start_city:
                        self.path_error_labels[city].config(text=f"Incorrect path for {city}. Correct path is {city}.", fg="green")
            
            # Provide final feedback
            if all_correct:
                end_time = time.time()
                play_time = end_time - self.start_time
                self.win_label.config(text=f"Correct! You found the shortest paths. You took {play_time} seconds.")
                messagebox.showinfo("Result", f"Correct! You found the shortest paths. You took {play_time} seconds")
                self.path_error_labels[start_city].config(text="")
                self.save_to_database(player_name, play_time, player_answer,  player_paths, correct_answer, correct_paths, bellman_time, dijkstra_time)
            else:
                messagebox.showinfo("Result", "Some answers were incorrect. Please check the distances and paths and try again.")
        else:
            messagebox.showerror("Error", "Graph contains negative weight cycles or other errors.")


    def reconstruct_path(self, predecessors, start, end):
        path = []
        while end is not None and end != start:
            path.insert(0, end)
            end = predecessors[end]
        if end == start:
            path.insert(0, start)
        return path
    
    
    def save_to_database(self, player_name, play_time, player_answer, player_paths, correct_answer, correct_paths, bellman_ford_time, dijkstra_time):
        game_id = str(uuid.uuid4())  # Generate a unique ID for the game session

        game_data = {
            "game_id": game_id,
            "player_name": player_name,
            "player_play_time": play_time,
            "player_answer": player_answer,
            "player_paths": player_paths,
            "correct_answer": correct_answer,
            "correct_paths": correct_paths,  
            "bellman_ford_time": bellman_ford_time,
            "dijkstra_time": dijkstra_time,
        }

        # Save the game result to Firebase with a unique document ID
        try:
            print("done")
            self.db.collection("ShortestPath").document(game_id).set(game_data)
            print(f"Game result saved to Firebase with game ID: {game_id}")
        except Exception as e:
            print(f"An error occurred while saving to Firestore: {e}")
            
            
    def start_new_game(self):   
        #Emptying the table values
        for i, city1 in enumerate(self.cities):
            for j, city2 in enumerate(self.cities):
                self.matrix_labels[i][j].config(text="")
        
        #Distance and path error lables
        for i, city in enumerate(self.cities):
            self.distance_error_labels[city].config(text="")
            self.path_error_labels[city].config(text="")
        
        #Emptying input filds
        for i, city in enumerate(self.cities):
            self.distance_entries[city].delete(0, tk.END)
            self.path_entries[city].delete(0, tk.END)

        self.start_city_var.set("")
        self.instructions_label_city.config(textvariable=None)
        self.graph = {}
        self.win_label.config(text="")
        self.player_name_error_label.config(text="")
        self.player_name.set("")
        self.show_frame("NameEntry")
        
    def create_view_results_frame(self):
        frame = tk.Frame(self.master)

        tk.Label(frame, text="Results for All Players:", font=("Arial", 14)).pack(pady=20)

        # Create Treeview
        columns = ("player_name", "play_time", "player_answer", "player_paths", "correct_answer",  "correct_paths", "bellman_ford_time", "dijkstra_time")
        self.results_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.results_tree.pack(pady=10, fill="both", expand=True)

        # Define column headings
        self.results_tree.heading("player_name", text="Name", anchor="w")
        self.results_tree.heading("play_time", text="Time_Taken_in_seconds", anchor="w")
        self.results_tree.heading("player_answer", text="Distances", anchor="w")
        self.results_tree.heading("player_paths", text="Paths", anchor="w")
        self.results_tree.heading("correct_answer", text="Algo_distance", anchor="w")
        self.results_tree.heading("correct_paths", text="Algo_path", anchor="w")
        self.results_tree.heading("bellman_ford_time", text="Bellman_Time", anchor="w")
        self.results_tree.heading("dijkstra_time", text="Dijkstra_Time", anchor="w")

        # Define column widths
        self.results_tree.column("player_name", width=15, anchor="w")
        self.results_tree.column("play_time", width=100, anchor="w")
        self.results_tree.column("player_answer", width=200, anchor="w")
        self.results_tree.column("player_paths", width=200, anchor="w")
        self.results_tree.column("correct_answer", width=200, anchor="w")
        self.results_tree.column("correct_paths", width=200, anchor="w")
        self.results_tree.column("bellman_ford_time", width=60, anchor="w")
        self.results_tree.column("dijkstra_time", width=60, anchor="w")

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
        
        self.frames["ViewResults"] = frame  # Add to frames dictionary
        self.show_frame("ViewResults")  # Show this frame
    
    def get_all_results(self):
        # Retrieve all documents from the 'ShortestPath' collection
        docs = self.db.collection("ShortestPath").stream()

        # Convert documents to dictionaries
        results = [doc.to_dict() for doc in docs]

        return results
    
    def show_all_results(self):
        # Clear existing data in the Treeview
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
    
        results = self.get_all_results()

        if results:
            for result in results:
                self.results_tree.insert("", "end", values=(
                    result['player_name'],
                    result['player_play_time'],
                    result['player_answer'],
                    result['player_paths'],
                    result['correct_answer'],
                    result['correct_paths'],
                    result['bellman_ford_time'],
                    result['dijkstra_time'],
                ))
        else:
            # If no results, you can optionally add a message or handle this case
            self.results_tree.insert("", "end", values=("No results found", "", "", "", "", "", "", ""))
        
    def exit(self):
        self.master.destroy()
            
if __name__ == "__main__":
    root = tk.Tk()
    app = ShortestPath(root)
    root.mainloop()