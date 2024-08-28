def solve_n_queens(n):
    solutions = []
    board = [-1] * n
    solve(0, board, n, solutions)
    return solutions

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
    solutions = solve_n_queens(n)
    print(f"Number of solutions: {len(solutions)}")
