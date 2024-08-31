import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate(r'') 
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()
