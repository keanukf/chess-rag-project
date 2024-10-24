import os
import pandas as pd
import time
from pandasai.agent import Agent
from pandasai.llm import GoogleVertexAI

# Set the path to the service account key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/keanuprivatbenutzer/gcloud_information/chess-chatbot-6e773e8c4ba2.json'

# Initialize the Google Vertex AI LLM
llm = GoogleVertexAI(
    project_id="chess-chatbot",
    location="us-central1",
    model="text-bison@001"
)

print("\nChess Games Analysis with Vertex AI")
print("----------------------------------")

# Load the chess games data
chess_data_path = 'data/processed/chess_games_simple.csv'
chess_df = pd.read_csv(chess_data_path)

# Initialize the Agent with the Google Vertex AI LLM
agent = Agent(chess_df, config={"llm": llm})

# Single query to test
chess_query = "How many games did Hikaru play as white?"

# Run query and measure performance
start_time = time.time()
try:
    response = agent.chat(chess_query)
except Exception as e:
    print(f"An error occurred: {e}")
    response = "An error occurred. Please try again later."
end_time = time.time()

print(f"\nQuery: {chess_query}")
print(f"Result: {response}")
print(f"Time taken: {end_time - start_time:.2f} seconds")
print("-" * 50)

# Add a delay to avoid hitting the rate limit
time.sleep(5)  # Adjust the sleep time as needed
