import json
from pathlib import Path

from langchain_core.tools import tool


# Find the capstone folder regardless of where the script is executed from
CAPSTONE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = CAPSTONE_DIR / "tools" / "mock_data.json"


def load_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)


@tool
def get_balance(account_id: str) -> str:
    """Return the current balance for an account such as ACC1001."""

    data = load_data()

    if account_id not in data:
        return f"Error: account {account_id} was not found."

    balance = data[account_id]["balance"]

    return (
        f"Account {account_id} balance is "
        f"{balance:.2f} NovaCredits."
    )


@tool
def hotlist_card(card_last4: str, reason: str) -> str:
    """Block a card using its last four digits."""

    if not card_last4.isdigit() or len(card_last4) != 4:
        return "Error: card_last4 must contain exactly 4 digits."

    data = load_data()

    for account in data.values():

        if card_last4 in account["cards"]:
            return (
                f"Card {card_last4} hotlisted. "
                f"Reason: {reason}. "
                f"Ref: HTL-1029"
            )

    return f"Error: card ending {card_last4} was not found."


@tool
def get_statement(account_id: str, period: str) -> str:
    """Return a fictional account statement for an account and period."""

    data = load_data()

    if account_id not in data:
        return f"Error: account {account_id} was not found."

    return (
        f"Statement for {account_id} - {period}\n"
        "01 Aug - Grocery Store - 1250.00 NovaCredits\n"
        "05 Aug - Salary Credit +45000.00 NovaCredits\n"
        "12 Aug - Electricity Bill - 2100.00 NovaCredits\n"
        "18 Aug - UPI Payment - 650.00 NovaCredits"
    )


BANKING_TOOLS = [
    get_balance,
    hotlist_card,
    get_statement
]