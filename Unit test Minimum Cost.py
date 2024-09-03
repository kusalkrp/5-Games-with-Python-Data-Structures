import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from Minimum_Cost import TaskAssignmentGame   # Assuming the class is in this file

class TestTaskAssignmentGame(unittest.TestCase):

    @patch('task_assignment_game.tk.Tk')
    def setUp(self, mock_tk):
        """Setup a new TaskAssignmentGame instance for testing."""
        self.root = mock_tk
        self.game = TaskAssignmentGame(self.root)

    def test_validate_name_empty(self):
        """Test that validate_name method shows warning when name is empty."""
        self.game.name_entry.get = MagicMock(return_value="  ")
        self.game.validate_name()
        self.assertEqual(self.game.warning_label.cget("text"), "Name cannot be empty.")

    def test_validate_name_non_empty(self):
        """Test that validate_name method proceeds when name is non-empty."""
        self.game.name_entry.get = MagicMock(return_value="John Doe")
        self.game.create_task_frame = MagicMock()
        self.game.validate_name()
        self.game.create_task_frame.assert_called_once()

    def test_validate_tasks_valid(self):
        """Test that validate_tasks proceeds with valid input."""
        self.game.task_entry.get = MagicMock(return_value="5")
        self.game.run_game = MagicMock()
        self.game.validate_tasks()
        self.game.run_game.assert_called_once_with(5)

    def test_validate_tasks_invalid(self):
        """Test that validate_tasks shows warning with invalid input."""
        self.game.task_entry.get = MagicMock(return_value="-1")
        self.game.validate_tasks()
        self.assertEqual(self.game.task_warning_label.cget("text"),
                         "Please enter a valid positive integer for the number of tasks.")

    def test_hungarian_algorithm(self):
        """Test that the Hungarian algorithm returns correct assignments."""
        cost_matrix = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
        row_ind, col_ind = self.game.hungarian_algorithm(cost_matrix)
        self.assertEqual(row_ind, [0, 1, 2])
        self.assertEqual(col_ind, [2, 1, 0])

    def test_calc_costs(self):
        """Test cost calculation based on assignment."""
        cost_matrix = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
        assignment = [{'row': 0, 'col': 2}, {'row': 1, 'col': 1}, {'row': 2, 'col': 0}]
        total_cost = self.game.calc_costs(cost_matrix, assignment)
        self.assertEqual(total_cost, 4 + 0 + 3)

    @patch('task_assignment_game.db.collection')
    def test_run_game_saves_results(self, mock_db_collection):
        """Test that run_game method saves results to Firebase."""
        self.game.player_name = "Test Player"
        self.game.create_result_frame = MagicMock()
        mock_db_collection.return_value.add = MagicMock()
        
        num_tasks = 3
        cost_matrix = np.random.randint(20, 201, size=(num_tasks, num_tasks))
        self.game.hungarian_algorithm = MagicMock(return_value=(list(range(num_tasks)), list(range(num_tasks))))
        self.game.calc_costs = MagicMock(return_value=100)

        self.game.run_game(num_tasks)

        mock_db_collection.return_value.add.assert_called_once()
        self.game.create_result_frame.assert_called_once()

    @patch('task_assignment_game.tk.Toplevel')
    def test_show_cost_matrix(self, mock_toplevel):
        """Test that show_cost_matrix creates a new window."""
        cost_matrix = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
        assignment = [{'row': 0, 'col': 1}, {'row': 1, 'col': 0}, {'row': 2, 'col': 2}]
        self.game.show_cost_matrix(cost_matrix, assignment)
        mock_toplevel.assert_called_once()

if __name__ == '__main__':
    unittest.main()
