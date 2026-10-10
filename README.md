# LangGraph Chatbot with FastAPI and Streamlit

A conversational AI chatbot built with **LangGraph**, **FastAPI**,
**Streamlit**, and **SQLite**. Streamlit provides the user interface,
FastAPI exposes HTTP endpoints, LangGraph manages the conversation
workflow, and SQLite stores LangGraph checkpoints so conversations can
be revisited.

## Features

-   Chat with a hosted language model through an OpenAI-compatible API.
-   Separate frontend and backend responsibilities.
-   FastAPI endpoints for creating conversations, sending messages,
    listing conversations, and loading conversation history.
-   LangGraph state management and checkpoint persistence with SQLite.
-   Streamlit sidebar for starting a new chat and switching between
    saved conversations.
-   Interactive API documentation provided by FastAPI.
-   Environment-variable configuration for API credentials.

## Architecture

``` text
Streamlit Frontend
       |
       | HTTP requests / JSON
       v
FastAPI (backend/main.py)
       |
       | Python calls
       v
LangGraph Chatbot
       |
       +---- Hosted LLM API
       |
       +---- SQLite checkpoint database
```

### Main technologies

-   **Python** --- application language
-   **Streamlit** --- frontend UI
-   **FastAPI** --- REST API
-   **LangGraph** --- chatbot workflow and state
-   **LangChain OpenAI integration** --- connects to an
    OpenAI-compatible model endpoint
-   **SQLite** --- persistent LangGraph checkpoints
-   **Uvicorn** --- ASGI server
-   **Requests** --- HTTP calls from Streamlit to FastAPI
-   **python-dotenv** --- loads environment variables from `.env`

## Project structure

The structure below is a suggested layout matching the application
described in this project. Adjust filenames if yours differ.

``` text
Langgraph_chatbot_with_Fastapi/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── langgraph_backend_with_database.py
│   └── chatbot.db                 # Created/used by the backend
├── frontend/
│   └── streamlit_frontend_with_database.py
├── .env                           # Local secrets; do not commit
├── .gitignore
└── requirements.txt
```



## Requirements

-   Python installed
-   A virtual environment for project dependencies
-   An API key for the configured model provider
-   Internet access to call the hosted model API

## Setup

### 1. Clone the repository

``` bash
git clone https://github.com/thesagarraut/Conversational-AI-Chatbot
cd Langgraph_chatbot_with_Fastapi
```

Replace `https://github.com/thesagarraut/Conversational-AI-Chatbot` with your repository URL. If you already
have the project locally, open a terminal in its root directory instead.

### 2. Create and activate a virtual environment

**Windows PowerShell**

``` powershell
python -m venv .new_venv
.\.new_venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt:

``` bat
.new_venv\Scripts\activate.bat
```

### 3. Install dependencies

If the project has a `requirements.txt` file:

``` bash
python -m pip install -r requirements.txt
```

The application uses packages such as:

``` text
fastapi
uvicorn[standard]
streamlit
requests
langgraph
langgraph-checkpoint-sqlite
langchain-core
langchain-openai
python-dotenv
```

Keep any additional dependencies required by your actual backend in
`requirements.txt`. Package versions may be pinned after testing.

### 4. Configure the API key

Create a `.env` file in the project root. For the Groq configuration
described for this project, use:

``` dotenv
GROQ_API_KEY=your_groq_api_key_here
```

The LangGraph backend should load the key with `load_dotenv()` and
configure `ChatOpenAI` with the provider's OpenAI-compatible endpoint.
For example:

``` python
llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)
```

Confirm that the selected model is available to your provider account
and that your account has remaining usage. Provider models, free-tier
limits, and availability can change.



### 5. Start FastAPI

From the project root, run:

``` bash
python -m uvicorn backend.main:app --reload
```

If `main.py` is in the `backend` directory, the import path
`backend.main:app` refers to the `app` object inside `backend/main.py`.

The API will normally be available at:

-   API root: `http://127.0.0.1:8000/`
-   Interactive documentation: `http://127.0.0.1:8000/docs`
-   OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

Keep this terminal running.

### 6. Start Streamlit

Open a second terminal, activate the same virtual environment, and run
the frontend using its actual path. For the suggested structure:

``` bash
streamlit run frontend/streamlit_frontend_with_database.py
```

If your frontend file is in the project root, use its root-level
filename instead.

The Streamlit frontend is configured to call:

``` python
API_URL = "http://127.0.0.1:8000"
```

Make sure FastAPI is running before using the chat UI.

## API endpoints

The FastAPI backend currently provides the following endpoints.

  ------------------------------------------------------------------------
  Method                  Endpoint                 Purpose
  ----------------------- ------------------------ -----------------------
  `GET`                   `/`                      Check that the API is
                                                   running

  `POST`                  `/threads`               Generate a new
                                                   conversation ID

  `GET`                   `/threads`               List thread IDs found
                                                   in saved LangGraph
                                                   checkpoints

  `GET`                   `/threads/{thread_id}`   Retrieve messages for a
                                                   conversation

  `POST`                  `/chat`                  Send a user message to
                                                   the chatbot and receive
                                                   an answer
  ------------------------------------------------------------------------

### Send a chat message

Example request to `POST /chat`:

``` json
{
  "thread_id": "demo-thread-001",
  "message": "Explain FastAPI in simple words."
}
```

The endpoint returns a JSON response similar to:

``` json
{
  "thread_id": "demo-thread-001",
  "user_message": "Explain FastAPI in simple words.",
  "answer": "FastAPI is a Python framework for building APIs..."
}
```

The answer shown here is illustrative; the actual response is generated
by the model.

### Try the API

1.  Start FastAPI.
2.  Open `http://127.0.0.1:8000/docs`.
3.  Expand an endpoint.
4.  Select **Try it out**.
5.  Enter the required values and execute the request.

## Conversation persistence

LangGraph is compiled with a SQLite checkpointer in the backend. The
`thread_id` is passed in the graph configuration to associate messages
with a conversation. Reusing the same thread ID allows LangGraph to
continue from that thread's saved state.

The frontend stores the currently displayed messages in Streamlit
session state, while the backend checkpoint database provides persisted
conversation state.

Creating a thread ID does not necessarily create a database row
immediately; a checkpoint is written when graph execution persists
state. The current thread-list endpoint discovers IDs from saved
checkpoints.

## Troubleshooting

### FastAPI cannot import `main`

Run Uvicorn from the project root:

``` bash
python -m uvicorn backend.main:app --reload
```

Check that `backend/main.py` exists and defines `app = FastAPI(...)`. If
the backend module imports are incorrect, update them to match your
package layout.

### Streamlit cannot connect to FastAPI

-   Confirm FastAPI is running at `http://127.0.0.1:8000`.
-   Check the `API_URL` value in the frontend.
-   Ensure both applications use the intended Python environment.
-   Check the FastAPI terminal for errors.

### The chat endpoint returns HTTP 500

Inspect the FastAPI terminal traceback. The API may be reachable even if
the model provider call fails. Check that the provider API key is
loaded, the key is valid, the model is available, and the account has
remaining usage.

### The provider returns 401, 403, or 429

-   **401:** check the API key.
-   **403:** check model access and account permissions.
-   **429:** check rate limits or usage quotas.

Provider error meanings can vary; use the provider's current
documentation for the exact response.

### Conversation history does not load

Verify that `GET /threads/{thread_id}` returns a `messages` array
containing objects with `role` and `content` fields, and that FastAPI
and Streamlit are using the same backend database.

## Current limitations

-   Chat responses use a regular request-response flow; token-by-token
    streaming through FastAPI has not been implemented yet.
-   Authentication and authorization for API clients have not been
    added.
-   Conversation deletion has not been implemented.
-   Thread listing currently returns IDs rather than metadata such as
    titles or last-updated timestamps.
-   The application is intended as a learning project and needs
    additional hardening before public production deployment.

## Future improvements

-   Add streaming responses using Server-Sent Events (SSE).
-   Add automated tests for API endpoints and chatbot behavior.
-   Add authentication and per-user conversation access controls.
-   Add conversation titles, timestamps, pagination, and deletion.
-   Improve structured logging and error handling.
-   Add CI/CD and deploy the frontend and backend.
-   Configure production secrets and deployment settings.


