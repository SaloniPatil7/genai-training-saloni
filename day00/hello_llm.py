import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("OPENROUTER_API_KEY")

print("API KEY LOADED:", key is not None)
print("API KEY START:", key[:10] if key else None)
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

resp = client.chat.completions.create(
    model="openai/gpt-oss-20b:free",
    messages=[
        {
            "role": "user",
            "content": "Say hello to a new AI engineering trainee in one sentence."
        }
    ],
)

print(resp.choices[0].message.content)