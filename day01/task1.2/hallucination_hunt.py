import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-oss-20b:free"

questions = [
    "What is the capital of Maharashtra?",
    "Who wrote the Ramayana?",
    "What are the annual charges of the Platinum Sapphire Credit Card from SuryaFirst Bank? This bank and card do not exist.",
    "What are the current RBI repo rate and today's date?",
    "What is the customer-care number of SuryaFirst Bank?"
]

for question in questions:
    print("\nQUESTION:", question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            },
            {
                "role": "system",
                "content": "If you are not certain or the information may be out of date, say 'I don't know' instead of guessing."
            }
        ]
    )

    answer = response.choices[0].message.content

    print("ANSWER:", answer)