import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from Minimum_Cost import MinimumCostTaskAssignmentGame  # Corrected import path

class TestMinimumCostTaskAssignmentGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = MinimumCostTaskAssignmentGame(self.root)
        self.app.initialize_firebase = MagicMock()  # Mock Firebase initialization
        self.app.db = MagicMock()  # Mock Firestore client

    def tearDown(self):
        self.root.destroy()

    def test_generate_cost_matrix(self):
        num_tasks = 4
        self.app.generate_cost_matrix(num_tasks)
        
        self.assertEqual(len(self.app.cost_matrix), num_tasks, "Cost matrix should have the same number of rows as num_tasks.")
        self.assertEqual(len(self.app.cost_matrix[0]), num_tasks, "Each row in the cost matrix should have the same number of elements as num_tasks.")
        
        for row in self.app.cost_matrix:
            for cost in row:
                self.assertGreaterEqual(cost, 20, "Cost should be greater than or equal to 20.")
                self.assertLessEqual(cost, 200, "Cost should be less than or equal to 200.")

    def test_find_optimal_assignment(self):
        # Set a known cost matrix
        self.app.cost_matrix = [
            [90, 75, 75, 80],
            [35, 85, 55, 65],
            [125, 95, 90, 105],
            [45, 110, 95, 115]
        ]
        self.app.find_optimal_assignment()

        # Expected results
        expected_assignment = [(0, 1), (1, 0), (2, 2), (3, 3)]
        expected_total_cost = 275

        self.assertEqual(self.app.assignment, expected_assignment, "Optimal assignment should match the expected assignment.")
        self.assertEqual(self.app.total_cost, expected_total_cost, "Total cost should match the expected total cost.")

    @patch('Minimum_Cost_Task_Assignment_Game.MinimumCostTaskAssignmentGame.save_result_to_database')
    def test_start_game(self, mock_save_result_to_database):
        self.app.num_tasks.set(4)
        self.app.start_game()

        self.assertEqual(len(self.app.cost_matrix), 4, "Cost matrix should have 4 rows when num_tasks is set to 4.")
        self.assertTrue(hasattr(self.app, 'assignment'), "The app should have an assignment attribute after starting the game.")
        mock_save_result_to_database.assert_called_once()

    def test_display_results(self):
        self.app.user_name.set("Test User")
        self.app.num_tasks.set(3)
        self.app.cost_matrix = [
            [50, 40, 60],
            [30, 90, 70],
            [80, 20, 90]
        ]
        self.app.assignment = [(0, 1), (1, 0), (2, 2)]
        self.app.total_cost = 180
        self.app.execution_time = 0.00123

        self.app.display_results(3)

        result_text = self.app.result_text_widget.get("1.0", "end-1c")
        expected_text = (
            "User: Test User\n"
            "Total Minimum Cost: $180\n"
            "Time Taken: 0.001230 seconds\n"
            "Optimal Assignment:\n"
        )

        self.assertIn(expected_text, result_text, "Displayed results should match the expected output.")

    @patch('Minimum_Cost_Task_Assignment_Game.firestore')
    def test_save_result_to_database(self, mock_firestore):
        mock_db = mock_firestore.client()
        self.app.db = mock_db

        self.app.user_name.set("Player1")
        self.app.num_tasks.set(4)
        self.app.total_cost = 150
        self.app.execution_time = 0.123456

        self.app.save_result_to_database()

        # Check if the Firestore client's add method was called with the correct data
        mock_db.collection.assert_called_once_with("minimum_cost_task_assignment")
        mock_db.collection().add.assert_called_once()
        saved_data = mock_db.collection().add.call_args[0][0]

        self.assertEqual(saved_data["user_name"], "Player1", "Saved user_name should match the input.")
        self.assertEqual(saved_data["num_tasks"], 4, "Saved num_tasks should match the input.")
        self.assertEqual(saved_data["total_cost"], 150, "Saved total_cost should match the input.")
        self.assertEqual(saved_data["execution_time"], 0.123456, "Saved execution_time should match the input.")
        self.assertIsInstance(saved_data["timestamp"], float, "Timestamp should be a float value.")

if __name__ == "__main__":
    unittest.main()
