import pandas as pd
from transformers import TapasTokenizer, TapasForQuestionAnswering
import torch

# Sample table data
data = {
    'Name': ['John', 'Emma', 'Alex'],
    'Age': [28, 32, 25],
    'City': ['New York', 'London', 'Paris']
}
table = pd.DataFrame(data)

# Initialize TAPAS model and tokenizer
model_name = "google/tapas-base-finetuned-wtq"
tokenizer = TapasTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
model = TapasForQuestionAnswering.from_pretrained(model_name, device="cpu")

# Sample question
question = "Who is the oldest person?"

# Tokenize input
inputs = tokenizer(table=table, queries=[question], padding='max_length', return_tensors="pt")

# Get model output
outputs = model(**inputs)

# Process results
predicted_answer_coordinates, predicted_aggregation_indices = outputs.logits, outputs.logits_aggregation
predicted_answer_coordinates = torch.argmax(predicted_answer_coordinates, dim=-1).squeeze().tolist()
predicted_aggregation_indices = torch.argmax(predicted_aggregation_indices, dim=-1).squeeze().tolist()

# Print results
print("Table:")
print(table)
print("\nQuestion:", question)
print("\nPredicted Answer Coordinates:", predicted_answer_coordinates)
print("Predicted Aggregation Index:", predicted_aggregation_indices)

# Interpret results
if predicted_aggregation_indices == 0:  # "NONE" aggregation
    selected_cells = [table.iat[coord // len(table.columns), coord % len(table.columns)] for coord in predicted_answer_coordinates if coord < len(table.columns) * len(table)]
    print("\nAnswer:", ", ".join(str(cell) for cell in selected_cells))
else:
    aggregation_operators = ["NONE", "SUM", "AVERAGE", "COUNT"]
    print("\nAggregation Operation:", aggregation_operators[predicted_aggregation_indices])
