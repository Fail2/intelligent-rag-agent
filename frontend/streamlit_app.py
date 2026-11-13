import uuid

import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000/api/chat"
APPROVAL_URL = "http://127.0.0.1:8000/api/approval"

st.set_page_config(
    page_title="Intelligent RAG Agent",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Intelligent RAG Agent")
st.caption("Your AI-powered assistant")

# Initialize session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! How can I help you today?",
        }
    ]

if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input
if prompt := st.chat_input(
    "Type your message...",
    disabled=st.session_state.pending_approval is not None,
):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = httpx.post(
                    API_URL,
                    json={
                        "thread_id": st.session_state.thread_id,
                        "message": prompt,
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()

                if data["status"] == "completed":
                    answer = data["message"]

                elif data["status"] == "approval_required":
                    st.session_state.pending_approval = data["approval"]
                    answer = "I need your approval before sending this email."

                else:
                    answer = "Unexpected response from the server."

            except httpx.HTTPError as error:
                answer = f"API connection error: {error}"

        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# Display HITL approval panel
approval = st.session_state.pending_approval

if approval:
    st.warning("⚠️ Human approval required")

    st.write(f"**Recipient:** {approval['recipient']}")
    st.write(f"**Subject:** {approval['subject']}")
    st.write("**Email body:**")
    st.info(approval["body"])

    col1, col2 = st.columns(2)

    with col1:
        approve = st.button("✅ Approve", use_container_width=True)

    with col2:
        reject = st.button("❌ Reject", use_container_width=True)

    if approve or reject:
        try:
            response = httpx.post(
                APPROVAL_URL,
                json={
                    "thread_id": st.session_state.thread_id,
                    "approval_id": approval["approval_id"],
                    "approved": approve,
                },
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": data["message"],
                }
            )

            st.session_state.pending_approval = None
            st.rerun()

        except httpx.HTTPError as error:
            st.error(f"Approval request failed: {error}")