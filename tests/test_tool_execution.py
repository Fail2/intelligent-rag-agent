from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from app.agent.model import get_chat_model
from app.agent.tools import tools

# Bind tools to the model
model_with_tools = get_chat_model().bind_tools(tools)

# Get a tool-call request from the LLM
response = model_with_tools.invoke(
    "What products and solutions does W3 Engineers publicly present?"
)

# Create a temporary graph containing ToolNode
builder = StateGraph(MessagesState)

builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "tools")
builder.add_edge("tools", END)

tool_graph = builder.compile()

# Execute the tool through the graph
result = tool_graph.invoke({"messages": [response]})

# Inspect the execution result
tool_message = result["messages"][-1]

print("Tool name:", tool_message.name)
print("Tool call ID:", tool_message.tool_call_id)
print("Tool result:", tool_message.content)