import pandas as pd
import pytest

def load_chess_data():
    return pd.read_csv("data/processed/chess_games_simple.csv")

def test_result_column_values():
    df = load_chess_data()
    expected_results = {"won", "lost", "draw"}  # Add or modify based on expected values
    actual_results = set(df["result"].unique())
    assert actual_results == expected_results, f"Unexpected values in result column: {actual_results - expected_results}"

def test_rated_column_values():
    df = load_chess_data()
    expected_values = {True, False}
    actual_values = set(df["rated"].unique())
    assert actual_values == expected_values, f"Unexpected values in rated column: {actual_values - expected_values}"

def test_time_class_column_values():
    df = load_chess_data()
    expected_time_classes = {"blitz", "bullet", "daily", "rapid"}
    actual_time_classes = set(df["time_class"].unique())
    assert actual_time_classes.issubset(expected_time_classes), f"Unexpected values in time_class column: {actual_time_classes - expected_time_classes}"

# Add more tests as needed
