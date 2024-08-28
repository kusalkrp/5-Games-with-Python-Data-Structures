import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate(r'pdsa-cw-4fe71-firebase-adminsdk-mvt7n-831ea4b85d.json')  # Replace with your JSON file path
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()
