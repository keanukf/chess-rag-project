from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def transform_query(user_query):
    # Load the model and tokenizer
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Create a text2text-generation pipeline with the small FLAN-T5 model
    generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device="cpu")

    # Prepare the input prompt
    prompt = f"Rewrite the following user query into a clear, structured question that can be used to retrieve information from a table with the following columns: game_id, date, time, player, role, opponent, player_result, winner, rated, time_class. Make sure the rewritten query clearly specifies the relevant columns and filters to improve precision for querying the table: '{user_query}'"

    # Generate the transformed query
    result = generator(prompt, max_length=100, num_return_sequences=1, do_sample=True, temperature=0.2)

    # Return the transformed query
    return result[0]["generated_text"]
