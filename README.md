# ThumbLab

Thumbnail generation service powered by AI. Create YouTube, LinkedIn, and cinematic thumbnails from a reference headshot and text prompt.

## Stack

- **Backend** -- FastAPI, SQLModel (SQLite), OpenAI, ImageKit
- **Frontend** -- React, TypeScript, Vite, TanStack React Query, React Router

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 20+
- OpenAI API key
- ImageKit account (private key, public key, URL endpoint)

### Backend

```bash
cd backend
cp .env.example .env
# fill in your API keys in .env

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### All-in-one

```bash
./start.sh
```

Open http://localhost:5173 in your browser.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/jobs` | List all jobs |
| POST | `/api/jobs` | Create a new thumbnail job |
| GET | `/api/jobs/{id}` | Get job details with thumbnails |
| GET | `/api/jobs/{id}/thumbnails` | List thumbnails for a job |

## Project Structure

```
ThumbLab/
  backend/
    main.py              -- FastAPI application and routes
    models.py            -- SQLModel ORM models (Job, Thumbnail)
    database.py          -- SQLite engine and session
    config.py            -- Environment variable loading
    services/
      generator.py       -- Job processing orchestration
      openai_service.py  -- OpenAI image generation
      imagekit_service.py-- ImageKit upload and transformations
  frontend/
    src/
      api/               -- API client and endpoint functions
      components/        -- Reusable UI components
      pages/             -- Route-level page components
      types/             -- TypeScript interfaces
```

## How It Works

1. A user submits a prompt, headshot URL, and desired number of thumbnails.
2. The backend creates a Job and queues background processing.
3. For each thumbnail, the generator calls OpenAI with the headshot and a style-specific prompt.
4. Generated images are uploaded to ImageKit and their URLs are stored on the Thumbnail record.
5. The frontend polls for status updates and displays results.
