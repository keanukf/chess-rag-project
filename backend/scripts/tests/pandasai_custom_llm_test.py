import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import BambooLLM
import time
from pandasai.llm.base import LLM
from cohere import Client  # Assuming you have a Cohere client library

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

class CohereLLM(LLM):
    def __init__(self, api_key: str):
        self.client = Client(api_key)
        self.api_key = api_key

    def call(self, instruction: str, context=None) -> str:
        # Implement the call method to interact with the Cohere API
        response = self.client.generate(
            model='large',  # Specify the model you want to use
            prompt=instruction,
            max_tokens=100  # Adjust as needed
        )
        return response.generations[0].text

    def type(self) -> str:
        return "Cohere"

# Example usage
cohere_llm = CohereLLM(api_key="your_cohere_api_key")
response = cohere_llm.call("What is the capital of France?")
print(response)
