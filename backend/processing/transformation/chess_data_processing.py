import pandas as pd
import os
from datetime import datetime

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # Return original if parsing fails

# Define the paths
input_csv_path = os.path.join("data", "raw", "chess_games_raw.csv")
output_csv_path = os.path.join("data", "processed", "chess_games_simple.csv")

# Load the CSV file
df = pd.read_csv(input_csv_path)

# Select only the essential columns
essential_columns = [
    "end_time", "white_username", "black_username", "white_result"
]

# Select only the important columns
df = df[essential_columns]

# Clean and format the data
df['end_time'] = df['end_time'].apply(format_date)
df['white_result'] = df['white_result'].map({'win': 'won', 'checkmated': 'lost', 'resigned': 'lost', 'timeout': 'lost', 'draw': 'draw'})

# Rename columns for clarity
df.columns = ['date', 'white_player', 'black_player', 'result']

# Create the processed directory if it doesn't exist
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Export the processed DataFrame to CSV
df.to_csv(output_csv_path, index=False)

print(f"Processed data saved to: {output_csv_path}")
print(f"Shape of the processed DataFrame: {df.shape}")
print("\nFirst few rows of the processed data:")
print(df.head())

