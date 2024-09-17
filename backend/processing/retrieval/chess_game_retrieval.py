from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pandas as pd
import re

def extract_relevant_info(user_request: str) -> dict:
    # Load model and tokenizer
    model_name = "meta-llama/Meta-Llama-3.1-8B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

    # Prompt engineering for Llama
    prompt = f"""
    Given the following user request for chess games:
    "{user_request}"
    
    Extract and return only the relevant information that matches any of these columns:
    time_control, end_time, time_class, rules, white_username, white_rating, black_username, black_rating, result

    Format the output as a Python dictionary.
    """

    # Tokenize and generate
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.7)
    
    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract the dictionary from the generated text
    dict_match = re.search(r'\{.*\}', generated_text, re.DOTALL)
    if dict_match:
        extracted_dict = eval(dict_match.group())
        return extracted_dict
    else:
        return {}

def main():
    # Load the CSV file
    df = pd.read_csv("./data/raw/chess_games_raw.csv")
    
    user_request = input("Enter your chess game query: ")
    extracted_info = extract_relevant_info(user_request)
    print("Extracted information:")
    print(extracted_info)
    
    # Use the extracted information to filter the DataFrame
    query = " & ".join([f"{k} == '{v}'" for k, v in extracted_info.items() if k in df.columns])
    if query:
        filtered_df = df.query(query)
        print("\nFiltered games:")
        print(filtered_df)
    else:
        print("\nNo matching criteria found.")

if __name__ == "__main__":
    main()
