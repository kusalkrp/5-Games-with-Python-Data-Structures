import threading

class NQueensThread(threading.Thread):
    def __init__(self, start_row, n, solutions):
        super().__init__()
        self.start_row = start_row
        self.n = n
        self.solutions = solutions

    def run(self):
        board = [-1] * self.n
        solve(self.start_row, board, self.n, self.solutions)

def solve(row, board, n, solutions):
    if row == n:
        solutions.append(board[:])
        return
    for col in range(n):
        if is_safe(row, col, board):
            board[row] = col
            solve(row + 1, board, n, solutions)

def is_safe(row, col, board):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

if __name__ == "__main__":
    n = 16
    solutions = []
    threads = []

    for i in range(n):
        thread = NQueensThread(i, n, solutions)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Number of solutions: {len(solutions)}")
