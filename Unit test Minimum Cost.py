import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from tkinter import Tk
from Minimum_Cost import TaskAssignmentGame  # Replace with the actual module name

class TestTaskAssignmentGame(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.game = TaskAssignmentGame(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_validate_name_with_empty_name(self):
        self.game.name_entry.insert(0, "")
        self.game.validate_name()
        self.assertEqual(self.game.warning_label.cget("text"), "Name cannot be empty.")

    def test_validate_name_with_valid_name(self):
        self.game.name_entry.insert(0, "John Doe")
        with patch.object(self.game, 'create_task_frame') as mock_create_task_frame:
            self.game.validate_name()
            mock_create_task_frame.assert_called_once()

    def test_validate_tasks_with_invalid_input(self):
        self.game.task_entry.insert(0, "-1")
        self.game.validate_tasks()
        self.assertEqual(self.game.task_warning_label.cget("text"), "Please enter a valid positive integer for the number of tasks.")

    def test_validate_tasks_with_valid_input(self):
        self.game.task_entry.insert(0, "5")
        with patch.object(self.game, 'run_game') as mock_run_game:
            self.game.validate_tasks()
            mock_run_game.assert_called_once_with(5)

    def test_hungarian_algorithm(self):
        cost_matrix = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
        row_ind, col_ind = self.game.hungarian_algorithm(cost_matrix)
        self.assertEqual(list(row_ind), [0, 1, 2])
        self.assertEqual(list(col_ind), [2, 1, 0])

    def test_calc_costs(self):
        cost_matrix = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
        assignment = [(0, 1), (1, 0), (2, 2)]
        total_cost = self.game.calc_costs(cost_matrix, assignment)
        self.assertEqual(total_cost, 6)

    def test_run_game(self):
        with patch.object(self.game, 'create_guessing_window') as mock_create_guessing_window:
            self.game.run_game(3)
            mock_create_guessing_window.assert_called_once()

    @patch('firebase_admin.firestore.client')
    def test_submit_result_to_firestore(self, mock_firestore):
        mock_db = mock_firestore.return_value
        self.game.player_name = "John Doe"
        self.game.num_tasks = 5
        self.game.create_result_frame(np.array([[4, 1], [2, 0]]), [(0, 1), (1, 0)], 5, 1.2, True)
        mock_db.collection.return_value.add.assert_called_once_with({
            'player_name': 'John Doe',
            'num_tasks': 5,
            'total_cost': 5.0,
            'time_taken': 1.2
        })

    # Additional tests for other functions and edge cases

if __name__ == '__main__':
    unittest.main()
