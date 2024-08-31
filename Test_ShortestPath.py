import unittest
from unittest.mock import patch, MagicMock
import random

# Import the ShortestPath class from your main module
from ShortestPath import ShortestPath


class TestShortestPath(unittest.TestCase):
    def setUp(self):
        # Setup that runs before each test
        self.shortest_path = ShortestPath()

    def tearDown(self):
        # Teardown that runs after each test
        pass

    @patch('ShortestPath.firestore')  # Mock firestore to avoid actual Firebase calls
    def test_initialize_firebase(self, mock_firestore):
        # Mock the credentials and initialize_app methods
        mock_cred = MagicMock()
        mock_firestore.client.return_value = MagicMock()
        self.shortest_path.initialize_firebase()

        # Check if Firebase was initialized
        self.assertTrue(mock_firestore.client.called, "Firestore client should be called")

    def test_generate_random_graph(self):
        graph = self.shortest_path.generate_random_graph()

        # Check if all cities have been initialized in the graph
        self.assertEqual(len(graph), len(self.shortest_path.cities))
        for city in self.shortest_path.cities:
            self.assertIn(city, graph)

        # Check if at least one connection exists between cities
        has_edges = any(len(edges) > 0 for edges in graph.values())
        self.assertTrue(has_edges, "Graph should have at least one edge")

    def test_bellman_ford(self):
        # Creating a graph with known shortest paths
        graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'C': 2, 'D': 2},
            'C': {'D': 3},
            'D': {}
        }
        start_city = 'A'
        distances, predecessors = self.shortest_path.bellman_ford(graph, start_city)

        # Assert expected distances
        expected_distances = {'A': 0, 'B': 1, 'C': 3, 'D': 3}
        self.assertEqual(distances, expected_distances)

        # Assert expected predecessors
        expected_predecessors = {'A': None, 'B': 'A', 'C': 'B', 'D': 'B'}
        self.assertEqual(predecessors, expected_predecessors)

    def test_dijkstra(self):
        # Creating a graph with known shortest paths
        graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'C': 2, 'D': 2},
            'C': {'D': 3},
            'D': {}
        }
        start_city = 'A'

        # Mock display_step_callback to avoid real display during testing
        mock_callback = MagicMock()

        distances, predecessors = self.shortest_path.dijkstra(graph, start_city, mock_callback)

        # Assert expected distances
        expected_distances = {'A': 0, 'B': 1, 'C': 3, 'D': 3}
        self.assertEqual(distances, expected_distances)

        # Assert expected predecessors
        expected_predecessors = {'A': None, 'B': 'A', 'C': 'B', 'D': 'B'}
        self.assertEqual(predecessors, expected_predecessors)

    @patch('your_module_name.firestore')  # Mock firestore to avoid actual Firebase calls
    def test_save_to_database(self, mock_firestore):
        mock_firestore.client.return_value.collection.return_value.document.return_value.set = MagicMock()

        player_name = "Test Player"
        player_answer = {"A": 0, "B": 5}
        player_paths = {"A": ["A"], "B": ["A", "B"]}
        correct_answer = {"A": 0, "B": 5}
        correct_paths = {"A": ["A"], "B": ["A", "B"]}
        bellman_ford_time = 0.1
        dijkstra_time = 0.2

        self.shortest_path.save_to_database(player_name, player_answer, player_paths, correct_answer, correct_paths, bellman_ford_time, dijkstra_time)

        # Assert that Firestore set method was called once
        self.assertTrue(mock_firestore.client.return_value.collection.return_value.document.return_value.set.called, "Firestore set method should be called")

if __name__ == "__main__":
    unittest.main()