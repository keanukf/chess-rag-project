import os
import pandas as pd
from google.cloud import storage
from src.data_fetching.chesscom_data_extraction import process_user_data
from src.transformation.chess_data_processor import process_chess_data
from src.retrieval.pandasai_retrieval import analyze_chess_data

# Initialize Google Cloud Storage client
storage_client = storage.Client()

def fetch_chess_data(request):
    """
    Fetches chess data from Chess.com API and stores it in Google Cloud Storage.
    """
    try:
        username = request.args.get('username')
        year = int(request.args.get('year'))
        start_month = int(request.args.get('start_month'))
        end_month = int(request.args.get('end_month'))

        games_data = process_user_data(username, year, start_month, end_month)
        df = pd.DataFrame(games_data)

        bucket_name = os.environ.get('GCS_BUCKET_NAME')
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f'raw/chess_games_raw_{username}_{year}.csv')
        blob.upload_from_string(df.to_csv(index=False), 'text/csv')

        return f"Data fetched and stored for {username} from {year}-{start_month} to {year}-{end_month}", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

def process_chess_data(request):
    """
    Processes raw chess data and stores the result in Google Cloud Storage.
    """
    try:
        bucket_name = os.environ.get('GCS_BUCKET_NAME')
        input_blob_name = request.args.get('input_blob')
        output_blob_name = request.args.get('output_blob')

        bucket = storage_client.bucket(bucket_name)
        input_blob = bucket.blob(input_blob_name)
        raw_data = pd.read_csv(input_blob.download_as_string())

        processed_data = process_chess_data(raw_data)

        output_blob = bucket.blob(output_blob_name)
        output_blob.upload_from_string(processed_data.to_csv(index=False), 'text/csv')

        return f"Data processed and stored as {output_blob_name}", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

def analyze_chess_data(request):
    """
    Analyzes processed chess data using PandasAI.
    """
    try:
        bucket_name = os.environ.get('GCS_BUCKET_NAME')
        input_blob_name = request.args.get('input_blob')
        query = request.args.get('query')

        bucket = storage_client.bucket(bucket_name)
        input_blob = bucket.blob(input_blob_name)
        chess_df = pd.read_csv(input_blob.download_as_string())

        result = analyze_chess_data(chess_df, query)

        return result, 200
    except Exception as e:
        return f"Error: {str(e)}", 500

