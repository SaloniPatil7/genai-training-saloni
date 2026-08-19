print("HELLO LLM SCRIPT STARTED")
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": "Say hello to a new AI engineering trainee in one sentence."
    }],
)

print(resp.choices[0].message.content)