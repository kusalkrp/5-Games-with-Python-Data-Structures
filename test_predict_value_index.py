import unittest
from unittest.mock import patch, MagicMock
from predict_value_index import PredictValueIndexGame

class TestPredictValueIndexGame(unittest.TestCase):

    @patch('tkinter.IntVar')
    @patch('tkinter.StringVar')
    def setUp(self, mock_stringvar, mock_intvar):
        # Mock StringVar and IntVar to avoid Tkinter root dependency
        mock_stringvar.return_value = MagicMock()
        mock_intvar.return_value = MagicMock()
        
        # Mock the Tkinter root window
        self.root = MagicMock()
        
        # Initialize the game with the mocked root window
        self.game = PredictValueIndexGame(self.root)

    def test_binary_search(self):
        arr = [1, 3, 5, 7, 9, 11]
        target = 7
        expected_index = 3
        self.assertEqual(self.game.binary_search(arr, target), expected_index)

    def test_jump_search(self):
        arr = [1, 3, 5, 7, 9, 11]
        target = 9
        expected_index = 4
        self.assertEqual(self.game.jump_search(arr, target), expected_index)

    def test_exponential_search(self):
        arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        target = 15
        expected_index = 7
        self.assertEqual(self.game.exponential_search(arr, target), expected_index)

    def test_fibonacci_search(self):
        arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        target = 13
        expected_index = 6
        self.assertEqual(self.game.fibonacci_search(arr, target), expected_index)

    def test_interpolation_search(self):
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        target = 70
        expected_index = 6
        self.assertEqual(self.game.interpolation_search(arr, target), expected_index)

@patch('firebase_admin.initialize_app')
@patch('firebase_admin.credentials.Certificate')
def test_initialize_firebase(self, mock_certificate, mock_initialize_app):
    mock_certificate.return_value = MagicMock()
    mock_initialize_app.return_value = True

    # Call the method to test Firebase initialization
    self.game.initialize_firebase()

    # Check if the Certificate was called with the correct argument
    try:
        mock_certificate.assert_called_once_with("pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json")
    except AssertionError as e:
        self.fail(f"Certificate was not called as expected: {e}")

    # Check if initialize_app was called
    try:
        mock_initialize_app.assert_called_once_with(mock_certificate.return_value)
    except AssertionError as e:
        self.fail(f"initialize_app was not called as expected: {e}")

if __name__ == '__main__':
    unittest.main()
