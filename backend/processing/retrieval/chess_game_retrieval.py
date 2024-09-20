import pandas as pd
import os
from typing import Tuple, List
from transformers import pipeline, AutoTokenizer
from query_transformer import transform_query
import warnings

# Suppress FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

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
    model_name = "google/tapas-base-finetuned-wtq"
    tokenizer = AutoTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)

    return pipeline(
        task="table-question-answering",
        model=model_name,
        tokenizer=tokenizer,  # Use the explicitly configured tokenizer
        device=device
    )

def query_table(tqa: callable, question: str, df: pd.DataFrame) -> Tuple[str, List[Tuple[int, int]]]:
    
    transformed_question = transform_query(question)
    print(f"Transformed question: {transformed_question}")
    
    result = tqa(table=df, query=transformed_question)
    return result["answer"]

def process_questions(tqa: callable, df: pd.DataFrame):
    while True:
        question = input("Enter your question (or 'quit' to exit): ")
        if question.lower() == "quit":
            break
        print(f"\nOriginal question: {question}")
        answer = query_table(tqa, question, df)
        print(f"Answer: {answer}")

def main():
    df = load_filtered_chess_data()
    tqa = initialize_qa_pipeline()

    process_questions(tqa, df)

if __name__ == "__main__":
    main()