import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Get the Hugging Face token from the environment variable
huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")

# Check if the token is available
if not huggingface_token:
    raise ValueError("HUGGINGFACE_TOKEN is not set in the environment variables.")

def generate_answer(question):
    # Load the model and tokenizer
    model_name = "meta-llama/Meta-Llama-3.1-8B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=huggingface_token)
    print("Tokenizer loaded successfully.")
    
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        token=huggingface_token,
        torch_dtype=torch.float16,
        device_map="auto",
        low_cpu_mem_usage=True
    )
    print("Model loaded successfully.")

    # Prepare the input
    prompt = f"Human: {question}\n\nAssistant: "
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate the response
    print("Generating response...")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
    print("Response generated.")

    # Decode and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("Assistant: ")[-1].strip()

# Test the function
def main():
    question = "What is the capital of France?"
    print(f"Question: {question}")
    answer = generate_answer(question)
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()

