
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SENDER_REGISTRY_API_KEY")

URL = "https://www.senderregistry.com/api/v1/check/email"

email = input("Enter an email address to check: ").strip()

if not API_KEY:
    print("ERROR: API key not found.")
else:
    try:
        response = requests.get(
            URL,
            params={"email": email},
            headers={
                "Authorization": f"Bearer {API_KEY}"
            },
            timeout=15
        )

        print("\nHTTP Status:", response.status_code)

        try:
            print("API Response:")
            print(response.json())
        except ValueError:
            print("Response:", response.text[:1000])

    except requests.RequestException as error:
        print("Connection error:", error)
