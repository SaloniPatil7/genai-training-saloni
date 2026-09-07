from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# State
class State(TypedDict):
    name: str
    account_type: str
    message: str


# Node 1: Greet the customer
def greet(state: State):
    return {
        "message": f"Hello {state['name']}!"
    }


# Node 2: Set account type
def set_account_type(state: State):
    return {
        "account_type": "savings"
    }


# Node 3: Compose final message
def compose(state: State):
    return {
        "message": f"Hello {state['name']}! Your account type is {state['account_type']}."
    }


# Create graph
builder = StateGraph(State)

# Add nodes
builder.add_node("greet", greet)
builder.add_node("set_account_type", set_account_type)
builder.add_node("compose", compose)

# Connect nodes
builder.add_edge(START, "greet")
builder.add_edge("greet", "set_account_type")
builder.add_edge("set_account_type", "compose")
builder.add_edge("compose", END)

# Compile graph
graph = builder.compile()


# Run graph
result = graph.invoke({
    "name": "Asha",
    "account_type": "",
    "message": ""
})

print("Final State:")
print(result)