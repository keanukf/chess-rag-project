from typing import List, Tuple
import pandas as pd
import torch
from transformers import pipeline
import warnings
import os

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning, module='transformers.tokenization_utils_base')

def load_chess_data() -> pd.DataFrame:
    """
    Load chess game data from a CSV file into a pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing chess game data.
    """
    csv_path = os.path.join("data", "raw", "chess_games_raw.csv")
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Convert all columns to string type
    df = df.astype(str)
    
    # Clean the data
    df = df.fillna('')  # Replace NaN with empty string
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Strip whitespace
    
    return df

def initialize_qa_pipeline():
    """
    Initialize the table question-answering pipeline.

    Returns:
        callable: The table question-answering pipeline function.
    """
    device = 0 if torch.cuda.is_available() else -1
    return pipeline(
        task="table-question-answering",
        model="google/tapas-base-finetuned-wtq",
        device=device,
        tokenizer_kwargs={"clean_up_tokenization_spaces": False}
    )

def query_table(tqa: callable, question: str, df: pd.DataFrame) -> Tuple[str, List[Tuple[int, int]]]:
    """
    Query the table with a given question.

    Args:
        tqa (callable): The table question-answering pipeline function.
        question (str): The question to ask about the table.
        df (pd.DataFrame): The DataFrame containing the table data.

    Returns:
        Tuple[str, List[Tuple[int, int]]]: The answer and the coordinates of the cells used for the answer.
    """
    result = tqa(table=df, query=question)
    return result['answer'], result['coordinates']

def process_questions(tqa: callable, questions: List[str], df: pd.DataFrame):
    """
    Process a list of questions and print the results.

    Args:
        tqa (callable): The table question-answering pipeline function.
        questions (List[str]): List of questions to process.
        df (pd.DataFrame): The DataFrame containing the table data.
    """
    for question in questions:
        print(f"\nQuestion: {question}")
        answer, coordinates = query_table(tqa, question, df)
        print(f"Answer: {answer}")
        print(f"Coordinates: {coordinates}")

def main():
    df = load_chess_data()
    tqa = initialize_qa_pipeline()

    questions = [
        "When was Hikaru's last loss?",
        "How many games did Magnus win?",
        "Who did Fabiano play against on July 30th?",
    ]

    process_questions(tqa, questions, df)

    print("\nDataframe:")
    print(df)

if __name__ == "__main__":
    main()