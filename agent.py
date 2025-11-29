import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode, tools_condition
from tools import search_tool

load_dotenv()

# 1. Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Setup LLM & Tools
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
tools = [search_tool]
llm_with_tools = llm.bind_tools(tools)

# 3. Define Nodes
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# 4. Build Graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

# ToolNode handles the "Factual -> Search Tool" logic
tool_node = ToolNode(tools=[search_tool])
graph_builder.add_node("tools", tool_node)

# 5. Add Edges
graph_builder.add_edge(START, "chatbot")
# tools_condition checks: If factual (tool call) -> tools node, Else -> END
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot") # Loop back after tool usage (React pattern)

# 6. Compile Graph with Memory
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)