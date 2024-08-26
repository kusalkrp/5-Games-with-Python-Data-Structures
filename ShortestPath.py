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

class ShortestPath:
    def __init__(self):
        self.cities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.graph = {}
        self.matrix_labels = []
        self.distance_entries = {}
        self.path_entries = {}
        self.start_city_var = None
        self.canvas = None
        self.graph_plot = None
        self.start_frame = None
        self.game_frame = None
        self.player_name_entry = None
        self.setup_database()
        self.setup_ui()

    def setup_database(self):
        conn = sqlite3.connect('shortest_path_game.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_results (
                id INTEGER PRIMARY KEY,
                player_name TEXT,
                player_answer TEXT,
                player_paths TEXT,
                correct_answer TEXT,
                correct_paths TEXT,
                bellman_ford_time REAL,
                dijkstra_time REAL
            )
        ''')
        conn.commit()
        conn.close()

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
        conn = sqlite3.connect('shortest_path_game.db')
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO game_results (player_name, player_answer, player_paths, correct_answer, correct_paths, bellman_ford_time, dijkstra_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (player_name, str(player_answer), str(player_paths), str(correct_answer), str(correct_paths), bellman_ford_time, dijkstra_time))
        
        conn.commit()
        conn.close()

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
        return graph

    def setup_ui(self):
        root = tk.Tk()
        root.title("Shortest Path Game")
        root.geometry("1000x700")

        self.start_frame = tk.Frame(root)
        tk.Label(self.start_frame, text="Player Name:").grid(row=0, column=0)
        self.player_name_entry = tk.Entry(self.start_frame)
        self.player_name_entry.grid(row=0, column=1)
        tk.Button(self.start_frame, text="Start Game", command=self.start_game).grid(row=1, columnspan=2)
        self.start_frame.grid(row=0, column=1)
        
        self.game_frame = tk.Frame(root)

        tk.Label(self.game_frame, text="Select Start City:").grid(row=1, column=0)
        self.start_city_var = tk.StringVar(root)
        self.start_city_var.set(self.cities[0])  # default value
        tk.OptionMenu(self.game_frame, self.start_city_var, *self.cities).grid(row=1, column=1)

        tk.Button(self.game_frame, text="New Game", command=self.new_game).grid(row=2, column=0)
        tk.Button(self.game_frame, text="Check Answer", command=self.check_answer).grid(row=2, column=1)

        # Matrix display
        matrix_frame = tk.Frame(self.game_frame)
        matrix_frame.grid(row=3, column=2, columnspan=2)

        # Create column headers
        for i, city in enumerate(self.cities):
            tk.Label(matrix_frame, text=city, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=len(self.cities)+1, column=i+1, sticky="nsew")
            tk.Label(matrix_frame, text=city, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=i+1, column=0, sticky="nsew")
        
        self.matrix_labels = [[tk.Label(matrix_frame, text="", borderwidth=1, relief="solid", padx=10, pady=5) for _ in self.cities] for _ in self.cities]
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                self.matrix_labels[i][j].grid(row=i+1, column=j+1, sticky="nsew")

        # Entry fields for distances and paths
        for i, city in enumerate(self.cities):
            if city != self.cities[0]:  # Skip the start city itself
                tk.Label(self.game_frame, text=f"Distance to {city}:").grid(row=4+i, column=0)
                self.distance_entries[city] = tk.Entry(self.game_frame)
                self.distance_entries[city].grid(row=4+i, column=1)
                
                tk.Label(self.game_frame, text=f"Path to {city} (comma-separated):").grid(row=4+i, column=2)
                self.path_entries[city] = tk.Entry(self.game_frame)
                self.path_entries[city].grid(row=4+i, column=3)

        # Dijkstra Algorithm Illustration
        fig, self.graph_plot = plt.subplots(figsize=(5, 4))
        plt.axis('off')
        self.canvas = FigureCanvasTkAgg(fig, master=self.game_frame)
        self.canvas.get_tk_widget().grid(row=25, column=2, rowspan=len(self.cities)+1)

        root.mainloop()
    
    def start_game(self):
        player_name = self.player_name_entry.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        
        # Hideing the starting frame and show game frame
        self.start_frame.grid_forget()
        self.game_frame.grid(row=0, column=0)

    def new_game(self):
        self.graph = self.generate_random_graph()
        self.display_graph(self.graph)
        self.draw_graph(self.graph)

    def display_graph(self, graph):
        for i, city1 in enumerate(self.cities):
            for j, city2 in enumerate(self.cities):
                if city1 in graph and city2 in graph[city1]:
                    self.matrix_labels[i][j].config(text=str(graph[city1][city2]))
                else:
                    self.matrix_labels[i][j].config(text="")

    def draw_graph(self, graph, highlight=[]):
        self.graph_plot.clear()
        G = nx.Graph()  
        for city in graph:
            for neighbor, distance in graph[city].items():
                G.add_edge(city, neighbor, weight=distance)

        pos = nx.spring_layout(G) 
        nx.draw(G, pos, with_labels=True, ax=self.graph_plot, node_color='lightblue', font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, ax=self.graph_plot)
        if highlight:
            nx.draw_networkx_nodes(G, pos, nodelist=highlight, node_color='orange', ax=self.graph_plot)
        self.canvas.draw()

    def update_dijkstra_display(self, distances, highlight):
        self.draw_graph(self.graph, highlight)
        self.canvas.draw()
        self.canvas.flush_events()
        time.sleep(0.5)  

    def check_answer(self):
        start_city = self.start_city_var.get()
        player_name = self.player_name_entry.get()

        player_answer = {city: int(self.distance_entries[city].get()) for city in self.distance_entries if self.distance_entries[city].get()}
        player_paths = {city: self.path_entries[city].get().split(',') for city in self.path_entries if self.path_entries[city].get()}

        start_time = time.time()
        correct_answer, correct_paths = self.bellman_ford(self.graph, start_city)
        bellman_ford_time = time.time() - start_time
        
        start_time = time.time()
        dijkstra_answer, dijkstra_paths = self.dijkstra(self.graph, start_city, display_step_callback=self.update_dijkstra_display)
        dijkstra_time = time.time() - start_time

        result_message = ""
        if correct_answer is None:
            result_message = "The graph contains a negative weight cycle!"
        else:
            for city in self.cities:
                if city == start_city:
                    continue

                player_distance = player_answer.get(city, float('inf'))
                correct_distance = correct_answer[city]

                player_path = player_paths.get(city, [])
                correct_path = []
                if correct_paths[city]:
                    path_node = city
                    while path_node:
                        correct_path.insert(0, path_node)
                        path_node = correct_paths[path_node]

                if player_distance == correct_distance and player_path == correct_path:
                    result_message += f"Correct: Distance to {city} is {player_distance} and path is {player_path}\n"
                else:
                    result_message += f"Incorrect: Distance to {city} should be {correct_distance} and path should be {correct_path}\n"

            self.save_to_database(player_name, player_answer, player_paths, correct_answer, correct_paths, bellman_ford_time, dijkstra_time)

        messagebox.showinfo("Results", result_message)

if __name__ == "__main__":
    ShortestPath()
