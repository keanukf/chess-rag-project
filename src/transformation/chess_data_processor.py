import pandas as pd
import os
from datetime import datetime

def format_date_time(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")
    except ValueError:
        return date_str, ""  # Return original date and empty time if parsing fails

# Define the paths
input_csv_path = os.path.join("data", "raw", "chess_games_raw.csv")
output_csv_path = os.path.join("data", "processed", "chess_games_simple.csv")

# Load the CSV file
df = pd.read_csv(input_csv_path)

# Select only the essential columns
essential_columns = [
    "end_time", "white_username", "black_username", "white_result",
    "rated", "time_class"
]

# Select only the important columns
df = df[essential_columns]

# Clean and format the data
df["date"], df["time"] = zip(*df["end_time"].apply(format_date_time))
df["white_result"] = df["white_result"].map({"win": "win", "checkmated": "loss", "resigned": "loss", "timeout": "loss", "draw": "draw", "repetition": "draw", "agreed": "draw", "timevsinsufficient": "draw", "insufficient": "draw", "stalemate": "draw", "50move": "draw", "bughousepartnerlose": "loss", "abandoned": "loss"})

# Create the restructured dataframe
restructured_data = []

for _, row in df.iterrows():
    # White player entry
    restructured_data.append({
        'date': row['date'],
        'time': row['time'],
        'player': row['white_username'],
        'role': 'white',
        'opponent': row['black_username'],
        'player_result': row['white_result'],
        'winner': row['white_username'] if row['white_result'] == 'win' else (row['black_username'] if row['white_result'] == 'loss' else 'draw'),
        'rated': row['rated'],
        'time_class': row['time_class']
    })
    
    # Black player entry
    restructured_data.append({
        'date': row['date'],
        'time': row['time'],
        'player': row['black_username'],
        'role': 'black',
        'opponent': row['white_username'],
        'player_result': 'win' if row['white_result'] == 'loss' else ('loss' if row['white_result'] == 'win' else 'draw'),
        'winner': row['white_username'] if row['white_result'] == 'win' else (row['black_username'] if row['white_result'] == 'loss' else 'draw'),
        'rated': row['rated'],
        'time_class': row['time_class']
    })

# Create the new dataframe
new_df = pd.DataFrame(restructured_data)

# Reorder columns to match the desired output
new_df = new_df[['date', 'time', 'player', 'role', 'opponent', 'player_result', 'winner', 'rated', 'time_class']]

# Add an index column
new_df.insert(0, 'game_id', range(1, len(new_df) + 1))

# Create the processed directory if it doesn't exist
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Export the processed DataFrame to CSV
new_df.to_csv(output_csv_path, index=False)

print(f"Processed data saved to: {output_csv_path}")
print(f"Shape of the processed DataFrame: {new_df.shape}")
print("\nFirst few rows of the processed data:")
print(new_df.head())
