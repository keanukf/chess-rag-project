import pandas as pd
import os
from typing import Tuple, List
from transformers import pipeline, AutoTokenizer
from query_transformer import transform_query
import warnings
import re
from collections import Counter

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

def process_tapas_result(result: dict) -> str:
    aggregation_operators = {
        "NONE": lambda x: ", ".join(x),
        "COUNT": lambda x: str(len(set(x))),
        "SUM": lambda x: str(sum(float(v) for v in x if v.replace('.','').isdigit())),
        "AVERAGE": lambda x: str(sum(float(v) for v in x if v.replace('.','').isdigit()) / len(x)) if x else "0",
        "MIN": lambda x: str(min(x)),
        "MAX": lambda x: str(max(x))
    }
    
    aggregator = result.get("aggregator")
    answer = result.get("answer", "")
    cells = result.get("cells", [])
    
    print(f"\nDebug - Aggregator: {aggregator}")
    print(f"Debug - Raw Answer: {answer}")
    print(f"Debug - Cells: {cells}")
    
    if aggregator in aggregation_operators:
        processed_answer = aggregation_operators[aggregator](cells)
        print(f"Debug - Processed Answer: {processed_answer}")
        return processed_answer
    else:
        print(f"Debug - Returning Raw Answer: {answer}")
        return answer

def query_table(tqa: callable, question: str, df: pd.DataFrame) -> str:
    transformed_question = transform_query(question)
    print(f"Transformed question: {transformed_question}")
    
    result = tqa(table=df, query=transformed_question)
    print(f"\nFull TAPAS result:\n{result}\n")  # Print the entire TAPAS result
    
    processed_answer = process_tapas_result(result)
    
    print(f"\nFinal Processed Answer: {processed_answer}")
    return processed_answer

def process_questions(tqa: callable, df: pd.DataFrame):
    print("Enter your questions. Press Enter without typing anything to quit.")
    while True:
        question = input("\nEnter your question: ").strip()
        if question == "":
            print("Exiting. Thank you for using the chess game retrieval system!")
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