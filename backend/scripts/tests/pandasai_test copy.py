import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import BambooLLM
import time

# Get the PandasAI API key from the environment variable
pandasai_api_key = os.environ.get("PANDASAI_API_KEY")

# Check if the API key is available
if not pandasai_api_key:
    raise ValueError("PANDASAI_API_KEY is not set in the environment variables.")

# Initialize the BambooLLM
llm = BambooLLM(api_key=pandasai_api_key)

print("\nChess Games Analysis")
print("----------------------------------")

# Load the chess games data
chess_data_path = 'data/processed/chess_games_simple.csv'
chess_df = pd.read_csv(chess_data_path)

# Initialize SmartDataframe with the chess data and BambooLLM
df_chess = SmartDataframe(chess_df, config={"llm": llm})

# Single query to test
chess_query = "How many games did Hikaru play as white?"

# Run query and measure performance
start_time = time.time()
result = df_chess.chat(chess_query)
end_time = time.time()

print(f"\nQuery: {chess_query}")
print(f"Result: {result}")
print(f"Time taken: {end_time - start_time:.2f} seconds")
print("-" * 50)
