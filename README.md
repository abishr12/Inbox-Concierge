# Email Concierge

AI-powered email categorization application built with Next.js and FastAPI.

## Project Structure

```
/client - Next.js frontend
/server - FastAPI backend
```

## Setup

### Server Setup

1. Navigate to server directory:
```bash
cd server
```

2. Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

Required environment variables:
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret
- `ANTHROPIC_API_KEY` - Anthropic API key for Claude

3. Install dependencies (already installed via `uv add`):
```bash
# Dependencies are managed via uv and already installed
```

4. Run the server:
```bash
uv run uvicorn main:app --reload
```

Server will run on `http://localhost:8000`

### Client Setup

1. Navigate to client directory:
```bash
cd client
```

2. Install dependencies (already done):
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

Client will run on `http://localhost:3000`

## Features

- **Google OAuth Authentication** - Secure sign-in with Gmail access
- **Email Fetching** - Retrieves last 200 email threads
- **AI Categorization** - Uses Claude LLM to categorize emails into buckets
- **Custom Buckets** - Add/remove custom categories with automatic recategorization
- **Clean UI** - Simple, intuitive interface with Tailwind CSS

## Default Buckets

- Important
- Can Wait
- Auto-archive
- Newsletter

## API Endpoints

### Auth
- `GET /auth/login` - Get OAuth URL
- `GET /auth/callback` - OAuth callback handler
- `GET /auth/status` - Check authentication status
- `POST /auth/logout` - Logout

### Emails
- `GET /emails` - Fetch and categorize emails
- `POST /emails/recategorize` - Recategorize existing emails

### Buckets
- `GET /buckets` - List all buckets
- `POST /buckets` - Add new bucket
- `DELETE /buckets/{name}` - Remove bucket

## Tech Stack

**Client:**
- Next.js 14 (App Router)
- React
- TypeScript
- Tailwind CSS
- Axios

**Server:**
- Python 3.11+
- FastAPI
- PydanticAI
- Anthropic Claude
- Google Gmail API
- uv (package manager)

## Development Notes

- No database required - uses JSON file storage
- Single-user application
- Email data cached after first fetch
- Automatic recategorization when buckets change
