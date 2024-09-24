import pandas as pd
import os
from typing import Tuple, List
from transformers import pipeline, AutoTokenizer
from query_transformer import transform_query
import warnings
import re
from collections import Counter
from sentence_transformers import SentenceTransformer, util

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

def initialize_reranker():
    """
    Initialize the sentence transformer model for reranking.
    """
    return SentenceTransformer('all-MiniLM-L6-v2')

def process_tapas_result(result: str) -> str:
    # Check for aggregation keywords
    agg_keywords = ['COUNT', 'SUM', 'AVERAGE', 'MIN', 'MAX']
    
    for keyword in agg_keywords:
        if result.startswith(keyword):
            # Extract values after the keyword
            values = result[len(keyword):].strip(' >').split(', ')
            
            if keyword == 'COUNT':
                return str(len(set(values)))  # Count unique values
            elif keyword == 'SUM':
                return str(sum(float(v) for v in values if v.replace('.','').isdigit()))
            elif keyword == 'AVERAGE':
                nums = [float(v) for v in values if v.replace('.','').isdigit()]
                return str(sum(nums) / len(nums)) if nums else "0"
            elif keyword == 'MIN':
                return min(values)
            elif keyword == 'MAX':
                return max(values)
    
    # If no aggregation, return the original result
    return result

def rerank_results(question: str, answers: List[str], reranker: SentenceTransformer) -> List[Tuple[str, float]]:
    """
    Rerank the answers based on their similarity to the question.
    """
    question_embedding = reranker.encode(question, convert_to_tensor=True)
    answer_embeddings = reranker.encode(answers, convert_to_tensor=True)
    
    similarities = util.pytorch_cos_sim(question_embedding, answer_embeddings)[0]
    
    reranked_results = list(zip(answers, similarities.tolist()))
    reranked_results.sort(key=lambda x: x[1], reverse=True)
    
    return reranked_results

def query_table(tqa: callable, question: str, df: pd.DataFrame, reranker: SentenceTransformer) -> str:
    transformed_question = transform_query(question)
    print(f"Transformed question: {transformed_question}")
    
    result = tqa(table=df, query=transformed_question)
    raw_answer = result["answer"]
    
    processed_answer = process_tapas_result(raw_answer)
    
    # Split the processed answer into individual results if it contains multiple items
    answer_list = [a.strip() for a in processed_answer.split(',') if a.strip()]
    
    if len(answer_list) > 1:
        reranked_results = rerank_results(question, answer_list, reranker)
        return ', '.join([result[0] for result in reranked_results])
    else:
        return processed_answer

def process_questions(tqa: callable, df: pd.DataFrame, reranker: SentenceTransformer):
    while True:
        question = input("Enter your question (or 'quit' to exit): ")
        if question.lower() == "quit":
            break
        print(f"\nOriginal question: {question}")
        answer = query_table(tqa, question, df, reranker)
        print(f"Answer: {answer}")

def main():
    df = load_filtered_chess_data()
    tqa = initialize_qa_pipeline()
    reranker = initialize_reranker()

    process_questions(tqa, df, reranker)

if __name__ == "__main__":
    main()