import asyncio

from langchain_core.messages import HumanMessage

from app.agent.graph import graph


async def test_agent(question: str):
    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=question)]},
    )

    print("\nQuestion:", question)
    print("\nFinal answer:", result["messages"][-1].content)


async def main():
    # Test 1: Knowledge-base question
    await test_agent("What products and solutions does W3 Engineers offer?")

    # Test 2: General question
    await test_agent("What is the difference between Python lists and tuples?")


if __name__ == "__main__":
    asyncio.run(main())