import threading
import time
from firebase_config import db

# Function to check if a queen can be placed on board[row][col]
def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True

# Recursive function to solve problem
def solve_queens(board, col, solutions, n):
    if col >= n:
        solution = [(i, row.index(1)) for i, row in enumerate(board)]
        solutions.append(solution)
        return True
    
    res = False
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            res = solve_queens(board, col + 1, solutions, n) or res
            board[i][col] = 0
    
    return res

# Thread worker function
def find_solutions(thread_id, solutions, n):
    board = [[0]*n for _ in range(n)]
    solve_queens(board, 0, solutions, n)

# Function to save solutions to Firestore
def save_to_firestore(solutions):
    collection_ref = db.collection('threaded_solutions')
    for idx, solution in enumerate(solutions):
        # Convert each solution from a list of tuples to a list of strings
        solution_str = [f"({row},{col})" for row, col in solution]
        collection_ref.add({"solution": solution_str})
        print(f"Solution {idx + 1} saved")

def main():
    n = 8
    solutions = []
    threads = []

    # Start time for finding solutions
    find_start_time = time.time()

    # Create and start 4 threads separately
    thread1 = threading.Thread(target=find_solutions, args=(1, solutions, n))
    thread2 = threading.Thread(target=find_solutions, args=(2, solutions, n))
    thread3 = threading.Thread(target=find_solutions, args=(3, solutions, n))
    thread4 = threading.Thread(target=find_solutions, args=(4, solutions, n))

    threads.extend([thread1, thread2, thread3, thread4])

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # End time for finding solutions
    find_end_time = time.time()

    # Save distinct solutions to Firestore
    distinct_solutions = list(set(tuple(sol) for sol in solutions))

    # Start time for saving solutions
    save_start_time = time.time()
    save_to_firestore(distinct_solutions)
    # End time for saving solutions
    save_end_time = time.time()

    # Total time taken
    total_time_taken = (find_end_time - find_start_time) + (save_end_time - save_start_time)

    # Print results
    print(f"Number of distinct solutions: {len(distinct_solutions)}")
    print(f"Time taken to find solutions: {find_end_time - find_start_time} seconds")
    print(f"Time taken to save solutions: {save_end_time - save_start_time} seconds")
    print(f"Total time taken: {total_time_taken} seconds")

if __name__ == "__main__":
    main()
