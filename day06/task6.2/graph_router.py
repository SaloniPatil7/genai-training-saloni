from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from intent_classifier import classify


# 1. STATE

class State(TypedDict):
    user_input: str
    intent: str
    confidence: float
    response: str
    handover: dict | None


# 2. CLASSIFY NODE


def classify_node(state: State):

    result = classify(state["user_input"])

    return {
        "intent": result.get("intent", "out_of_scope"),
        "confidence": result.get("confidence", 0.0)
    }


# ============================================================
# 3. FAQ NODE
# ============================================================

def faq_node(state: State):

    faq = {
        "upi_issue": (
            "For a UPI issue, please check the transaction status. "
            "If money was deducted, do not immediately repeat the payment."
        )
    }

    response = faq.get(
        state["intent"],
        "I could not find a suitable FAQ answer."
    )

    return {
        "response": response
    }


# ============================================================
# 4. MOCK API NODE
# ============================================================

def mock_api_node(state: State):

    intent = state["intent"]

    if intent == "balance_enquiry":

        response = {
            "status": "ok",
            "action": "balance_checked",
            "balance": "10000 NovaCredits"
        }

    elif intent == "card_hotlist":

        response = {
            "status": "ok",
            "action": "card_hotlisted",
            "ref": "HTL-1029"
        }

    elif intent == "statement_request":

        response = {
            "status": "ok",
            "action": "statement_requested",
            "ref": "STMT-2045"
        }

    else:

        response = {
            "status": "error",
            "action": "unsupported_intent"
        }

    return {
        "response": str(response)
    }


# ============================================================
# 5. ESCALATE NODE
# ============================================================

def escalate_node(state: State):

    handover = {
        "reason": (
            "Low confidence or unsupported customer request"
        ),
        "intent": state["intent"],
        "confidence": state["confidence"],
        "summary_for_agent": state["user_input"]
    }

    return {
        "response": (
            "I'm connecting you to a human support agent."
        ),
        "handover": handover
    }


# ============================================================
# 6. CONDITIONAL ROUTER
# ============================================================

def route_after_classification(state: State):

    intent = state["intent"]
    confidence = state["confidence"]

    # Low confidence → escalation
    if confidence < 0.6:
        return "escalate"

    # Out of scope → escalation
    if intent == "out_of_scope":
        return "escalate"

    # UPI → FAQ
    if intent == "upi_issue":
        return "faq"

    # Banking operations → mock API
    if intent in {
        "balance_enquiry",
        "card_hotlist",
        "statement_request"
    }:
        return "mock_api"

    # Anything unexpected → escalation
    return "escalate"


# ============================================================
# 7. BUILD GRAPH
# ============================================================

builder = StateGraph(State)


builder.add_node("classify", classify_node)
builder.add_node("faq", faq_node)
builder.add_node("mock_api", mock_api_node)
builder.add_node("escalate", escalate_node)


# START → classify
builder.add_edge(START, "classify")


# classify → different paths
builder.add_conditional_edges(
    "classify",
    route_after_classification,
    {
        "faq": "faq",
        "mock_api": "mock_api",
        "escalate": "escalate"
    }
)


# Handlers → END
builder.add_edge("faq", END)
builder.add_edge("mock_api", END)
builder.add_edge("escalate", END)


# Compile
app = builder.compile()


# ============================================================
# 8. REPL
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("BANKING GRAPH ROUTER")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 70)

    while True:

        user = input("\nYou: ")

        if user.lower() in {"quit", "exit"}:
            break

        result = app.invoke({
            "user_input": user,
            "intent": "",
            "confidence": 0.0,
            "response": "",
            "handover": None
        })

        print("\nBot:", result["response"])

        print("\nGraph State:")
        print("Intent:", result["intent"])
        print("Confidence:", result["confidence"])

        if result["handover"] is not None:
            print("Handover:", result["handover"])