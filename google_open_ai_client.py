import os
from dotenv import load_dotenv
from openai import OpenAI

# Demonstrates calling Gemini using the OpenAI chat completion library.

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

load_dotenv(override=True)
api_key = os.getenv("GOOGLE_API_KEY")

gemini = OpenAI(base_url=GEMINI_BASE_URL, api_key=api_key)

response = gemini.chat.completions.create(
    model="gemini-2.5-flash",
    messages= [{"role": "user", "content": "Tell me a fun fact."}]
)

print(response.choices[0].message.content)