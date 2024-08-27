import unittest
from unittest.mock import MagicMock
import tkinter as tk
from TowerofHanoi import TowerOfHanoi  # Adjust this import based on your project structure

class TestTowerOfHanoi(unittest.TestCase):
    def setUp(self):
        # Create the root window
        self.root = tk.Tk()
        # Initialize the TowerOfHanoi with the root window
        self.mock_app = TowerOfHanoi(self.root)
        # Mock Firebase and other dependencies if needed
        self.mock_root = MagicMock()

    def tearDown(self):
        # Destroy the root window after tests
        self.root.destroy()

    def test_check_win(self):
        # Test the check_win method
        # Setup your game state and call check_win
        self.mock_app.number_of_disks = 3
        self.mock_app.move_count = 7
        self.assertTrue(self.mock_app.check_win())

    def test_get_all_results(self):
        # Test the get_all_results method
        # Mock Firebase results if necessary
        mock_firebase = MagicMock()
        self.mock_app.firebase = mock_firebase
        mock_firebase.get.return_value = {
            'player1': {'moves': 5, 'time': '00:02:30'},
            'player2': {'moves': 8, 'time': '00:03:00'}
        }
        results = self.mock_app.get_all_results()
        expected_results = {
            'player1': {'moves': 5, 'time': '00:02:30'},
            'player2': {'moves': 8, 'time': '00:03:00'}
        }
        self.assertEqual(results, expected_results)

    def test_initialize_firebase(self):
        # Test the initialization of Firebase
        # Mock Firebase initialization and check if it's called correctly
        mock_firebase = MagicMock()
        self.mock_app.firebase = mock_firebase
        self.mock_app.initialize_firebase()
        mock_firebase.initialize_app.assert_called_once()

    def test_save_game_result(self):
        # Test saving a game result
        mock_firebase = MagicMock()
        self.mock_app.firebase = mock_firebase
        self.mock_app.save_game_result('player1', 5, '00:02:30')
        mock_firebase.collection('results').document('player1').set.assert_called_once_with({
            'moves': 5,
            'time': '00:02:30'
        })

    def test_start_game(self):
        # Test starting a new game
        self.mock_app.start_game()
        self.assertEqual(self.mock_app.move_count, 0)
        self.assertTrue(self.mock_app.is_game_running)

    def test_validate_disk_entry_invalid(self):
        # Test validation for invalid disk entry
        result = self.mock_app.validate_disk_entry("abc")
        self.assertFalse(result)

    def test_validate_disk_entry_valid(self):
        # Test validation for valid disk entry
        result = self.mock_app.validate_disk_entry("3")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
