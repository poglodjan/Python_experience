from camel.models import OpenAIModel
import os

def get_openai_model():
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAIModel(model_name="gpt-3.5-turbo", api_key=api_key)