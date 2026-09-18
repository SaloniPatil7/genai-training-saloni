import json
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_openai.chat_models.base import OpenAIRateLimitError


load_dotenv(".env")


# ============================================================
# 1. MOCK DATA FILE
# ============================================================

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "mock_data.json"
)


def load_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)


# ============================================================
# 2. TOOL: GET BALANCE
# ============================================================

@tool
def get_balance(account_id: str) -> str:
    """Return the current balance for an account id like ACC1001."""

    data = load_data()

    if account_id not in data:
        return f"Error: account {account_id} was not found."

    balance = data[account_id]["balance"]

    return f"Account {account_id} balance is {balance:.2f} NovaCredits."


# ============================================================
# 3. TOOL: HOTLIST CARD
# ============================================================

@tool
def hotlist_card(card_last4: str, reason: str) -> str:
    """Block a card by its last 4 digits and return a reference number."""

    # Validate that card number is exactly 4 digits
    if not card_last4.isdigit() or len(card_last4) != 4:
        return "Error: card_last4 must contain exactly 4 digits."

    data = load_data()

    # Check whether the card exists
    card_found = False

    for account in data.values():
        if card_last4 in account["cards"]:
            card_found = True
            break

    if not card_found:
        return f"Error: card ending {card_last4} was not found."

    # Synthetic reference number
    reference = "HTL-1029"

    return (
        f"Card **{card_last4} hotlisted successfully "
        f"for reason: {reason}. Ref {reference}"
    )


# ============================================================
# 4. MODEL
# ============================================================

model = ChatOpenAI(
    model="minimax/minimax-m3:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)


# ============================================================
# 5. SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a customer-service assistant for a fictional bank.

Use the provided tools whenever balance or card-hotlisting information
is required.

Rules:
- Never invent an account balance.
- Never invent a hotlisting reference number.
- If an account or card is not found, report the tool's error honestly.
- If a request requires more than one tool, use the necessary tools
  in the correct order.
- Keep the final answer short and clear.
"""


# ============================================================
# 6. CREATE REACT AGENT
# ============================================================

agent = create_agent(
    model=model,
    tools=[get_balance, hotlist_card],
    system_prompt=SYSTEM_PROMPT,
)


# ============================================================
# 7. RUN ONE QUESTION
# ============================================================

def run_agent(question):

    print("\n" + "=" * 70)
    print("USER:")
    print(question)

    try:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        )
    except OpenAIRateLimitError:
        print("\nMODEL RATE LIMITED:")
        print("The OpenRouter free model is temporarily rate-limited. Please retry in a minute or use a paid/custom API key.")
        return None

    print("\nAGENT TRACE:")

    for message in result["messages"]:
        print(type(message).__name__, ":", message.content)

        # Show tool calls if present
        if isinstance(message, dict):
            tool_calls = message.get("tool_calls")
        else:
            tool_calls = getattr(message, "tool_calls", None)

        if tool_calls:
            print("Tool calls:", tool_calls)

    print("\nFINAL ANSWER:")
    print(result["messages"][-1].content)

    return result


# ============================================================
# 8. TEST CONVERSATIONS
# ============================================================

questions = [
    "What's the balance of ACC1001?",

    "Block my card ending 4412, I lost it.",

    (
        "I lost my card ending 4412 — block it and then tell me "
        "my remaining balance in ACC1001."
    ),

    "What's the balance of ACC9999?"
]


for question in questions:
    run_agent(question)