from fastapi import APIRouter, Request
from langchain_core.messages import HumanMessage

from app.api.schemas import ChatRequest, ChatResponse


router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request):
    graph = request.app.state.graph

    config = {
        "configurable": {
            "thread_id": payload.thread_id,
        }
    }

    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=payload.message)]},
        config=config,
    )

    if "__interrupt__" in result:
        approval = result["__interrupt__"][0].value

        return ChatResponse(
            thread_id=payload.thread_id,
            status="approval_required",
            approval=approval,
        )

    return ChatResponse(
        thread_id=payload.thread_id,
        status="completed",
        message=result["messages"][-1].content,
    )