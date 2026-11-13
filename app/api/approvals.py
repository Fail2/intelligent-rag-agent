from fastapi import APIRouter, HTTPException, Request
from langgraph.types import Command

from app.api.schemas import ApprovalRequest, ApprovalResponse


router = APIRouter(prefix="/api", tags=["Approvals"])


@router.post("/approval", response_model=ApprovalResponse)
async def handle_approval(payload: ApprovalRequest, request: Request):
    graph = request.app.state.graph

    config = {
        "configurable": {
            "thread_id": payload.thread_id,
        }
    }

    # Retrieve the latest checkpoint for this conversation.
    snapshot = await graph.aget_state(config)

    # Collect interrupts that are still waiting for a response.
    pending_interrupts = [
        interrupt
        for task in snapshot.tasks
        for interrupt in task.interrupts
    ]

    if len(pending_interrupts) != 1:
        raise HTTPException(
            status_code=409,
            detail="No pending approval found for this conversation.",
        )

    approval = pending_interrupts[0].value

    # Verify the pending approval type.
    if not isinstance(approval, dict):
        raise HTTPException(
            status_code=409,
            detail="Invalid pending approval.",
        )

    if approval.get("type") != "email_approval":
        raise HTTPException(
            status_code=409,
            detail="Unsupported approval type.",
        )

    # Verify that the submitted approval ID matches the checkpoint.
    if approval.get("approval_id") != payload.approval_id:
        raise HTTPException(
            status_code=403,
            detail="Approval verification failed.",
        )

    # Resume the same graph thread.
    result = await graph.ainvoke(
        Command(
            resume={
                "approved": payload.approved,
                "approval_id": payload.approval_id,
            }
        ),
        config=config,
    )

    final_message = result["messages"][-1].content

    return ApprovalResponse(
        thread_id=payload.thread_id,
        status="completed",
        message=(
            final_message
            if isinstance(final_message, str)
            else str(final_message)
        ),
    )