# LangGraph AI Chatbot with SQLite Memory

A conversational AI chatbot built using **LangGraph, LangChain, Streamlit, and SQLite**. The application supports streaming AI responses, multiple conversations, and persistent conversation state using LangGraph's SQLite checkpointing.

## Features

- **AI-powered conversations:** Interact with a language model through a chat interface.
- **LangGraph workflow:** Manage chatbot execution using a state graph.
- **Streaming responses:** Display AI responses incrementally as they are generated.
- **Multiple conversations:** Start new chats and switch between previous conversations.
- **Persistent conversation state:** Use SQLite checkpointing to store and retrieve conversation states.
- **Streamlit UI:** Provide an interactive web-based chatbot interface.
- **Environment-based configuration:** Load API credentials securely using environment variables.

## Tech Stack

- **Language:** Python
- **LLM Integration:** LangChain ChatOpenAI interface
- **LLM API:** Hugging Face Router
- **Workflow Orchestration:** LangGraph
- **Frontend:** Streamlit
- **Database and Checkpointing:** SQLite and LangGraph SQLite Checkpointer
- **Configuration:** python-dotenv

## Project Structure

```text
langgraph-ai-chatbot/
├── langgraph_backend_with_database.py
├── streamlit_frontend_with_database.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## Architecture

1. The user enters a message through the Streamlit chat interface.
2. The frontend sends the message to the LangGraph chatbot.
3. LangGraph maintains the conversation state using a message-based state schema.
4. The backend invokes the language model through LangChain.
5. The model response is streamed to the frontend.
6. SQLite checkpointing saves conversation state associated with a thread ID.
7. Users can create new conversations or return to previous conversations.

## Prerequisites

- Python 3.12 or a compatible version supported by your installed dependencies.
- A Hugging Face account and an API token with the required access.
- Git and VS Code (recommended).

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd langgraph-ai-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your Hugging Face API token:

```env
HUGGINGFACEHUB_ACCESS_TOKEN=your_huggingface_token_here
```

Replace the placeholder with your own token. Never commit your `.env` file or expose your API token publicly.

### 5. Run the application

Start the Streamlit frontend from the project root:

```bash
streamlit run streamlit_frontend_with_database.py
```

Streamlit will provide a local URL where you can interact with the chatbot.

## How to Use

1. Launch the application.
2. Enter a message in the chat input.
3. View the AI response as it streams into the conversation.
4. Select **New Chat** to begin another conversation.
5. Use the conversation sidebar to revisit available chat threads.

## Database and Persistence

The backend uses SQLite through Python's built-in `sqlite3` module and LangGraph's `SqliteSaver` checkpointer. Conversation checkpoints are stored in `chatbot.db`, allowing the application to retrieve conversation state by thread ID.

Keep the database file local unless you intentionally want to distribute conversation data. Do not commit private conversations or sensitive information to GitHub.

## Future Improvements

- Add user authentication and per-user conversation management.
- Introduce configurable model selection and chat parameters.
- Add conversation deletion and renaming.
- Improve error handling and API failure recovery.
- Deploy the application to a cloud hosting platform.
- Add automated tests for conversation handling and persistence.

.