import pandas as pd
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_date_time(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")
    except ValueError:
        return date_str, ""  # Return original date and empty time if parsing fails

def load_data(input_csv_path):
    """Load raw chess data from a CSV file."""
    logger.info(f"Loading data from {input_csv_path}")
    return pd.read_csv(input_csv_path)

def select_essential_columns(df):
    """Select only the essential columns from the DataFrame."""
    essential_columns = [
        "end_time", "white_username", "black_username", "white_result",
        "rated", "time_class"
    ]
    logger.info("Selecting essential columns")
    return df[essential_columns]

def clean_and_format_data(df):
    """Clean and format the chess data."""
    logger.info("Cleaning and formatting data")
    df["date"], df["time"] = zip(*df["end_time"].apply(format_date_time))
    df["white_result"] = df["white_result"].map({
        "win": "win", "checkmated": "loss", "resigned": "loss", "timeout": "loss",
        "draw": "draw", "repetition": "draw", "agreed": "draw", "timevsinsufficient": "draw",
        "insufficient": "draw", "stalemate": "draw", "50move": "draw",
        "bughousepartnerlose": "loss", "abandoned": "loss"
    })
    return df

def restructure_data(df):
    """Restructure the DataFrame to include both white and black player entries."""
    logger.info("Restructuring data")
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
            'winner': row['white_username'] if row['white_result'] == 'win' else (
                row['black_username'] if row['white_result'] == 'loss' else 'draw'),
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
            'player_result': 'win' if row['white_result'] == 'loss' else (
                'loss' if row['white_result'] == 'win' else 'draw'),
            'winner': row['white_username'] if row['white_result'] == 'win' else (
                row['black_username'] if row['white_result'] == 'loss' else 'draw'),
            'rated': row['rated'],
            'time_class': row['time_class']
        })

    return pd.DataFrame(restructured_data)

def save_data(df, output_csv_path):
    """Save the processed DataFrame to a CSV file."""
    logger.info(f"Saving processed data to {output_csv_path}")
    df.to_csv(output_csv_path, index=False)

def main():
    # Define the paths
    input_csv_path = os.path.join("data", "raw", "chess_games_raw.csv")
    output_csv_path = os.path.join("data", "processed", "chess_games_simple.csv")

    # Load, process, and save the data
    df = load_data(input_csv_path)
    df = select_essential_columns(df)
    df = clean_and_format_data(df)
    processed_df = restructure_data(df)
    save_data(processed_df, output_csv_path)

# This part will only run if the script is executed directly (not when imported as a module)
if __name__ == "__main__":
    main()
