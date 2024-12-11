from typing_extensions import TypedDict
from IPython.display import display, Image
import random
from typing import Literal
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_msg: str


def node_01 (state: State):
    print(f"Node: {state['graph_msg']}")
    return {"graph_msg": state["graph_msg"] + "node_01"}

def node_02 (state: State):
    print(f"Node: {state['graph_msg']}")
    return {"graph_msg": state["graph_msg"] + "node_02"}

def node_03 (state: State):
    print(f"Node: {state['graph_msg']}")
    return {"graph_msg": state["graph_msg"] + "node_03"}


def select_next_node(state: State) -> Literal["node_02", "node_03"]:
    next_node = random.choice(["node_02", "node_03"])

    print (f"Selected node: {next_node}")
    return next_node

# Create builder
builder = StateGraph(State)

# Graph nodes

builder.add_node("node_01", node_01)
builder.add_node("node_02", node_02)
builder.add_node("node_03", node_03)

# Add edge
builder.add_edge(START, "node_01")
builder.add_conditional_edges("node_01", select_next_node)
builder.add_edge("node_02", END)
builder.add_edge("node_03", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

response = graph.invoke({"graph_msg": "Hello "})

response