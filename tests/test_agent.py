from langchain_core.messages import HumanMessage

from app.agent.graph import graph


def test_agent(question: str):
    result = graph.invoke(
        {"messages": [HumanMessage(content=question)]},
    )

    print("\nQuestion:", question)
    print("\nFinal answer:", result["messages"][-1].content)


# Test 1: Knowledge-base question
test_agent("What products and solutions does W3 Engineers offer?")

# Test 2: General question
test_agent("What is the difference between Python lists and tuples?")