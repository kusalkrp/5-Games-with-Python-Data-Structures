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
    def __init__(self):
        
        self.cities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.graph = {}
        self.matrix_labels = []
        self.player_name_entry = None
        self.start_city_var = None
        self.canvas = None
        self.graph_plot = None
        print("start")
        self.distance_entries = {}
        self.path_entries = {}
        self.start_frame = None
        self.game_frame = None
        print("initalized")
        self.initialize_firebase()
        self.db = firestore.client()
        self.setup_ui()
        
        
        
    def initialize_firebase(self):
    # Use your own Firebase credentials
        try:
            if not firebase_admin._apps:  # Check if Firebase is already initialized
                cred = credentials.Certificate(
                    r'pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json'
                )
                firebase_admin.initialize_app(cred)
                print("Firebase initialized.")
            else:
                print("Firebase already initialized.")
        except ValueError as e:
            print(f"Error initializing Firebase: {e}")


    # Bellman-Ford algorithm------------------------------------------------------------------------------------------------------------------------------------
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

    # Dijkstra's algorithm with plotting-------------------------------------------------------------------------------------------------------------------------
    def dijkstra(self, graph, start, display_step_callback):
        distances = {city: float('inf') for city in graph}
        distances[start] = 0
        predecessors = {city: None for city in graph}
        priority_queue = [(0, start)]
        visited = set()

        display_step_callback(distances, highlight=[])  # Display initial distances

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

            display_step_callback(distances, highlight=list(visited))  # Update display after processing each city

        return distances, predecessors

    def save_to_database(self, player_name, player_answer, player_paths, correct_answer, correct_paths, bellman_ford_time, dijkstra_time):
        game_id = str(uuid.uuid4())  # Generate a unique ID for the game session

        game_data = {
            "game_id": game_id,
            "player_name": player_name,  
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
 #-----------------------------------------------------------------------------------------------------------------------------generating a random matrix
    # Generate a random undirected graph
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

    
    def setup_ui(self):
        root = tk.Tk()
        root.title("Shortest Path Game")
        root.geometry("1110x650")

        # Create the start frame
        self.start_frame = tk.Frame(root, bg="#ffffff")

        # Player name label
        tk.Label(self.start_frame, text="Enter your name:", font=("Arial", 18, "bold"), fg="#fa0000", bg="#ffffff").grid(row=0, column=0, padx=10, pady=10)

        # Player name entry
        self.player_name_entry = tk.Entry(self.start_frame, font=("Arial", 14))
        self.player_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Error label for name entry
        self.name_error_label = tk.Label(self.start_frame, text="", fg="red", font=("Arial", 12), bg="#ffffff")
        self.name_error_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Start Game button
        tk.Button(self.start_frame, text="Start Game", command=self.start_game, font=("Arial", 12, "bold"),
            bg="#f86b53",
            fg="white",
            padx=10,
            pady=5,
            relief="raised",
            borderwidth=2,
            width=20,
            height=1,
            activebackground="#e74755",
            activeforeground="white").grid(row=2, column=0, columnspan=2, pady=10)

        # Center the frame within the main window
        self.start_frame.grid(row=0, column=0, padx=(root.winfo_screenwidth() - 1250) // 2, pady=(root.winfo_screenheight() - 650) // 2)

        menu_bar = tk.Menu(root)  # Attach the menu bar to the main window
        root.config(menu=menu_bar)

        # Create a 'Game' menu
        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menu", menu=game_menu)

        # Add 'Start New Game', 'View Results', and 'Exit' options
        game_menu.add_command(label="Start New Game", command=self.back_to_start)
        game_menu.add_command(label="View Results", command=self.result_transfer)
        game_menu.add_command(label="Exit", command=root.quit)
        

        # Second frame
        self.game_frame = tk.Frame(root)

        tk.Label(self.game_frame, text="The Starting City is:", font=("Arial", 18, "bold"), fg="#fa0000", bg="#ffffff").grid(row=1, column=1, padx=10, pady=10)
        self.start_city_var = tk.StringVar(root)
        tk.Label(self.game_frame, textvariable=self.start_city_var, font=("Arial", 18, "bold"), fg="#fa0000", bg="#ffffff").grid(row=1, column=2, padx=10, pady=10)

        tk.Button(self.game_frame, text="New Game", command=self.new_game).grid(row=2, column=0)
        tk.Button(self.game_frame, text="Check Answer", command=self.check_answer).grid(row=2, column=1)

        # Matrix display
        matrix_frame = tk.Frame(self.game_frame)
        matrix_frame.grid(row=3, column=2, columnspan=2)

        for i, city in enumerate(self.cities):
            # Row and column headers with enhanced styles
            tk.Label(matrix_frame, text=city, borderwidth=2, relief="solid", padx=10, pady=5, 
                    font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333333").grid(row=len(self.cities) + 1, column=i + 1, sticky="nsew")
            tk.Label(matrix_frame, text=city, borderwidth=2, relief="solid", padx=10, pady=5, 
                    font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333333").grid(row=i + 1, column=0, sticky="nsew")

        # Matrix labels with enhanced styles and diagonal logic
        self.matrix_labels = [[tk.Label(matrix_frame, text="", borderwidth=1, relief="solid", padx=10, pady=5, 
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

        self.distance_entries = {}
        self.path_entries = {}
        self.distance_error_labels = {}  # To store error labels for distance inputs
        self.path_error_labels = {}  # To store error labels for path inputs

        for i, city in enumerate(self.cities):
            # Distance entry label
            tk.Label(self.game_frame, text=f"Distance to {city}:", font=("Arial", 13, "bold"), fg="#587cd6", bg="#ffffff").grid(row=4 + i, column=0)
    
            # Distance entry field
            self.distance_entries[city] = tk.Entry(self.game_frame, font=("Arial", 13))
            self.distance_entries[city].grid(row=4 + i, column=1)

            # Error label for distance entry
            self.distance_error_labels[city] = tk.Label(self.game_frame, text="", fg="red", font=("Arial", 13))
            self.distance_error_labels[city].grid(row=4 + i, column=2)  # Error label next to the distance entry

            # Path entry label
            tk.Label(self.game_frame, text=f"Path to {city} (comma-separated):", font=("Arial", 13, "bold"), fg="#587cd6", bg="#ffffff").grid(row=4 + i, column=3)
    
            # Path entry field
            self.path_entries[city] = tk.Entry(self.game_frame, font=("Arial", 13))
            self.path_entries[city].grid(row=4 + i, column=4)

            # Error label for path entry
            self.path_error_labels[city] = tk.Label(self.game_frame, text="", fg="red", font=("Arial", 13))
            self.path_error_labels[city].grid(row=4 + i, column=5)  # Error label next to the path entry

        # Result frame
        self.result_frame = tk.Frame(root)

        tk.Label(self.result_frame, text="Results for All Players:", font=("Arial", 14)).pack(pady=20)

        # Create Treeview
        columns = ("player_name", "player_answer", "player_paths", "correct_answer",  "correct_paths", "bellman_ford_time", "dijkstra_time")
        self.results_tree = ttk.Treeview(self.result_frame, columns=columns, show="headings")
        self.results_tree.pack(pady=10, fill="both", expand=True)

        # Define column headings
        self.results_tree.heading("player_name", text="Name", anchor="w")
        self.results_tree.heading("player_answer", text="Distances", anchor="w")
        self.results_tree.heading("player_paths", text="Paths", anchor="w")
        self.results_tree.heading("correct_answer", text="Algo_distance", anchor="w")
        self.results_tree.heading("correct_paths", text="Algo_path", anchor="w")
        self.results_tree.heading("bellman_ford_time", text="Bellman_Time", anchor="w")
        self.results_tree.heading("dijkstra_time", text="Dijkstra_Time", anchor="w")

        # Define column widths
        self.results_tree.column("player_name", width=100, anchor="w")
        self.results_tree.column("player_answer", width=200, anchor="w")
        self.results_tree.column("player_paths", width=200, anchor="w")
        self.results_tree.column("correct_answer", width=200, anchor="w")
        self.results_tree.column("correct_paths", width=200, anchor="w")
        self.results_tree.column("bellman_ford_time", width=60, anchor="w")
        self.results_tree.column("dijkstra_time", width=60, anchor="w")

        tk.Button(
            self.result_frame,
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

    # Start the Tkinter main loop
        root.mainloop()


    def start_game(self):
        player_name = self.player_name_entry.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        # Hide start frame and show game frame
        self.start_frame.grid_forget()
        self.game_frame.grid(row=0, column=0)
    
    def result_transfer(self):
        self.start_frame.grid_forget()
        self.game_frame.grid_forget()
        self.result_frame.grid(row=0, column=0)
        
    def back_to_start(self):
        self.game_frame.grid_forget()
        self.result_frame.grid_forget()
        self.start_frame.grid(row=0, column=0)

    # Start a new game
    def new_game(self):
        self.graph = self.generate_random_graph()
        self.display_graph()
        # self.draw_graph()

        # Randomly select a starting city and set it in the dropdown
        selected_city = random.choice(self.cities)
        self.start_city_var.set(selected_city)  # Update dropdown display with selected city

    # Display the graph on the UI
    def display_graph(self):
        for i, city1 in enumerate(self.cities):
            for j, city2 in enumerate(self.cities):
                if city1 in self.graph and city2 in self.graph[city1]:
                    self.matrix_labels[i][j].config(text=str(self.graph[city1][city2]))
                else:
                    self.matrix_labels[i][j].config(text="")

    # Draw the undirected graph using NetworkX-----------------------------------------------NOT USED CURRENTLY                           
    def draw_graph(self):
        G = nx.Graph()
        for city, edges in self.graph.items():
            for destination, weight in edges.items():
                G.add_edge(city, destination, weight=weight)

        pos = nx.spring_layout(G)
        self.graph_plot.clear()
        nx.draw(G, pos, ax=self.graph_plot, with_labels=True)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.graph_plot)
        self.canvas.draw()

    # Illustrate each step of Dijkstra's algorithm-------------------------------------------NOT USED CURRENTLY
    def display_step_callback(self, distances, highlight=[]):
        G = nx.Graph()
        for city, edges in self.graph.items():
            for destination, weight in edges.items():
                G.add_edge(city, destination, weight=weight)

        pos = nx.spring_layout(G)
        # self.graph_plot.clear()
        nx.draw(G, pos, ax=self.graph_plot, with_labels=True)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.graph_plot)

        # Highlight visited nodes
        nx.draw_networkx_nodes(G, pos, nodelist=highlight, node_color='r', ax=self.graph_plot)

        self.canvas.draw()
        time.sleep(1)
        
    def validate_inputs(self):
        valid = True
        # Validate distance entries
        for city, entry in self.distance_entries.items():
            distance = entry.get()
            try:
                # Checking if the distance is a non-negative integer or float
                if not (distance.isdigit() or float(distance) >= 0):
                    raise ValueError("Invalid distance")
                self.distance_error_labels[city].config(text="") 
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
                self.path_error_labels[city].config(text="")

        return valid

    
    def check_answer(self):
        if not self.validate_inputs():
            print("Invalid input detected")
            return
        player_name = self.player_name_entry.get()
        start_city = self.start_city_var.get()

        if not player_name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        # Run Bellman-Ford and Dijkstra algorithms
        start_time_bell = time.time()
        bellman_result, bellman_predecessors = self.bellman_ford(self.graph, start_city)
        print('bell ans ' + json.dumps(bellman_result))
        print('bell pred ' + json.dumps(bellman_predecessors))
        bellman_time = time.time() - start_time_bell

        start_time_dij = time.time()
        dijkstra_result, dijkstra_predecessors = self.dijkstra(self.graph, start_city, self.display_step_callback)
        print('dijk ans ' + json.dumps(dijkstra_result))
        print('dijk pred ' + json.dumps(dijkstra_predecessors))
        dijkstra_time = time.time() - start_time_dij

        if bellman_result and dijkstra_result:
            correct_answer = dijkstra_result  # Since graph has no negative weights
            correct_paths = {city: self.reconstruct_path(dijkstra_predecessors, start_city, city) for city in self.cities if city != start_city}# ----------------------------------------- generating correct user paths

            # Retrieve the player's answers from the entry fields
            player_answer = {}
            player_paths = {}
            all_correct = True

            for city in self.cities:
                if city != start_city:
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
                    messagebox.showinfo("Result", f"Incorrect distance for {city}. Correct distance is {correct_answer[city]}.")

                # Check paths
                correct_path_str = ','.join(correct_paths[city])
                player_path_str = ','.join(player_paths[city])
                if player_paths[city] != correct_paths[city]:
                    all_correct = False
                    messagebox.showinfo("Result", f"Incorrect path for {city}. Correct path is {correct_path_str}.")
                    
            # self.save_to_database(player_name, player_answer, player_paths, correct_answer, correct_paths, bellman_time, dijkstra_time)
            
            # Provide final feedback
            if all_correct:
                messagebox.showinfo("Result", "Correct! You found the shortest paths.")
                self.save_to_database(player_name, player_answer, player_paths, correct_answer, correct_paths, bellman_time, dijkstra_time)
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
                    result['player_answer'],
                    result['player_paths'],
                    result['correct_answer'],
                    result['correct_paths'],
                    result['bellman_ford_time'],
                    result['dijkstra_time'],
                ))
        else:
            # If no results, you can optionally add a message or handle this case
            self.results_tree.insert("", "end", values=("No results found", "", "", "", "", "", ""))

if __name__ == "__main__":
    app = ShortestPath()