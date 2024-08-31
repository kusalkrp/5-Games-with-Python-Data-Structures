import time
from firebase_config import db

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

def save_solution_to_db(solution, db, collection_name="sequential_solutions"):
    queen_positions = []  # List to store the queen positions as strings (row, col)
    
    for row in range(len(solution)):
        col = solution[row]
        # Store the queen's position as a string "(row,col)"
        queen_positions.append(f"({row + 1},{col + 1})")

    # Store only the queen positions in Firestore
    db.collection(collection_name).add({
        "queen_positions": queen_positions  # List of strings representing positions
    })

def estimate_time_complexity(n):
    import math
    return math.factorial(n)  # O(n!)

if __name__ == "__main__":
    n = 16       # generate n=16 is practically not possible
    
    start_time = time.time()
    
    solutions = solve_n_queens(n)
    
    for index, solution in enumerate(solutions):
        print(f"Saving solution {index + 1} to Firestore...")
        save_solution_to_db(solution, db)
    
    # Measure the end time
    end_time = time.time()
    
    # Calculate and print the total runtime
    total_time = end_time - start_time
    print(f"Total time taken: {total_time:.2f} seconds")
    
    # Estimate and print the time complexity
    time_complexity = estimate_time_complexity(n)
    print(f"Estimated time complexity: O({n}!) = O({time_complexity})")
    
    print(f"Total number of distinct solutions saved: {len(solutions)}")
