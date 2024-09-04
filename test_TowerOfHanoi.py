import unittest
from unittest.mock import MagicMock, patch
import time
import tkinter as tk
import uuid
from TowerOfHanoi import TowerOfHanoi

class TestTowerOfHanoi(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = TowerOfHanoi(self.root)
        self.app.initialize_firebase = MagicMock()  # Mock Firebase initialization
        self.app.db = MagicMock()  # Mock Firestore client

    def tearDown(self):
        self.root.destroy()

    def test_validate_disk_entry(self):
        print("Starting test_validate_disk_entry")
        try:
            print("Testing with value '3'")
            self.assertTrue(self.app.validate_disk_entry("3"))
            print("Testing with value '10'")
            self.assertTrue(self.app.validate_disk_entry("10"))
            print("Testing with value '0'")
            self.assertFalse(self.app.validate_disk_entry("0"))
            print("Testing with value '-1'")
            self.assertFalse(self.app.validate_disk_entry("-1"))
            print("Testing with value 'abc'")
            self.assertFalse(self.app.validate_disk_entry("abc"))
            print("Testing with value '3.5'")
            self.assertFalse(self.app.validate_disk_entry("3.5"))
            print("test_validate_disk_entry passed")
        except AssertionError as e:
            print("test_validate_disk_entry failed")
            raise e
        finally:
            print("Finished test_validate_disk_entry")

    def test_start_game(self):
        print("Starting test_start_game")
        try:
            self.app.num_disks.set("3")
            print(f"Number of disks set to: {self.app.num_disks.get()}")
            self.app.start_game()
            print(f"Number of disks initialized: {self.app.num_disks_int.get()}")
            print(f"Rods state: {self.app.rods}")
            self.assertEqual(self.app.num_disks_int.get(), 3)
            self.assertEqual(len(self.app.rods["A"]), 3)
            self.assertEqual(len(self.app.rods["B"]), 0)
            self.assertEqual(len(self.app.rods["C"]), 0)
            print("test_start_game passed")
        except AssertionError as e:
            print("test_start_game failed")
            raise e
        finally:
            print("Finished test_start_game")

    def test_on_disk_release_valid_move(self):
        print("Starting test_on_disk_release_valid_move")
        try:
            self.app.num_disks.set("3")
            print(f"Number of disks set to: {self.app.num_disks.get()}")
            self.app.start_game()
            self.app.rods = {"A": [3, 2], "B": [], "C": [1]}
            print(f"Initial rods state: {self.app.rods}")
            self.app.on_disk_release(self.app.canvas.create_rectangle(0, 0, 0, 0))
            print(f"Rods state after move: {self.app.rods}")
            self.assertEqual(self.app.rods["A"], [3, 2])
            self.assertEqual(self.app.rods["B"], [])
            self.assertEqual(self.app.rods["C"], [1])
            print("test_on_disk_release_valid_move passed")
        except AssertionError as e:
            print("test_on_disk_release_valid_move failed")
            raise e
        finally:
            print("Finished test_on_disk_release_valid_move")

    def test_on_disk_release_invalid_move(self):
        print("Starting test_on_disk_release_invalid_move")
        try:
            self.app.num_disks.set("3")
            print(f"Number of disks set to: {self.app.num_disks.get()}")
            self.app.start_game()
            self.app.rods = {"A": [3, 2], "B": [1], "C": []}
            print(f"Initial rods state: {self.app.rods}")
            self.app.on_disk_release(self.app.canvas.create_rectangle(0, 0, 0, 0))
            print(f"Rods state after move: {self.app.rods}")
            self.assertEqual(self.app.rods["A"], [3, 2])
            self.assertEqual(self.app.rods["B"], [1])
            self.assertEqual(self.app.rods["C"], [])
            print("test_on_disk_release_invalid_move passed")
        except AssertionError as e:
            print("test_on_disk_release_invalid_move failed")
            raise e
        finally:
            print("Finished test_on_disk_release_invalid_move")

    def test_check_win(self):
        print("Starting test_check_win")
        try:
            self.app.num_disks.set("3")
            print(f"Number of disks set to: {self.app.num_disks.get()}")
            self.app.start_game()
            self.app.rods = {"A": [], "B": [], "C": [3, 2, 1]}
            print(f"Rods state: {self.app.rods}")
            self.app.check_win()
            result_text = self.app.result_label.cget("text")
            print(f"Result label text: {result_text}")
            self.assertIn("solved the puzzle", result_text)
            print("test_check_win passed")
        except AssertionError as e:
            print("test_check_win failed")
            raise e
        finally:
            print("Finished test_check_win")

    @patch('TowerOfHanoi.firestore')
    def test_save_game_result(self, mock_firestore):
        print("Starting test_save_game_result")
        try:
            mock_db = mock_firestore.client()
            self.app.db = mock_db

            self.app.name.set("Test1")
            self.app.num_disks_int.set(3)
            self.app.num_moves = 10
            self.app.start_time = time.time() - 60  # Assume the game took 60 seconds
            self.app.move_sequence = [("A", "C"), ("A", "B"), ("C", "B")]

            print(f"Player name: {self.app.name.get()}")
            print(f"Number of disks: {self.app.num_disks_int.get()}")
            print(f"Number of moves: {self.app.num_moves}")
            print(f"Time taken: {time.time() - self.app.start_time} seconds")
            print(f"Move sequence: {self.app.move_sequence}")

            self.app.save_game_result()

            # Check if the Firestore client's set method was called with the correct data
            mock_db.collection.assert_called_once_with("TowerofHanoi")
            mock_db.collection().document().set.assert_called_once()
            saved_data = mock_db.collection().document().set.call_args[0][0]

            print(f"Saved data: {saved_data}")

            self.assertEqual(saved_data["player_name"], "Test1")
            self.assertEqual(saved_data["num_disks"], 3)
            self.assertEqual(saved_data["moves"], 10)
            self.assertAlmostEqual(saved_data["time_taken"], 60, delta=1)
            self.assertEqual(saved_data["move_sequence"], "AC,AB,CB")
            print("test_save_game_result passed")
        except AssertionError as e:
            print("test_save_game_result failed")
            raise e
        finally:
            print("Finished test_save_game_result")

class TestTowerOfHanoiIntegration(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = TowerOfHanoi(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_save_game_result_integration(self):
        print("Starting test_save_game_result_integration")
        try:
            self.app.name.set("Test1")
            self.app.num_disks_int.set(3)
            self.app.num_moves = 10
            self.app.start_time = time.time() - 60  # Assume the game took 60 seconds
            self.app.move_sequence = [("A", "C"), ("A", "B"), ("C", "B")]

            print(f"Player name: {self.app.name.get()}")
            print(f"Number of disks: {self.app.num_disks_int.get()}")
            print(f"Number of moves: {self.app.num_moves}")
            print(f"Time taken: {time.time() - self.app.start_time} seconds")
            print(f"Move sequence: {self.app.move_sequence}")

            self.app.save_game_result()

            # Since this is an integration test, manually verify the data in Firestore
            print("Check Firestore to verify that the data was saved correctly.")
            print("test_save_game_result_integration passed")
        except Exception as e:
            print("test_save_game_result_integration failed")
            raise e
        finally:
            print("Finished test_save_game_result_integration")

if __name__ == "__main__":
    unittest.main()