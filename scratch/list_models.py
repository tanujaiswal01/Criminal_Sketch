import os
from google import genai
from dotenv import load_dotenv

# Load .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print(f"Using API Key: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    for model in client.models.list():
        print(f"Model Name: {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
