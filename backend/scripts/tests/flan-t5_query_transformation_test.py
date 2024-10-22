from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

def transform_query(user_query, model_name='google/flan-t5-small'):
    # Load the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Force CPU usage
    device = torch.device('cpu')
    model = model.to(device)

    # Create a text2text-generation pipeline with the FLAN-T5 model
    generator = pipeline('text2text-generation', model=model, tokenizer=tokenizer, device=device)

    # Refined prompt
    prompt = f"Rewrite the following user query into a clear, structured question that can be used to retrieve information from a table with the following columns: game_id, date, time, player, role, opponent, player_result, winner, rated, time_class. Make sure the rewritten query clearly specifies the relevant columns and filters to improve precision for querying the table: '{user_query}'"

    # Generate the transformed query
    result = generator(prompt, max_length=150, num_return_sequences=1, do_sample=True, temperature=0.3)

    # Return the transformed query
    return result[0]['generated_text'].strip()

def main():
    test_queries = [
        'When did Hikaru last win?',
        'How many games did Magnus play?',
        'Who\'s the best player?',
        'What\'s the most common time control?',
        'How often does white win?',
        'Are there any unrated games?',
        'Who plays the most?',
        'How many games did Hikaru win as black against Magnus?',
        'What\'s the average number of games played per day?',
        'Who has the highest win rate in blitz games?',
        'How many rated games were played in October 2023?'
    ]

    print('\nUsing model: google/flan-t5-small\n')
    for query in test_queries:
        try:
            transformed = transform_query(query)
            print(f'Original: {query}')
            print(f'Transformed: {transformed}')
            print('-' * 50)
        except Exception as e:
            print(f'Error processing query "{query}": {str(e)}')
            print('-' * 50)

if __name__ == '__main__':
    main()
