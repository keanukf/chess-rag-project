import torch
from transformers import pipeline
import time

def get_device():
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"

def transform_query(user_query, device):
    # Create a text2text-generation pipeline with the small FLAN-T5 model
    generator = pipeline("text2text-generation", model="google/flan-t5-small", device=device)

    # Prepare the input prompt
    prompt = f"Transform the following query into a more detailed and structured question for table analysis: '{user_query}'"

    # Generate the transformed query
    result = generator(prompt, max_length=100, num_return_sequences=1, temperature=0.7)

    # Return the transformed query
    return result[0]["generated_text"]

def compare_performance(user_query, num_runs=5):
    devices = ["cpu", "mps"] if torch.backends.mps.is_available() else ["cpu"]
    
    for device in devices:
        total_time = 0
        print(f"\nRunning on {device.upper()}:")
        
        for i in range(num_runs):
            start_time = time.time()
            transformed_query = transform_query(user_query, device)
            end_time = time.time()
            
            run_time = end_time - start_time
            total_time += run_time
            
            print(f"Run {i+1}: {run_time:.4f} seconds")
            if i == 0:
                print(f"Transformed query: {transformed_query}")
        
        avg_time = total_time / num_runs
        print(f"Average time on {device.upper()}: {avg_time:.4f} seconds")

# Example usage
user_query = "When did Hikaru last win?"
compare_performance(user_query)
