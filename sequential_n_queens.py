import time
from firebase_config import db

# Function to solve N-Queens problem and return all solutions
def solve_n_queens(n):
    solutions = []
    board = [-1] * n
    solve(0, board, n, solutions)
    return solutions

# Recursive function to solve the problem
def solve(row, board, n, solutions):
    if row == n:
        solutions.append(board[:])
        return
    for col in range(n):
        if is_safe(row, col, board):
            board[row] = col
            solve(row + 1, board, n, solutions)

# Function to check if placing a queen at (row, col) is safe
def is_safe(row, col, board):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

# Function to save a single solution to Firestore
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

# Function to estimate time complexity (for reference)
def estimate_time_complexity(n):
    import math
    return math.factorial(n)  # O(n!)

if __name__ == "__main__":
    n = 8  # n=16 is practically not possible

    # Start time for solution generation
    start_time_gen = time.time()

    # Generate all solutions
    solutions = solve_n_queens(n)

    # End time for solution generation
    end_time_gen = time.time()

    # Calculate and print the solution generation time
    solution_gen_time = end_time_gen - start_time_gen
    print(f"Solution generation time: {solution_gen_time:.2f} seconds")

    # Start time for saving solutions
    start_time_save = time.time()

    # Save solutions to Firestore
    for index, solution in enumerate(solutions):
        print(f"Saving solution {index + 1} to Firestore...")
        save_solution_to_db(solution, db)

    # End time for saving solutions
    end_time_save = time.time()

    # Calculate and print the saving time
    solution_save_time = end_time_save - start_time_save
    print(f"Solution saving time: {solution_save_time:.2f} seconds")

    # Calculate the total time
    total_time = solution_gen_time + solution_save_time
    print(f"Total time taken: {total_time:.2f} seconds")

    # Estimate and print the time complexity
    time_complexity = estimate_time_complexity(n)
    print(f"Estimated time complexity: O({n}!) = O({time_complexity})")

    print(f"Total number of distinct solutions saved: {len(solutions)}")
