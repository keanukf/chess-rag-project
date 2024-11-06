import os
import pandas as pd
from sqlalchemy import create_engine
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_chess_data():
    """
    Upload chess games data to Cloud SQL using Cloud SQL Proxy
    """
    try:
        # Database connection details
        DB_USER = os.getenv("DB_USER")
        DB_PASS = os.getenv("DB_PASS")
        DB_NAME = os.getenv("DB_NAME")
        DB_HOST = '127.0.0.1'  # Localhost, since the proxy routes traffic
        DB_PORT = '3306'       # Default MySQL port

        # Create the SQLAlchemy engine using the Cloud SQL Proxy connection
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

        # Path to your CSV file
        csv_file_path = 'data/chess_games_simple.csv'  # Update with your actual file path

        # Load CSV data into a DataFrame
        logger.info("Reading chess games data...")
        df = pd.read_csv(csv_file_path)

        # Upload DataFrame to SQL table
        # Replace 'chess_games' with the actual table name in your database
        logger.info("Uploading data to Cloud SQL...")
        df.to_sql('chess_games', con=engine, if_exists='replace', index=False)

        logger.info("Data uploaded successfully.")

    except Exception as e:
        logger.error(f"Error uploading data: {str(e)}")
        raise
    finally:
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
    upload_chess_data()
