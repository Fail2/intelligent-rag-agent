from app.agent.model import get_chat_model
from app.agent.tools import tools
from langgraph.prebuilt import ToolNode

# Bind available tools to the model
model_with_tools = get_chat_model().bind_tools(tools)

# Ask a question that requires knowledge-base information
response = model_with_tools.invoke(
    "What products and solutions does W3 Engineers publicly present?"
)

# Inspect the LLM response
print("Content:", response.content)
print("Tool calls:", response.tool_calls)

tool_node = ToolNode(tools)