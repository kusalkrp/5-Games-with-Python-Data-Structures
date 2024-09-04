import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import tkinter as tk
from Minimum_Cost import TaskAssignmentGame

class TestTaskAssignmentGame(unittest.TestCase):
    @patch('Minimum_Cost.firestore.client')
    @patch('Minimum_Cost.initialize_app')
    @patch('Minimum_Cost.credentials.Certificate')
    def setUp(self, mock_cred, mock_init, mock_firestore_client):
        # Mock Firebase
        self.mock_firestore = MagicMock()
        mock_firestore_client.return_value = self.mock_firestore

        # Create a test Tkinter root
        self.root = tk.Tk()
        self.game = TaskAssignmentGame(self.root)  # Initialize the app correctly
        self.game.db = self.mock_firestore  # Mock Firestore client

        # Mock methods
        self.game.create_menu = MagicMock()
        self.game.create_name_frame = MagicMock()
        self.game.create_task_frame = MagicMock()
        self.game.create_guessing_window = MagicMock()
        self.game.show_name_frame = MagicMock()

        # Initialize warning_label and task_warning_label
        self.game.warning_label = tk.Label(self.root)
        self.game.task_warning_label = tk.Label(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_validate_name_empty(self):
        self.game.name_entry = MagicMock()
        self.game.name_entry.get.return_value = ''
        self.game.validate_name()
        self.assertEqual(self.game.warning_label.cget('text'), "Name cannot be empty.")

    def test_validate_name_non_empty(self):
        self.game.name_entry = MagicMock()
        self.game.name_entry.get.return_value = 'John Doe'
        self.game.validate_name()
        self.assertEqual(self.game.warning_label.cget('text'), "")

    def test_validate_tasks_invalid(self):
        self.game.task_entry = MagicMock()
        self.game.task_entry.get.return_value = 'invalid'
        self.game.validate_tasks()
        self.assertEqual(self.game.task_warning_label.cget('text'), "Please enter a valid positive integer for the number of tasks.")

    def test_validate_tasks_valid(self):
        self.game.task_entry = MagicMock()
        self.game.task_entry.get.return_value = '5'
        self.game.validate_tasks()
        self.assertEqual(self.game.task_warning_label.cget('text'), "")

    def test_calc_costs(self):
        cost_matrix = np.array([[10, 19, 8, 15],
                                [10, 18, 7, 17],
                                [13, 16, 9, 14],
                                [12, 19, 8, 18]])
        assignment = [(0, 2), (1, 0), (2, 3), (3, 1)]
        total_cost = self.game.calc_costs(cost_matrix, assignment)
        
        self.assertEqual(total_cost, 8 + 10 + 14 + 19)

    def test_calc_costs_different_assignment(self):
        cost_matrix = np.array([[10, 19, 8, 15],
                                [10, 18, 7, 17],
                                [13, 16, 9, 14],
                                [12, 19, 8, 18]])
        assignment = [(0, 0), (1, 1), (2, 2), (3, 3)]
        total_cost = self.game.calc_costs(cost_matrix, assignment)
        
        self.assertEqual(total_cost, 10 + 18 + 9 + 18)

    @patch('Minimum_Cost.time.time', return_value=0)
    @patch('Minimum_Cost.db')
    def test_create_result_frame(self, mock_db, mock_time):
        self.game.player_name = 'Test Player'
        self.game.num_tasks = 4
        cost_matrix = np.array([[10, 19, 8, 15],
                                [10, 18, 7, 17],
                                [13, 16, 9, 14],
                                [12, 19, 8, 18]])
        assignment = [{'row': 0, 'col': 2}, {'row': 1, 'col': 0}, {'row': 2, 'col': 3}, {'row': 3, 'col': 1}]
        total_cost = 50
        elapsed_time = 0
        is_correct = True
        
        self.game.create_result_frame(cost_matrix, assignment, total_cost, elapsed_time, is_correct)
        self.assertTrue(self.game.result_frame is not None)

    @patch('Minimum_Cost.time.time', return_value=0)
    @patch('Minimum_Cost.db')
    def test_create_result_frame_different_input(self, mock_db, mock_time):
        self.game.player_name = 'Another Player'
        self.game.num_tasks = 3
        cost_matrix = np.array([[5, 9, 1],
                                [10, 3, 2],
                                [8, 7, 4]])
        assignment = [{'row': 0, 'col': 2}, {'row': 1, 'col': 1}, {'row': 2, 'col': 0}]
        total_cost = 1 + 3 + 8
        elapsed_time = 10
        is_correct = False
        
        self.game.create_result_frame(cost_matrix, assignment, total_cost, elapsed_time, is_correct)
        self.assertTrue(self.game.result_frame is not None)

if __name__ == '__main__':
    unittest.main()