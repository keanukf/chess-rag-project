from transformers import pipeline

def transform_query(user_query):
    # Create a text2text-generation pipeline with the small FLAN-T5 model
    generator = pipeline("text2text-generation", model="google/flan-t5-small", device="cpu")

    # Prepare the input prompt
    prompt = f"Transform the following query into a more detailed and structured question for table analysis: '{user_query}'"

    # Generate the transformed query
    result = generator(prompt, max_length=100, num_return_sequences=1, temperature=0.7)

    # Return the transformed query
    return result[0]["generated_text"]

# Example usage
user_query = "When did Hikaru last win?"
transformed_query = transform_query(user_query)
print(f"Original query: {user_query}")
print(f"Transformed query: {transformed_query}")
