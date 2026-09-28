# MemoryMeet AI — Meeting Prep Backend

> AI-powered meeting preparation with long-term, client-specific memory.

MemoryMeet AI helps teams prepare for recurring client meetings by recalling relevant information from previous conversations and combining it with the current meeting context.

This repository contains the **FastAPI backend** for MemoryMeet AI.

## What it does

The backend connects four main parts:

1. **FastAPI** — exposes the application API.
2. **Hindsight** — stores and recalls long-term client meeting memories.
3. **AI Agent** — uses recalled memories and current meeting context to generate a structured meeting brief.
4. **Frontend** — consumes the backend API and displays the preparation brief.

### Core flow

```text
Meeting Information
        |
        v
    FastAPI
        |
        v
 Hindsight Retain
        |
        v
 Hindsight Recall
        |
        v
   AI Agent / Groq
        |
        v
 Structured Meeting Brief
        |
        v
      Frontend
```

The important idea is that the system is **not limited to the current meeting**. It can recall relevant information from earlier meetings for the same client.

## Key Features

- Save meeting information through a REST API.
- Store meeting context in Hindsight long-term memory.
- Recall client-specific memories.
- Generate an AI-powered meeting preparation brief.
- Combine current meeting information with previous client context.
- Keep memories isolated by client.
- Return a consistent structured JSON response.
- Interactive API documentation through FastAPI/Swagger UI.

## AI Meeting Brief

The generated brief contains these sections:

- Client overview
- Previous interests
- Key concerns
- Important stakeholders
- Competitors
- Talking points
- Questions to ask
- Suggested next steps

The AI agent is instructed to use only the information supplied by the current meeting and recalled Hindsight memories and to avoid inventing facts.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend language |
| FastAPI | REST API |
| Pydantic | Request/response validation |
| Hindsight | Long-term memory |
| Groq | LLM access for the meeting agent |
| Uvicorn | ASGI server |
| python-dotenv | Environment variable loading |

## Project Structure

```text
backend/
├── agent/
│   ├── __init__.py
│   └── meeting_agent.py
├── models/
│   └── meeting.py
├── services/
│   ├── hindsight_service.py
│   ├── meeting_service.py
│   └── preparation_service.py
├── main.py
├── .gitignore
└── README.md
```

## API Endpoints

### Health Check

```http
GET /health
```

Returns:

```json
{
  "status": "ok"
}
```

### Save a Meeting

```http
POST /meetings
```

Example request:

```json
{
  "client": "ABC Technologies",
  "meeting_date": "2026-09-28",
  "participants": ["Sarah", "David"],
  "notes": "Client wants a detailed technical proposal."
}
```

The backend stores the meeting and sends its context to Hindsight.

### Get Meetings

```http
GET /meetings
```

Returns meetings stored by the backend during the current application run.

> Hindsight is used for long-term memory; the local `meetings` list is currently an in-memory application store.

### Recall Client Memory

```http
POST /meetings/recall
```

Example:

```json
{
  "client": "ABC Technologies",
  "query": "What are the client's main concerns?"
}
```

The backend queries Hindsight and returns relevant memories for that client.

### Prepare a Meeting

```http
POST /meetings/prepare
```

Example:

```json
{
  "client": "ABC Technologies",
  "query": "Prepare me for the next meeting. Focus on requirements, concerns, pricing, timeline, and previous discussions."
}
```

The backend:

1. Recalls relevant memories from Hindsight.
2. Combines them with the current meeting context.
3. Sends the information to the AI agent.
4. Generates the structured meeting brief.
5. Returns the brief to the frontend.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/jeevann9/meeting-prep-backend.git
cd meeting-prep-backend
```

### 2. Create a virtual environment

Windows:

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Install dependencies

Install the required packages:

```cmd
pip install fastapi uvicorn hindsight-client python-dotenv groq
```

### 4. Configure environment variables

Create a `.env` file in the backend root:

```env
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_API_URL=your_hindsight_api_url
HINDSIGHT_BANK_ID=your_hindsight_bank_id
GROQ_API_KEY=your_groq_api_key
```

**Never commit `.env` or API keys to GitHub.**

The repository's `.gitignore` excludes `.env`, virtual environments, Python cache files, and compiled Python files.

### 5. Start the backend

```cmd
python -m uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI provides interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

## Testing the API

You can test the endpoints using the Swagger UI:

```text
http://127.0.0.1:8000/docs
```

A basic test flow is:

```text
1. POST /meetings
       ↓
2. Meeting stored in Hindsight
       ↓
3. POST /meetings/recall
       ↓
4. Verify client-specific memories
       ↓
5. POST /meetings/prepare
       ↓
6. Verify generated meeting brief
```

## Memory Isolation

Client-specific memory is an important part of the system.

For example:

```text
ABC Technologies
    ├── Cloud migration
    ├── Security concerns
    ├── CloudX
    └── David

XYZ Retail
    ├── Inventory analytics
    ├── Real-time stock visibility
    ├── ₹8 lakh budget
    └── Priya / Arjun
```

The preparation request includes the client name when querying Hindsight so that information from one client is not intentionally mixed with another client's context.

## Example Demo Scenario

### ABC Technologies

Previous meetings establish:

- Cloud migration project
- Security concerns
- CloudX pricing comparison
- David as CTO
- Minimal downtime requirement
- Implementation timeline
- Technical proposal requirement

A later preparation request can combine these memories into one personalized brief.

### XYZ Retail

A separate client can have:

- Inventory analytics platform
- Real-time stock visibility
- ₹8 lakh budget
- December 15 target
- Priya and Arjun as participants

The system should prepare the XYZ brief without introducing ABC-specific information.

## Architecture

```text
                    ┌──────────────────┐
                    │     Frontend     │
                    │  Next.js / UI    │
                    └────────┬─────────┘
                             │
                             │ HTTP / JSON
                             ▼
                    ┌──────────────────┐
                    │     FastAPI      │
                    │      Backend     │
                    └───────┬──────────┘
                            / \
                           /   \
                          ▼     ▼
                ┌────────────┐  ┌──────────────┐
                │  Hindsight │  │  AI Agent    │
                │   Memory   │  │    Groq      │
                └────────────┘  └──────┬───────┘
                                       │
                                       ▼
                              Structured Brief
```

## Current Scope

The current backend MVP focuses on:

- Manual meeting information.
- Long-term memory through Hindsight.
- Client-specific recall.
- AI-powered meeting preparation.

Recording upload and direct Zoom/Google Meet integration are future extensions rather than part of the current backend MVP.

## Future Improvements

Potential next steps include:

- Meeting recording upload and transcription.
- Zoom/Google Meet integration.
- Persistent application database for meeting metadata.
- Authentication and user accounts.
- More advanced memory filtering and ranking.
- Production deployment.
- Automated evaluation and regression tests.

## Repository

GitHub:

https://github.com/jeevann9/meeting-prep-backend

## License

Add a project license before distributing the project publicly.
