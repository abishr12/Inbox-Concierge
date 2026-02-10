# Email Concierge

<div align="center">
  <a href="https://youtu.be/Qh9wOR8b_yY">
    <img src="https://img.youtube.com/vi/Qh9wOR8b_yY/maxresdefault.jpg" alt="Email Concierge Demo" width="600">
  </a>
  <p><em>Click to watch the demo on YouTube</em></p>
</div>

AI-powered email triage that connects to your Gmail, fetches your latest threads, and uses Claude to automatically sort them into actionable buckets (Important, Can Wait, Auto-archive, Newsletter, or any custom categories you define).

## Tech Stack

| Layer    | Technology                                                     |
| -------- | -------------------------------------------------------------- |
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS 4, React Query |
| Backend  | Python 3.11+, FastAPI, PydanticAI, Anthropic Claude            |
| Auth     | Google OAuth 2.0 (Gmail read-only scope)                       |
| Storage  | JSON files on disk (no database required)                      |
| Packages | npm (client), uv (server)                                      |

## Prerequisites

- **Node.js** >= 18 and **npm**
- **Python** >= 3.11
- [**uv**](https://docs.astral.sh/uv/) (Python package manager) -- install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- A **Google Cloud** project with the Gmail API enabled and OAuth 2.0 credentials (Web application type)
- An **Anthropic API key** for Claude

## Project Structure

```
tenex-email-concierge/
├── client/                     # Next.js frontend
│   ├── app/
│   │   ├── api/auth/callback/  # OAuth callback route handler
│   │   ├── emails/             # Email list page, components, hooks
│   │   ├── hooks/              # useLogin hook
│   │   ├── layout.tsx
│   │   ├── page.tsx            # Landing / login page
│   │   └── providers.tsx       # React Query provider
│   ├── components/             # LoginButton, LoginScreen
│   ├── types/                  # Shared TypeScript types
│   ├── utils/                  # Color helpers for bucket badges
│   └── package.json
├── server/                     # FastAPI backend
│   ├── __tests__/              # pytest test suite
│   ├── data/                   # JSON storage (gitignored at runtime)
│   ├── models/schemas.py       # Pydantic models
│   ├── routes/                 # auth, emails, buckets routers
│   ├── services/
│   │   ├── agents/             # PydanticAI categorization agent
│   │   ├── prompts/            # Jinja2 prompt templates
│   │   ├── categorization_service.py
│   │   ├── gmail_service.py
│   │   └── storage_service.py
│   ├── config.py               # Env var loader
│   ├── main.py                 # FastAPI entrypoint
│   ├── pyproject.toml
│   └── .env.example
└── README.md
```

## Getting Started

### 1. Clone the repo

```bash
git clone <repo-url>
cd tenex-email-concierge
```

### 2. Configure environment variables

```bash
cp server/.env.example server/.env
```

Edit `server/.env` and fill in your credentials:

```env
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
REDIRECT_URI=http://localhost:3000/api/auth/callback
```

> **Google OAuth setup:** In the Google Cloud Console, create an OAuth 2.0 Client ID of type *Web application*. Add `http://localhost:3000/api/auth/callback` as an authorized redirect URI. The app only requests the `gmail.readonly` scope.

### 3. Start the server

```bash
cd server
uv sync            # install Python dependencies
uv run uvicorn main:app --reload
```

The API will be available at **http://localhost:8000**.

### 4. Start the client

Open a new terminal:

```bash
cd client
npm install        # install Node dependencies
npm run dev
```

The app will be available at **http://localhost:3000**.

### 5. Use the app

1. Open **http://localhost:3000** in your browser.
2. Click **Sign in with Google** and authorize Gmail access.
3. After redirect, the app fetches your latest email threads and streams AI-categorized results in real time.
4. Add or remove custom buckets -- emails are automatically recategorized.

## API Endpoints

### Auth

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| GET    | `/auth/login`    | Returns Google OAuth URL |
| GET    | `/auth/callback` | Handles OAuth callback   |
| GET    | `/auth/status`   | Check auth status        |
| POST   | `/auth/logout`   | Clear session            |

### Emails

| Method | Endpoint                      | Description                        |
| ------ | ----------------------------- | ---------------------------------- |
| GET    | `/emails`                     | Return cached emails (if any)      |
| GET    | `/emails/stream`              | SSE stream of categorized emails   |
| POST   | `/emails/recategorize-stream` | SSE stream of recategorized emails |

### Buckets

| Method | Endpoint               | Description    |
| ------ | ---------------------- | -------------- |
| GET    | `/buckets`             | List buckets   |
| POST   | `/buckets`             | Create bucket  |
| POST   | `/buckets/{bucket_id}` | Remove bucket  |

## Default Buckets

| Bucket       | Description                              |
| ------------ | ---------------------------------------- |
| Important    | Urgent or action-required emails         |
| Can Wait     | Informational, non-urgent content        |
| Auto-archive | Order confirmations, promos, job alerts  |
| Newsletter   | Digests, Substacks, weekly round-ups     |

You can add your own custom buckets through the UI; the AI will recategorize all emails automatically.

## Running Tests

The server has a pytest test suite that validates the categorization service against sample email data.

> **Note:** Tests call the Anthropic API, so a valid `ANTHROPIC_API_KEY` must be set in `server/.env`.

### Full test suite

```bash
cd server
uv run pytest __tests__/test_categorization.py -v
```

### With detailed output

```bash
cd server
uv run pytest __tests__/test_categorization.py -v -s
```

### Run a single test

```bash
cd server
uv run pytest __tests__/test_categorization.py::test_categorize_emails_basic -v
```

### Standalone test runner (no pytest)

```bash
cd server
uv run python __tests__/run_categorization_test.py
```

This prints a nicely formatted summary showing categorization results and bucket distribution.

## How It Works

1. **OAuth flow** -- The client redirects to Google's consent screen. After approval, the authorization code is forwarded from the Next.js callback route to the FastAPI backend, which exchanges it for tokens and stores them in `server/data/session.json`.

2. **Email fetching** -- The server uses the Gmail API to pull the latest email threads (subject, snippet, sender, labels).

3. **AI categorization** -- Emails are batched and sent to Claude via PydanticAI with a Jinja2 prompt template. The model returns structured bucket assignments. Results stream to the client via Server-Sent Events (SSE).

4. **Storage** -- Categorized emails and bucket definitions are persisted as JSON files in `server/data/`. No external database is needed.

## Development Notes

- **Single-user app** -- session and email data are stored in flat files, not scoped per user.
- **No database** -- all state lives in `server/data/` as JSON.
- **Emails are cached** -- after the first fetch, subsequent loads serve from `emails.json` until you recategorize.
- **Model deprecation** -- the categorization agent currently uses `claude-3-5-haiku-latest`. Check `server/services/agents/categorization_agent.py` if you need to update the model.
- **CORS** -- the server allows requests from `http://localhost:3000` only.
