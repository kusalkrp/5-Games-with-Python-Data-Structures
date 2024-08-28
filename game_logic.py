class NQueensGame:
    def __init__(self, size):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.queens_left = size
        self.moves_count = 0

    def place_or_remove_queen(self, row, col):
        if self.board[row][col] == 1:
            # Remove the queen if it's already placed
            self.board[row][col] = 0
            self.queens_left += 1
            self.moves_count += 1
            return False  # Indicates removal
        elif self.is_valid_move(row, col):
            # Place the queen
            self.board[row][col] = 1
            self.queens_left -= 1
            self.moves_count += 1
            return True  # Indicates placement
        return False  # Invalid move

    def is_valid_move(self, row, col):
        for i in range(self.size):
            if self.board[row][i] == 1 or self.board[i][col] == 1:
                return False
        for i in range(-self.size, self.size):
            if 0 <= row + i < self.size and 0 <= col + i < self.size and self.board[row + i][col + i] == 1:
                return False
            if 0 <= row + i < self.size and 0 <= col - i < self.size and self.board[row + i][col - i] == 1:
                return False
        return True
