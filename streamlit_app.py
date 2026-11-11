import streamlit as st

st.set_page_config(
    page_title="Intelligent RAG Agent",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Intelligent RAG Agent")
st.caption("Your AI-powered assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! How can I help you today?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)
