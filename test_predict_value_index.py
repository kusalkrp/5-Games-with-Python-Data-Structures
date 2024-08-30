import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from predict_value_index import PredictValueIndexGame  # Import your main class correctly

class TestPredictValueIndexGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = PredictValueIndexGame(self.root)  # Initialize the app correctly
        self.app.initialize_firebase = MagicMock()  # Mock Firebase initialization
        self.app.db = MagicMock()  # Mock Firestore client

    def tearDown(self):
        self.root.destroy()

    def test_go_to_algorithm_selection_valid_name(self):
        print("Starting test_go_to_algorithm_selection_valid_name")
        try:
            self.app.player_name.set("Player1")
            self.app.go_to_algorithm_selection()
            self.assertIs(self.app.current_frame, self.app.frames["AlgorithmSelection"])
            print("test_go_to_algorithm_selection_valid_name passed")
        except AssertionError as e:
            print("test_go_to_algorithm_selection_valid_name failed")
            raise e
        finally:
            print("Finished test_go_to_algorithm_selection_valid_name")

    def test_go_to_algorithm_selection_invalid_name(self):
        print("Starting test_go_to_algorithm_selection_invalid_name")
        try:
            self.app.player_name.set("")
            self.app.go_to_algorithm_selection()
            self.assertEqual(self.app.name_error_label.cget("text"), "Name cannot be empty")
            print("test_go_to_algorithm_selection_invalid_name passed")
        except AssertionError as e:
            print("test_go_to_algorithm_selection_invalid_name failed")
            raise e
        finally:
            print("Finished test_go_to_algorithm_selection_invalid_name")

    @patch.object(PredictValueIndexGame, 'binary_search')  # Properly patch the method in the class
    def test_start_game(self, mock_binary_search):
        print("Starting test_start_game")
        try:
            mock_binary_search.return_value = 2500
            self.app.selected_algorithm.set("Binary Search")
            self.app.start_game()
            self.assertIn(self.app.target, range(1, 1000001))
            self.assertEqual(self.app.results["Binary Search"]["index"], 2500)
            print("test_start_game passed")
        except AssertionError as e:
            print("test_start_game failed")
            raise e
        finally:
            print("Finished test_start_game")

    def test_update_game(self):
        print("Starting test_update_game")
        try:
            self.app.results = {"Binary Search": {"index": 2500, "time": 0.002}}
            self.app.target = 123456
            self.app.selected_algorithm.set("Binary Search")
            self.app.update_game()
            self.assertIn(f"Predict the index of {self.app.target}:", self.app.label_target.cget("text"))
            print("test_update_game passed")
        except AssertionError as e:
            print("test_update_game failed")
            raise e
        finally:
            print("Finished test_update_game")

    def test_submit_answer_correct(self):
        print("Starting test_submit_answer_correct")
        try:
            self.app.results = {"Binary Search": {"index": 2500, "time": 0.002}}
            self.app.var.set(2500)
            with patch('tkinter.messagebox.showinfo') as mock_showinfo:
                self.app.submit_answer()
                mock_showinfo.assert_called_with("Correct!", f"Well done, {self.app.player_name.get()}! You guessed correctly.")
            print("test_submit_answer_correct passed")
        except AssertionError as e:
            print("test_submit_answer_correct failed")
            raise e
        finally:
            print("Finished test_submit_answer_correct")

    def test_submit_answer_incorrect(self):
        print("Starting test_submit_answer_incorrect")
        try:
            self.app.results = {"Binary Search": {"index": 2500, "time": 0.002}}
            self.app.var.set(3000)
            with patch('tkinter.messagebox.showwarning') as mock_showwarning:
                self.app.submit_answer()
                mock_showwarning.assert_called_with("Incorrect", f"Sorry, {self.app.player_name.get()}. The correct index was 2500.")
            print("test_submit_answer_incorrect passed")
        except AssertionError as e:
            print("test_submit_answer_incorrect failed")
            raise e
        finally:
            print("Finished test_submit_answer_incorrect")

    @patch('predict_value_index.firestore')  # Correctly patch the firestore import from the module
    def test_save_result_to_firebase(self, mock_firestore):
        print("Starting test_save_result_to_firebase")
        try:
            mock_db = mock_firestore.client()
            self.app.db = mock_db

            self.app.player_name.set("Player1")
            self.app.target = 123456
            self.app.results = {"Binary Search": {"index": 2500, "time": 0.002}}

            self.app.save_result_to_firebase(2500, 2500)

            # Check if the Firestore client's add method was called with the correct data
            mock_db.collection.assert_called_once_with("predict_value_index")
            mock_db.collection().add.assert_called_once()
            saved_data = mock_db.collection().add.call_args[0][0]

            self.assertEqual(saved_data["player_name"], "Player1")
            self.assertEqual(saved_data["correct_answer"], 123456)
            self.assertEqual(saved_data["chosen_index"], 2500)
            self.assertEqual(saved_data["correct_index"], 2500)
            self.assertEqual(saved_data["search_method"], "Binary Search")
            self.assertEqual(saved_data["time_taken"], 0.002)
            print("test_save_result_to_firebase passed")
        except AssertionError as e:
            print("test_save_result_to_firebase failed")
            raise e
        finally:
            print("Finished test_save_result_to_firebase")

if __name__ == "__main__":
    unittest.main()
