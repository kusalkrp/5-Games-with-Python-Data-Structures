import unittest
from unittest.mock import patch, MagicMock
from ShortestPath import ShortestPath
import random
import tkinter as tk

class TestShortestPath(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = ShortestPath(self.root)
        self.app.initialize_firebase = MagicMock()  # Mock Firebase initialization
        self.app.db = MagicMock()  # Mock Firestore client
        
    def tearDown(self):
        self.root.destroy()

    def test_generate_random_graph(self):
        print("Starting test for generating a random graph")
        try:
            graph = self.app.generate_random_graph()
            self.assertIsInstance(graph, dict)
            self.assertGreaterEqual(len(graph), 10)
            for city, connections in graph.items():
                self.assertIsInstance(connections, dict)
                for connected_city, distance in connections.items():
                    self.assertIsInstance(distance, int)
                    self.assertGreaterEqual(distance, 5)
                    self.assertLessEqual(distance, 50)
            print("test_generate_random_graph: SUCCESS")
        except AssertionError as e:
            print("test_generate_random_graph: FAILED")
            raise e
        finally:
            print("test_entry_without_name: FINISHED")

    def test_validate_inputs_correct(self):
        print("Starting test for validate correct inputs")
        try:
            self.app.distance_entries['A'].insert(0, '10')
            self.app.distance_entries['B'].insert(0, '20')
            self.app.distance_entries['C'].insert(0, '10')
            self.app.distance_entries['D'].insert(0, '20')
            self.app.distance_entries['E'].insert(0, '10')
            self.app.distance_entries['F'].insert(0, '20')
            self.app.distance_entries['G'].insert(0, '10')
            self.app.distance_entries['H'].insert(0, '20')
            self.app.distance_entries['I'].insert(0, '10')
            self.app.distance_entries['J'].insert(0, '20')
        
            self.app.path_entries['A'].insert(0, 'B,C')
            self.app.path_entries['B'].insert(0, 'C,D')
            self.app.path_entries['C'].insert(0, 'B,C')
            self.app.path_entries['D'].insert(0, 'C,D')
            self.app.path_entries['E'].insert(0, 'B,C')
            self.app.path_entries['F'].insert(0, 'C,D')
            self.app.path_entries['G'].insert(0, 'B,C')
            self.app.path_entries['H'].insert(0, 'C,D')
            self.app.path_entries['I'].insert(0, 'B,C')
            self.app.path_entries['J'].insert(0, 'C,D')
        
            valid = self.app.validate_inputs()
            self.assertTrue(valid)
            print("test_validate_inputs_correct: SUCCESS")
        except AssertionError as e:
            print("test_validate_inputs_correct: FAILED")
            raise e
        finally:
            print("test_validate_inputs_correct: FINISHED")
    
    def test_validate_inputs_wrong(self):
        print("Starting test for validate wrong inputs")
        try:
            self.app.distance_entries['A'].insert(0, tk.END)
            self.app.distance_entries['B'].insert(0, '20')
            self.app.distance_entries['C'].insert(0, '10')
            self.app.distance_entries['D'].insert(0, '20')
            self.app.distance_entries['E'].insert(0, '10')
            self.app.distance_entries['F'].insert(0, '20')
            self.app.distance_entries['G'].insert(0, '-10')
            self.app.distance_entries['H'].insert(0, '20')
            self.app.distance_entries['I'].insert(0, '10')
            self.app.distance_entries['J'].insert(0, '20')
        
            self.app.path_entries['A'].insert(0, 'B,C')
            self.app.path_entries['B'].insert(0, 'C,D')
            self.app.path_entries['C'].insert(0, 'B,C')
            self.app.path_entries['D'].insert(0, 'C,D')
            self.app.path_entries['E'].insert(0, 'B,C')
            self.app.path_entries['F'].insert(0, 'C,D')
            self.app.path_entries['G'].insert(0, 'B,C')
            self.app.path_entries['H'].insert(0, 'C,D')
            self.app.path_entries['I'].insert(0, 'B,C,')
            self.app.path_entries['J'].insert(0, 'C,D,')

            valid = self.app.validate_inputs()
            self.assertFalse(valid)
            print("test_validate_inputs_wrong: SUCCESS")
        except AssertionError as e:
            print("test_validate_inputs_wrong: FAILED")
            raise e
        finally:
            print("test_validate_inputs_wrong: FINISHED")
        
    def test_validate_inputs_null(self):
        print("Starting test for validate null inputs")
        try:
            self.app.distance_entries['A'].delete(0, '30')
            self.app.distance_entries['A'].insert(0, '10')

            valid = self.app.validate_inputs()
            self.assertFalse(valid)
            print("test_validate_inputs_null: SUCCESS")
        except AssertionError as e:
            print("test_validate_inputs_null: FAILED")
            raise e
        finally:
            print("test_validate_inputs_null: FINISHED")

    def test_bellman_ford(self):
        print("Starting test for Bellman-Ford algorithm")
        try:
            graph = {
                'A': {'B': 1, 'C': 4},
                'B': {'C': 2, 'D': 5},
                'C': {'D': 1},
                'D': {}
            }
            distances, predecessors = self.app.bellman_ford(graph, 'A')
            expected_distances = {'A': 0, 'B': 1, 'C': 3, 'D': 4}
            expected_predecessors = {'A': None, 'B': 'A', 'C': 'B', 'D': 'C'}
            self.assertEqual(distances, expected_distances)
            self.assertEqual(predecessors, expected_predecessors)
            print("test_bellman_ford: SUCCESS")
        except AssertionError as e:
            print("test_bellman_ford: FAILED")
            raise e
        finally:
            print("test_bellman_ford: FINISHED")

    def test_dijkstra(self):
        print("Starting test for Dijkstra algorithm")
        try:
            graph = {
                'A': {'B': 1, 'C': 4},
                'B': {'C': 2, 'D': 5},
                'C': {'D': 1},
                'D': {}
            }
            distances, predecessors = self.app.dijkstra(graph, 'A')
            expected_distances = {'A': 0, 'B': 1, 'C': 3, 'D': 4}
            expected_predecessors = {'A': None, 'B': 'A', 'C': 'B', 'D': 'C'}
            self.assertEqual(distances, expected_distances)
            self.assertEqual(predecessors, expected_predecessors)
            print("test_dijkstra: SUCCESS")
        except AssertionError as e:
            print("test_dijkstra: FAILED")
            raise e
        finally:
            print("test_dijkstra: FINISHED")

    def test_save_to_database(self):
        print("Starting test for Saving to database")
        try:
            with patch.object(self.app.db, 'collection') as mock_collection:
                mock_document = MagicMock()
                mock_collection.return_value.document.return_value = mock_document
                self.app.save_to_database(
                    player_name='TestPlayer',
                    player_answer={'A': 0, 'B': 1},
                    player_paths={'A': ['A'], 'B': ['A', 'B']},
                    correct_answer={'A': 0, 'B': 1},
                    correct_paths={'A': ['A'], 'B': ['A', 'B']},
                    bellman_ford_time=0.001,
                    dijkstra_time=0.002
                )
                mock_collection.assert_called_once_with('ShortestPath')
                mock_document.set.assert_called_once()
            print("test_save_to_database: SUCCESS")
        except AssertionError as e:
            print("test_save_to_database: FAILED")
            raise e
        finally:
            print("test_save_to_database: FINISHED")

    def test_start_game(self):
        print("Starting test for starting the game")
        try:
            self.app.start_game()
            self.assertIsNotNone(self.app.graph)
            self.assertIn(self.app.start_city_var.get(), self.app.cities)
            print("test_start_game: SUCCESS")
        except AssertionError as e:
            print("test_start_game: FAILED")
            raise e
        finally:
            print("test_start_game: FINISHED")

    def test_go_to_game_frame(self):
        print("Starting test to go for the game frame")
        try:
            self.app.player_name.set("TestPlayer")
            self.app.go_to_game_frame()
            self.assertEqual(self.app.current_frame, self.app.frames["Play"])
            print("test_go_to_game_frame: SUCCESS")
        except AssertionError as e:
            print("test_go_to_game_frame: FAILED")
            raise e
        finally:
            print("test_go_to_game_frame: FINISHED")

if __name__ == "__main__":
    unittest.main()