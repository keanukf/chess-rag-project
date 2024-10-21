from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def transform_query(user_query):
    # Load the model and tokenizer
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Create a text2text-generation pipeline with the small FLAN-T5 model
    generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device="cpu")

    # Prepare the input prompt
    #prompt = f"Rewrite the following user query into a clear, structured question that can be used to retrieve information from a table with the following columns: date, time, white_player, black_player, result, rated, and time_class. Make sure the rewritten query clearly specifies the relevant columns and filters to improve precision for querying the table: '{user_query}'"
    prompt = f"Given the following user question and CSV schema, transform the user query into a structured format that TAPAS can understand and process effectively. Ensure that the query accurately maps natural language elements to the corresponding columns in the CSV and frames the question in a clear, tabular way. Use the following rules for transformation: 1.	Identify the condition or outcome (e.g., “won”) and map it to the relevant column (e.g., 'result'). 2.	If the user is asking for a count, structure the query as a count over specific conditions (e.g., “How many rows have 'Hikaru' in 'player' and 'won' in 'result'?”). 3.	Ensure that any aggregation or comparison is explicitly stated in terms of the table structure which is (date, time, white_player, black_player, result, rated, and time_class). The user query is: '{user_query}'"

    # Generate the transformed query
    result = generator(prompt, max_length=100, num_return_sequences=1, do_sample=True, temperature=0.2)

    # Return the transformed query
    return result[0]["generated_text"]
