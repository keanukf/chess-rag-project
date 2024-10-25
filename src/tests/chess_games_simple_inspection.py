import pandas as pd
import os

def load_raw_chess_data():
    csv_path = os.path.join("data", "raw", "chess_games_raw.csv")
    return pd.read_csv(csv_path)

def print_distinct_values(df, column_name):
    distinct_values = df[column_name].unique()
    print(f"\nDistinct values in '{column_name}' column:")
    for value in sorted(distinct_values):
        print(value)
    print(f"Total distinct {column_name} values: {len(distinct_values)}")

def main():
    df = load_raw_chess_data()
    
    columns_to_check = ["white_result", "black_result", "time_class", "rated"]
    
    for column in columns_to_check:
        print_distinct_values(df, column)

if __name__ == "__main__":
    main()
