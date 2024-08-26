class NQueens:
    def __init__(self, size=16):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.queens_left = size

    def is_valid_move(self, row, col):
        # Check for another queen in the same row
        for i in range(col):
            if self.board[row][i] == 1:
                return False

        # Check upper diagonal on the left side
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        # Check lower diagonal on the left side
        for i, j in zip(range(row, self.size, 1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        return True

    def place_queen(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = 1
            self.queens_left -= 1
            return True
        else:
            return False

    def is_game_over(self):
        return self.queens_left == 0
