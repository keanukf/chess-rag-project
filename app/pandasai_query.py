import os
from io import StringIO
import pandas as pd
from google.cloud import storage
from pandasai import SmartDataframe
from pandasai.llm import BambooLLM
from app.config import GCS_BUCKET_NAME, CHESS_DATA_FILE_PATH

def get_chess_data():
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(CHESS_DATA_FILE_PATH)
    data = blob.download_as_string()
    return pd.read_csv(StringIO(data.decode('utf-8')))

def query_chess_data(query):
    df = get_chess_data()
    pandasai_api_key = os.environ.get("PANDASAI_API_KEY")
    llm = BambooLLM(api_key=pandasai_api_key)
    df_chess = SmartDataframe(df, config={"llm": llm})
    result = df_chess.chat(query)
    return result 