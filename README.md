# Intelligent RAG Agent

An LLM-powered assistant built for **W3 Engineers Ltd.** that answers questions using a predefined knowledge base and performs actions through integrated tools.

The application combines Retrieval-Augmented Generation (RAG), LLM-driven tool selection, LangGraph orchestration, and Human-in-the-Loop (HITL) approval to provide a controlled AI assistant experience.

## Key Features

- **Knowledge-Based Q&A:** Retrieves relevant information from predefined PDF documents stored in ChromaDB and generates answers with source references.
- **LLM-Driven Tool Selection:** The LLM decides whether to answer directly, retrieve documents, or invoke an available tool.
- **Agent Orchestration:** LangGraph manages the agent's decision-making and tool-execution workflow.
- **Human-in-the-Loop (HITL):** Sensitive actions, such as sending emails, require explicit human approval before execution.
- **Persistent Conversations:** SQLite-backed LangGraph checkpointing preserves conversation state and supports workflow resumption.
- **Email Integration:** Integrates with Brevo to send emails through the approval-controlled workflow.
- **Text-Based Interaction:** Users communicate through messages without uploading documents.

## Architecture

```text
                         User Message
                              |
                              v
                            FastAPI
                              |
                              v
                        LangGraph Agent
                              |
                              v
                         LLM Decision
                              |
                 +------------+------------+
                 |            |            |
                 v            v            v
             Direct       RAG Search    Tool Call
             Response         |            |
                              v            v
                           ChromaDB     Tool Result
                 |            |            |
                 +------------+------------+
                              |
                              v
                        Final Response

                       Protected Actions
                              |
                              v
                        HITL Approval
                         /        \
                     Approve     Reject
                         \        /
                       Resume Workflow
```

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Agent Orchestration | LangGraph |
| LLM Integration | LangChain |
| Vector Database | ChromaDB |
| Conversation Persistence | SQLite |
| Checkpointing | LangGraph SQLite Checkpointer |
| Embeddings | Google Gemini Embeddings |
| Email Service | Brevo |
| Configuration | Environment Variables |
| Testing | Pytest |

## How It Works

1. The user sends a text message to the assistant.
2. The LLM decides whether the request requires a direct answer, document retrieval, or a tool.
3. For knowledge-based questions, the retrieval tool searches the predefined ChromaDB knowledge base.
4. The agent uses the retrieved context or tool results to generate a response.
5. If a protected action is requested, the workflow pauses and waits for human approval.
6. After approval or rejection, LangGraph resumes the workflow using its persisted state.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Fail2/intelligent-rag-agent.git
cd intelligent-rag-agent
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and configure the required credentials and settings:

```env
# LLM
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=your_model_name

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/app.db

# Vector Database
CHROMA_PERSIST_DIRECTORY=./data/chroma

# Google AI - Embeddings
GOOGLE_API_KEY=your_google_api_key
EMBEDDING_MODEL=gemini-embedding-2

# Brevo - Email Service
BREVO_API_KEY=your_brevo_api_key
```

**Required API keys:**
- `GROQ_API_KEY` — for LLM access.
- `GOOGLE_API_KEY` — for generating text embeddings.
- `BREVO_API_KEY` — for email integration.

Replace the placeholder values with your actual credentials. Keep `.env` private and never commit it to Git.

### 4. Prepare the Knowledge Base

The predefined documents are already available in the project's `documents/` directory and stored in ChromaDB. No initial document upload or ingestion is required.

To add new documents, place them in the `documents/` directory and run the following command from the project root:

```bash
uv run python -m tests.test_vector_store
```

This command processes the documents and stores their content and embeddings in ChromaDB.

**Note:** Document ingestion is handled by the developer or administrator. Users cannot upload documents through the chat interface.

### 5. Run the Application

**Start the FastAPI backend:**
```bash
uv run uvicorn app.main:app --reload
```
Backend will run at http://127.0.0.1:8000.

**Start the Streamlit frontend:**

Open a separate terminal in the project root and run:
```bash
uv run streamlit run frontend/streamlit_app.py
```
The Streamlit frontend will open at:

http://localhost:8501
## Implementation Status

### Implemented

- FastAPI application and API integration.
- LangGraph agent and tool-execution workflow.
- ChromaDB-based document retrieval with source references.
- LLM-driven tool selection.
- Human-in-the-Loop approval and workflow resumption.
- Brevo email integration.
- SQLite-backed conversation checkpointing.

### Not Implemented Yet

- Separate long-term memory CRUD functionality.
- Custom MCP server and client integration.

## Security Considerations

- Store credentials in environment variables.
- Keep `.env` out of version control; commit `.env.example` with placeholder values only.
- Validate tool inputs before execution.
- Enforce human approval for protected actions.
- Treat retrieved document content as reference data, not system instructions.
- Avoid committing secrets, local databases, and vector-store data.
- The pre-ingested ChromaDB `data/` folder is included in the repository to make it easier for the supervisor to review the project's knowledge base and verify the implementation.

## Project Objective

To develop a unified AI assistant that combines document-grounded question answering, intelligent tool usage, persistent agent workflows, and human oversight in a single application.