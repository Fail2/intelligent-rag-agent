import unittest
from unittest.mock import AsyncMock, patch

from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Command

from app.agent.tools import send_email_with_approval


def create_test_graph():
    builder = StateGraph(MessagesState)

    builder.add_node(
        "tools",
        ToolNode([send_email_with_approval]),
    )

    builder.add_edge(START, "tools")
    builder.add_edge("tools", END)

    return builder.compile(checkpointer=InMemorySaver())


def create_email_tool_call():
    return AIMessage(
        content="",
        tool_calls=[
            {
                "name": "send_email_with_approval",
                "args": {
                    "recipient_email": "test@example.com",
                    "subject": "HITL Test",
                    "body": "Testing email approval.",
                },
                "id": "call_email_1",
                "type": "tool_call",
            }
        ],
    )


class TestEmailHITL(unittest.IsolatedAsyncioTestCase):

    async def test_email_approval(self):
        graph = create_test_graph()
        config = {"configurable": {"thread_id": "approval_test"}}

        with patch(
            "app.agent.tools.deliver_email",
            new_callable=AsyncMock,
        ) as mock_send:

            mock_send.return_value = "test-message-id"

            # First execution: graph should pause for approval.
            result = await graph.ainvoke(
                {"messages": [create_email_tool_call()]},
                config=config,
            )

            interrupts = result["__interrupt__"]
            approval_request = interrupts[0].value

            self.assertEqual(
                approval_request["type"],
                "email_approval",
            )
            mock_send.assert_not_awaited()

            # Resume after approval.
            result = await graph.ainvoke(
                Command(
                    resume={
                        "approved": True,
                        "approval_id": approval_request["approval_id"],
                    }
                ),
                config=config,
            )

            mock_send.assert_awaited_once()

            self.assertIn(
                "Email sent successfully",
                result["messages"][-1].content,
            )

    async def test_email_rejection(self):
        graph = create_test_graph()
        config = {"configurable": {"thread_id": "rejection_test"}}

        with patch(
            "app.agent.tools.deliver_email",
            new_callable=AsyncMock,
        ) as mock_send:

            # First execution: graph should pause for approval.
            result = await graph.ainvoke(
                {"messages": [create_email_tool_call()]},
                config=config,
            )

            approval_request = result["__interrupt__"][0].value

            # Resume after rejection.
            result = await graph.ainvoke(
                Command(
                    resume={
                        "approved": False,
                        "approval_id": approval_request["approval_id"],
                    }
                ),
                config=config,
            )

            mock_send.assert_not_awaited()

            self.assertIn(
                "Email rejected",
                result["messages"][-1].content,
            )


if __name__ == "__main__":
    unittest.main()