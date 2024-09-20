import pandas as pd
import os
from typing import Tuple, List
from transformers import pipeline, AutoTokenizer
import torch

def load_filtered_chess_data() -> pd.DataFrame:
    """
    Load the filtered chess game data from CSV file into a pandas DataFrame.
    """
    csv_path = os.path.join("backend", "processing", "storage", "filtered_chess_games.csv")
    
    df = pd.read_csv(csv_path)
    
    # Convert all columns to string type
    df = df.astype(str)
    
    # Clean the data
    df = df.fillna("")  # Replace NaN with empty string
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Strip whitespace
    
    return df

def initialize_qa_pipeline():
    """
    Initialize the table question-answering pipeline with CPU support.
    """
    device = -1  # Use CPU
    print("Using CPU")

    model_name = "google/tapas-base-finetuned-wtq"
    
    # Initialize the tokenizer with the parameter set
    tokenizer = AutoTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)

    return pipeline(
        task="table-question-answering",
        model=model_name,
        tokenizer=tokenizer,  # Use the explicitly configured tokenizer
        device=device
    )

def query_table(tqa: callable, question: str, df: pd.DataFrame) -> Tuple[str, List[Tuple[int, int]]]:
    print("DataFrame shape:", df.shape)
    print("DataFrame columns:", df.columns)
    print("First few rows:")
    print(df.head())
    print("DataFrame dtypes:")
    print(df.dtypes)
    
    result = tqa(table=df, query=question)
    return result["answer"], result["coordinates"]

def process_questions(tqa: callable, df: pd.DataFrame):
    while True:
        question = input("Enter your question (or 'quit' to exit): ")
        if question.lower() == "quit":
            break
        print(f"\nQuestion: {question}")
        answer, coordinates = query_table(tqa, question, df)
        print(f"Answer: {answer}")
        print(f"Coordinates: {coordinates}")

def main():
    df = load_filtered_chess_data()
    tqa = initialize_qa_pipeline()

    process_questions(tqa, df)

if __name__ == "__main__":
    main()