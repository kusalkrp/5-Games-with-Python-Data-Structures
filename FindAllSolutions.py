import tkinter as tk
from firebase_config import db

def check_and_reset_solutions(self):
    total_possible_solutions = 14772512  # Replace with actual total solutions count for 16-Queens

    # Fetch all records from Firebase
    records = db.collection("nqueens").get()
    current_solution_count = len(records)

    if current_solution_count >= total_possible_solutions:
        # Clear all records from the 'nqueens' collection
        docs = db.collection("nqueens").stream()
        for doc in docs:
            db.collection("nqueens").document(doc.id).delete()
        # Notify players that all solutions have been reset
        tk.messagebox.showinfo("Reset Complete", "All solutions have been identified. The system has been reset for new players.")
