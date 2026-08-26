import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

with open("day02/task2.1/complaint.txt", "r") as f:
    complaint = f.read()

# Prompt A
prompt_a = f"""
Summarize this email:

{complaint}
"""

# Prompt B
prompt_b = f"""
You are a complaints triage assistant for a bank.

Analyze the complaint below.

Return exactly these three fields:
- issue
- severity: low, medium, or high
- requested_action

Only use information contained in the complaint.
Do not invent any details.

Complaint:
{complaint}
"""

# Prompt A response
response_a = client.chat.completions.create(
    model="poolside/laguna-xs-2.1:free",
    messages=[
        {"role": "user", "content": prompt_a}
    ]
)

# Prompt B response
response_b = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {"role": "user", "content": prompt_b}
    ]
)

print("\n===== PROMPT A: SIMPLE =====")
print(response_a.choices[0].message.content)

print("\n===== PROMPT B: STRUCTURED =====")
print(response_b.choices[0].message.content)