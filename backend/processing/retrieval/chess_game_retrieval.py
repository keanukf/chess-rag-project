import pandas as pd
import os
from typing import Tuple, List
from transformers import pipeline

def load_chess_data(max_rows=None) -> pd.DataFrame:
    """
    Load chess game data from the simplified CSV file into a pandas DataFrame.
    """
    csv_path = os.path.join('data', 'processed', 'chess_games_simple.csv')
    
    df = pd.read_csv(csv_path)
    if max_rows is not None:
        df = df.head(max_rows)
    
    # Convert all columns to string type
    df = df.astype(str)
    
    # Clean the data
    df = df.fillna('')  # Replace NaN with empty string
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Strip whitespace
    
    return df

def initialize_qa_pipeline():
    """
    Initialize the table question-answering pipeline.
    """
    return pipeline(
        task="table-question-answering",
        model="google/tapas-base-finetuned-wtq",
        tokenizer_kwargs={"clean_up_tokenization_spaces": False}
    )

def query_table(tqa: callable, question: str, df: pd.DataFrame) -> Tuple[str, List[Tuple[int, int]]]:
    print("DataFrame shape:", df.shape)
    print("DataFrame columns:", df.columns)
    print("First few rows:")
    print(df.head())
    print("DataFrame dtypes:")
    print(df.dtypes)
    
    result = tqa(table=df, query=question)
    return result['answer'], result['coordinates']

def process_questions(tqa: callable, questions: List[str], df: pd.DataFrame):
    for question in questions:
        print(f"\nQuestion: {question}")
        answer, coordinates = query_table(tqa, question, df)
        print(f"Answer: {answer}")
        print(f"Coordinates: {coordinates}")

def main():
    df = load_chess_data()
    tqa = initialize_qa_pipeline()

    questions = [
        "When was the most recent game?",
        "When was Magnus last loss as white?",
        "Who played the most games as black?"
    ]

    process_questions(tqa, questions, df)

if __name__ == "__main__":
    main()