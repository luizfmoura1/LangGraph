import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import ChatOpenAI
from IPython.display import Image, display
from langchain_community.chat_models import ChatOpenAI


load_dotenv()

def _set_env(var: str):
    if not os.environ.get(var):
        raise ValueError(f"{var} não foi definido. Verifique o arquivo .env.")

_set_env("OPENAI_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN-PROJECT"] = "LangGraph tutorial"

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)
print(graph_builder)

llm = ChatOpenAI(model="gpt-4o-mini")


def chatbot(state: dict):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
