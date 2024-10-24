import os
import vertexai
from vertexai.preview.language_models import TextGenerationModel

# Set the path to your service account key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/keanuprivatbenutzer/gcloud_information/chess-chatbot-6e773e8c4ba2.json'

def test_bison_model():
    try:
        # Initialize Vertex AI
        vertexai.init(project="chess-chatbot", location="us-central1")

        # Initialize the Text Generation Model
        model = TextGenerationModel.from_pretrained("text-bison@001")

        # Define the parameters for the model
        parameters = {
            "temperature": 0.2,
            "max_output_tokens": 256,
            "top_p": 0.8,
            "top_k": 40,
        }

        # Make a prediction
        response = model.predict(
            'Is the Bison model available for use?',
            **parameters,
        )

        # Print the response
        print(f"Response from Model: {response.text}")

    except Exception as e:
        # Print any error encountered
        print(f"An error occurred: {e}")

# Execute the function
test_bison_model()



