import os
import requests
from dotenv import load_dotenv

# Demonstrates calling OpenAI's API using a post request.

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

#call OpenAI HTTP endpoint

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-5-nano",
    "messages": [{"role": "user", "content": "Tell me a fun fact."}]
}

response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=payload
)

print(response.json()["choices"][0]["message"]["content"])