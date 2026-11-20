import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SENDER_REGISTRY_API_KEY")

if api_key:
    print("API key loaded successfully!")
    print("Key is present:", bool(api_key))
else:
    print("API key not found. Check your .env file.")