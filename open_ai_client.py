import os
from dotenv import load_dotenv
from openai import OpenAI

# Demonstrates calling OpenAI's model using a the chat completion library.

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI()

response = openai.chat.completions.create(
    model="gpt-5-nano",
    messages= [{"role": "user", "content": "Tell me a fun fact."}]
)

print(response.choices[0].message.content)