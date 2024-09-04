import firebase_admin
from firebase_admin import credentials, firestore
import matplotlib.pyplot as plt

# Initialize Firebase
def initialize_firebase():
    try:
        if not firebase_admin._apps:  # Check if Firebase is already initialized
            cred = credentials.Certificate("pdsa-cw-4fe71-firebase-adminsdk-mvt7n-55e5f9e362.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db
    except ValueError as e:
        print(f"Error initializing Firebase: {e}")
        return None

# Fetch game results from Firebase for a specific user
def fetch_game_results(db, username):
    try:
        # Query the collection for documents where the 'username' field is 'kusal'
        docs = db.collection("nqueens").where("username", "==", username).stream()
        results = [doc.to_dict() for doc in docs]
        return results
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# Plot the game times as a bar chart with moves numbers on top of the bars
def plot_game_times(results):
    if results:
        # Create labels like "Round 1", "Round 2", etc.
        labels = [f"Round {i+1}" for i in range(len(results))]
        times = [result['game_time'] for result in results]
        moves = [result['moves_count'] for result in results]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, times, color='#3572EF')
        plt.xlabel('Round')
        plt.ylabel('Time Taken (seconds)')
        plt.title('Time Taken for Each Game Round')

        # Annotate the number of moves at the top of each bar
        for bar, move_count in zip(bars, moves):
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # x position
                bar.get_height(),  # y position (height of the bar)
                f'{move_count} moves',  # text to display
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
        username = "Chanuka"
        results = fetch_game_results(db, username)  # Fetch game results for the specified user
        plot_game_times(results)  # Plot the bar chart
