import os
from io import StringIO
import pandas as pd
from google.cloud import storage
from langchain.agents import CSVAgent
from app.config import GCS_BUCKET_NAME, CHESS_DATA_FILE_PATH

def get_chess_data():
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(CHESS_DATA_FILE_PATH)
    data = blob.download_as_string()
    return pd.read_csv(StringIO(data.decode('utf-8')))

def query_chess_data(query):
    # Load the chess data
    df = get_chess_data()
    
    # Save the DataFrame to a temporary CSV file
    temp_csv_path = '/tmp/chess_data.csv'
    df.to_csv(temp_csv_path, index=False)
    
    # Initialize the CSV agent
    csv_agent = CSVAgent(file_path=temp_csv_path)
    
    # Perform the query
    result = csv_agent.query(query)
    
    # Debug: Print the result to see what is being returned
    print(result)
    
    # Return the result
    return {"response": result}