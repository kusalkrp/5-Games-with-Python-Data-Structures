import unittest
from firebase_admin import credentials, firestore, initialize_app
from firebase_admin.exceptions import FirebaseError
from SixteenQueensPuzzle import NQueensUI

class TestNQueensGame(unittest.TestCase):

    def setUp(self):
        # Initialize a 16x16 NQueensGame instance for testing
        self.game = NQueensUI.NQueensGame(size=16)

    def test_initial_setup(self):
        # Test if the game is initialized correctly
        self.assertEqual(self.game.size, 16)
        self.assertEqual(self.game.queens_left, 16)
        self.assertEqual(self.game.moves_count, 0)
        self.assertEqual(sum(sum(row) for row in self.game.board), 0)  # No queens placed yet
        
        self.addCleanup(lambda: print("Test 1: pass"))

    def test_valid_move(self):
        # Test placing a queen in a valid position
        self.assertTrue(self.game.place_or_remove_queen(0, 0))
        self.assertEqual(self.game.queens_left, 15)
        self.assertEqual(self.game.moves_count, 1)
        self.assertEqual(self.game.board[0][0], 1)
        
        self.addCleanup(lambda: print("Test 2: pass"))

    def test_invalid_move(self):
        # Test placing a queen in an invalid position (same row, col, or diagonal)
        self.game.place_or_remove_queen(0, 0)
        self.assertFalse(self.game.place_or_remove_queen(0, 1))  # Same row
        self.assertFalse(self.game.place_or_remove_queen(1, 0))  # Same column
        self.assertFalse(self.game.place_or_remove_queen(1, 1))  # Same diagonal
        
        self.addCleanup(lambda: print("Test 3: pass"))

    def test_remove_queen(self):
        # Test removing a queen from a position
        self.game.place_or_remove_queen(0, 0)
        self.assertTrue(self.game.place_or_remove_queen(0, 0))  # Removing the queen
        self.assertEqual(self.game.queens_left, 16)
        self.assertEqual(self.game.moves_count, 2)
        self.assertEqual(self.game.board[0][0], 0)
        
        self.addCleanup(lambda: print("Test 4: pass"))

    def test_move_paths(self):
        # Test the move paths tracking
        self.game.place_or_remove_queen(0, 0)
        self.assertEqual(self.game.move_paths[-1], "P(0, 0)")
        self.game.place_or_remove_queen(0, 0)  # Remove the queen
        self.assertEqual(self.game.move_paths[-1], "R(0, 0)")
        
        self.addCleanup(lambda: print("Test 5: pass"))

    def test_firebase_initialization(self):
        # Test if Firebase initializes correctly
        try:
            cred = credentials.Certificate("pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json")
            initialize_app(cred)
            db = firestore.client()
            self.assertIsNotNone(db)
        except FirebaseError as e:
            self.fail(f"Firebase initialization failed with error: {e}")
        except Exception as e:
            self.fail(f"An unexpected error occurred during Firebase initialization: {e}")
            
        self.addCleanup(lambda: print("Test 6: pass"))


if __name__ == "__main__":
    unittest.main()
