import os
from dotenv import load_dotenv

load_dotenv()

# Load API keys from environment variables (GitHub Secrets)
PINECONE_API_KEY = os.getenv("PINE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PINECONE_ENVIRONMENT = "us-west1-gcp"
INDEX_NAME = "qa-bot"
