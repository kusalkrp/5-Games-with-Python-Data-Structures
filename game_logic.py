class NQueensGame:
    def __init__(self, size):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.queens_left = size
        self.moves_count = 0
        self.move_paths = []  # Store the move paths as a list of strings

    def is_valid_move(self, row, col):
        # Check the row
        for i in range(self.size):
            if self.board[row][i] == 1:
                return False

        # Check the column
        for i in range(self.size):
            if self.board[i][col] == 1:
                return False

        # Check the diagonals
        for i in range(self.size):
            for j in range(self.size):
                if abs(row - i) == abs(col - j) and self.board[i][j] == 1:
                    return False

        return True

    def place_or_remove_queen(self, row, col):
        if self.board[row][col] == 0:  # Try to place a queen
            if self.is_valid_move(row, col):
                self.board[row][col] = 1
                self.queens_left -= 1
                self.moves_count += 1
                self.move_paths.append(f"P({row}, {col})")
                return True
        else:  # Remove the queen
            self.board[row][col] = 0
            self.queens_left += 1
            self.moves_count += 1
            self.move_paths.append(f"R({row}, {col})")
            return True

        return False
