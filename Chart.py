import firebase_admin
from firebase_admin import credentials, firestore
import matplotlib.pyplot as plt

# Initialize Firebase
def initialize_firebase():
    try:
        if not firebase_admin._apps:  # Check if Firebase is already initialized
            cred = credentials.Certificate("pdsa-cw-firebase-adminsdk-fekak-92d0a01b44.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db
    except ValueError as e:
        print(f"Error initializing Firebase: {e}")
        return None

# Fetch game results from Firebase
def fetch_game_results(db):
    try:
        docs = db.collection("TowerofHanoi").stream()
        results = [doc.to_dict() for doc in docs]
        return results
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# Plot the game times as a bar chart with disk numbers on top of the bars
def plot_game_times(results):
    if results:
        # Create labels like "Round 1", "Round 2", etc.
        labels = [f"Round {i+1}" for i in range(len(results))]
        times = [result['time_taken'] for result in results]
        num_disks = [result['num_disks'] for result in results]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, times, color='skyblue')
        plt.xlabel('Round')
        plt.ylabel('Time Taken (seconds)')
        plt.title('Time Taken for Each Game Round')

        # Annotate the number of disks at the top of each bar
        for bar, disks in zip(bars, num_disks):
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # x position
                bar.get_height(),  # y position (height of the bar)
                f'{disks} disks',  # text to display
                ha='center',  # horizontal alignment
                va='bottom'   # vertical alignment
            )

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    else:
        print("No results to plot")

if __name__ == "__main__":
    db = initialize_firebase()  # Initialize Firebase
    if db:
        results = fetch_game_results(db)  # Fetch game results
        plot_game_times(results)  # Plot the bar chart
