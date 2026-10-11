# LangGraph Chatbot with FastAPI and Streamlit

A containerized AI chatbot built with **LangGraph**, **FastAPI**,
**Streamlit**, and **SQLite**. The Streamlit frontend communicates with
the FastAPI backend over HTTP, while LangGraph checkpointing stores
conversation state in a persistent SQLite volume.

## Architecture

``` text
User's browser
     |
     v
Streamlit frontend (:8501)
     |
     | HTTP requests via API_URL
     v
FastAPI backend (:8000)
     |
     +--> LangGraph chatbot + LLM provider
     |
     +--> SQLite checkpoint database (/app/data)
```

## Docker Hub images

-   **Backend:**
    [`7sagarraut/langgraph-chatbot-backend:1.0`](https://hub.docker.com/r/7sagarraut/langgraph-chatbot-backend)
-   **Frontend:**
    [`7sagarraut/langgraph-chatbot-frontend:1.0`](https://hub.docker.com/r/7sagarraut/langgraph-chatbot-frontend)

## Features

-   LangGraph-based chatbot workflow
-   FastAPI REST endpoints for chat and conversation/thread management
-   Streamlit chat interface
-   SQLite-backed LangGraph checkpoint persistence
-   Dockerized frontend and backend
-   Docker Compose orchestration and backend health check

## Prerequisites

-   Docker Desktop or Docker Engine with the Docker Compose plugin
-   An API key for the LLM provider configured by the backend
-   Internet access for pulling images and calling the LLM provider

## Run the published images with Docker Compose

### 1. Create a project folder

Create a folder, for example `langgraph-chatbot`, and create
`compose.yaml` inside it.

### 2. Create your `.env` file

In the same folder, create `.env` and add your own provider API key. For
the Groq configuration used by the backend, it should look like this:

``` dotenv
GROQ_API_KEY=your_groq_api_key_here
```

Use the environment variable name expected by your backend code if you
configured a different provider. **Never publish your real `.env` file
or API key.**

### 3. Add `compose.yaml`

``` yaml
services:
  volume-init:
    image: 7sagarraut/langgraph-chatbot-backend:1.0
    user: "0:0"
    command:
      - sh
      - -c
      - "mkdir -p /app/data && chown -R 10001:10001 /app/data"
    volumes:
      - chatbot_data:/app/data
    restart: "no"

  backend:
    image: 7sagarraut/langgraph-chatbot-backend:1.0
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - chatbot_data:/app/data
    depends_on:
      volume-init:
        condition: service_completed_successfully
    restart: unless-stopped
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=3)"
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s

  frontend:
    image: 7sagarraut/langgraph-chatbot-frontend:1.0
    environment:
      API_URL: http://backend:8000
    ports:
      - "8501:8501"
    depends_on:
      backend:
        condition: service_healthy
    restart: unless-stopped

volumes:
  chatbot_data:
```

### 4. Start the application

Run from the folder containing `compose.yaml` and `.env`:

``` bash
docker compose pull
docker compose up -d
docker compose ps
```

Open: - **Chat UI:** http://localhost:8501 - **FastAPI interactive
docs:** http://localhost:8000/docs

### 5. View logs

``` bash
docker compose logs -f backend
docker compose logs -f frontend
```

To stop the application:

``` bash
docker compose down
```

The named volume `chatbot_data` is retained when you run
`docker compose down`. Removing volumes explicitly can erase stored
conversation checkpoints; do that only if you intend to delete the data.

## API endpoints

  Method   Endpoint                 Purpose
  -------- ------------------------ -------------------------------
  `GET`    `/`                      Health-check/root endpoint
  `POST`   `/threads`               Create a conversation thread
  `GET`    `/threads`               Retrieve stored thread IDs
  `POST`   `/chat`                  Send a message to the chatbot
  `GET`    `/threads/{thread_id}`   Retrieve a thread's messages

Open <http://localhost:8000/docs> after starting the app to inspect
actual request and response schemas.

## Configuration notes

-   The frontend reaches the backend at `http://backend:8000` inside the
    Compose network. Do not replace `backend` with `localhost` in the
    frontend container configuration.
-   SQLite data is stored in the `chatbot_data` named volume mounted at
    `/app/data`.
-   The `volume-init` service fixes ownership of the data volume for the
    backend's non-root user (UID/GID `10001`).
-   This Compose file uses published `1.0` image tags. Update the tags
    when you publish a newer version.

## Security and production limitations

This project is intended as a learning and portfolio demo. Before
allowing unrelated users to use a public instance:

-   Add authentication and enforce authorization on every conversation
    endpoint.
-   Ensure each user can list and access only their own threads. Random
    thread IDs alone are not access control.
-   Keep API keys in environment/secret configuration, not in source
    code or image layers.
-   Configure HTTPS and appropriate request limits for public hosting.
-   Consider a managed database or a more suitable shared database setup
    if scaling beyond a small single-instance demo.

**Important:** The current thread-management endpoints may expose stored
thread IDs or conversation history if ownership checks are not
implemented. Do not use this deployment for sensitive or private
conversations until authentication and per-thread authorization are in
place.

## Technology stack

-   Python
-   LangGraph
-   FastAPI
-   Streamlit
-   SQLite / LangGraph checkpointing
-   Docker and Docker Compose
-   LLM provider API configured through environment variables


