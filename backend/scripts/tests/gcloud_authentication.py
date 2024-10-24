import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/keanuprivatbenutzer/gcloud_information/chess-chatbot-6e773e8c4ba2.json'

client = storage.Client()
buckets = list(client.list_buckets())
print(buckets)