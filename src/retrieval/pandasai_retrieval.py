import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import BambooLLM
import time
import logging

# Set up logging for Google Cloud Functions
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_chess_data(chess_df, query):
    try:
        # Get the PandasAI API key from the environment variable
        pandasai_api_key = os.environ.get("PANDASAI_API_KEY")

        # Check if the API key is available
        if not pandasai_api_key:
            raise ValueError("PANDASAI_API_KEY is not set in the environment variables.")

        # Initialize the BambooLLM
        llm = BambooLLM(api_key=pandasai_api_key)

        logger.info("Chess Games Analysis started")

        # Initialize SmartDataframe with the chess data and BambooLLM
        df_chess = SmartDataframe(chess_df, config={"llm": llm})

        # Run query and measure performance
        start_time = time.time()
        result = df_chess.chat(query)
        end_time = time.time()

        time_taken = end_time - start_time
        logger.info(f"Query executed. Time taken: {time_taken:.2f} seconds")

        return {
            "query": query,
            "result": result,
            "time_taken": time_taken
        }

    except Exception as e:
        logger.error(f"An error occurred during chess data analysis: {str(e)}")
        raise

# This part will only run if the script is executed directly (not when imported as a module)
if __name__ == "__main__":
    # Load the chess games data
    chess_data_path = 'data/processed/chess_games_simple.csv'
    chess_df = pd.read_csv(chess_data_path)

    # Single query to test
    chess_query = "How many games did Hikaru lose on 2024-01-02 and what are the opponents names?"

    result = analyze_chess_data(chess_df, chess_query)

    print(f"\nQuery: {result['query']}")
    print(f"Result: {result['result']}")
    print(f"Time taken: {result['time_taken']:.2f} seconds")
    print("-" * 50)
