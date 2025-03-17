import os
import json
from google.cloud import firestore
from google.oauth2 import service_account

# Load service account credentials
with open('new-key.json') as f:
    cred_dict = json.load(f)

# Create credentials object
cred = service_account.Credentials.from_service_account_info(cred_dict)

# Initialize Firestore client
db = firestore.Client(credentials=cred, project='telegram-jobs-bot-v2')

# Create a test document
doc_ref = db.collection('jobs').document('test')
doc_ref.set({
    'title': 'Test Job',
    'company': 'Test Company',
    'created_at': firestore.SERVER_TIMESTAMP
})

print("Firestore database initialized successfully!") 