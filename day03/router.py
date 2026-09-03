from day02.task2_2.intent_classifier import classify


FAQS = {
    "upi_issue": (
        "If your UPI payment failed but money was deducted, "
        "the transaction may be reversed automatically. "
        "If the issue persists, please contact support."
    ),

    "card_issue": (
        "If your debit or credit card is lost or stolen, "
        "you should hotlist the card immediately to prevent unauthorized transactions."
    ),

    "statement_issue": (
        "You can request an account statement for a specific month "
        "or a selected transaction period."
    ),

    "balance_issue": (
        "You can check your current account balance through your banking "
        "application, internet banking, or an authorized banking channel."
    ),
}



def answer_faq(utterance):
    """Return an FAQ answer when the question is covered."""
    text = utterance.lower()

    if any(word in text for word in ["upi", "gpay", "phonepe"]):
        return FAQS["upi_issue"]

    if any(word in text for word in ["card", "debit card", "credit card"]):
        return FAQS["card_issue"]

    if "statement" in text or "transactions" in text:
        return FAQS["statement_issue"]

    if "balance" in text:
        return FAQS["balance_issue"]

    return None


def call_mock_api(intent, entities):
    """Simulate a banking API call."""
    if intent == "card_hotlist":
        return {
            "status": "ok",
            "action": "card_hotlisted",
            "ref": "HTL-1029",
        }

    if intent == "statement_request":
        return {
            "status": "ok",
            "action": "statement_requested",
            "ref": "STM-2041",
            "period": entities.get("period", ""),
        }

    if intent == "balance_enquiry":
        return {
            "status": "ok",
            "action": "balance_retrieved",
            "balance": "₹25,430",
        }

    return {
        "status": "error",
        "action": "unsupported",
    }


def escalate(utterance, result):
    """Create a structured human handover."""
    intent = result.get("intent")
    confidence = result.get("confidence", 0.0)

    if confidence < 0.6:
        reason = "Low classifier confidence"
    elif intent == "out_of_scope":
        reason = "Request is outside supported banking scope"
    else:
        reason = "FAQ does not cover the customer's issue"

    return {
        "reason": reason,
        "intent": intent,
        "entities": result.get("entities", {}),
        "summary_for_agent": utterance,
    }


def route(utterance):
    """Classify the request and route it to the appropriate handler."""

    result = classify(utterance)

    intent = result.get("intent")
    confidence = result.get("confidence", 0.0)
    entities = result.get("entities", {})

    # Low confidence or unknown request
    if confidence < 0.6 or intent == "out_of_scope":
        return escalate(utterance, result)

    # Small talk
    if intent == "small_talk":
        return {
            "status": "ok",
            "reply": "Hello! How can I help you with your banking needs?"
        }

    # Mock API requests
    if intent in {
        "balance_enquiry",
        "card_hotlist",
        "statement_request",
    }:
        return call_mock_api(intent, entities)

    # UPI → FAQ first → escalate if not covered
    if intent == "upi_issue":
        answer = answer_faq(utterance)

        if answer:
            return {
                "status": "ok",
                "reply": answer,
            }

        return escalate(utterance, result)

    return escalate(utterance, result)


if __name__ == "__main__":

    while True:
        user = input("You: ")

        if user.lower() in {"quit", "exit"}:
            break

        print("Bot:", route(user))