import pandas as pd
import os

# Define the paths
input_csv_path = os.path.join("data", "raw", "chess_games_raw.csv")
output_csv_path = os.path.join("data", "processed", "chess_games_small.csv")

# Load the CSV file
df = pd.read_csv(input_csv_path)

# Convert all columns to string type
df = df.astype(str)

# Select the most important columns
important_columns = [
    "time_control", "end_time", "rated", "time_class",
    "white_username", "white_rating", "white_result",
    "black_username", "black_rating", "black_result", 
    "black_accuracy", "white_accuracy"
]

# Select only the important columns
df = df[important_columns]

# Clean the data
df = df.fillna('')  # Replace NaN with empty string
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Strip whitespace

# Create the processed directory if it doesn't exist
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Export the processed DataFrame to CSV
df.to_csv(output_csv_path, index=False)

print(f"Processed data saved to: {output_csv_path}")
print(f"Shape of the processed DataFrame: {df.shape}")
print("\nFirst few rows of the processed data:")
print(df.head())

