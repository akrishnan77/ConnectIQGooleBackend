# ConnectIQ Google Backend

This is a standalone FastAPI backend for Google API integration (Tasks, Calendar, etc.).

## Features
- FastAPI server
- Google OAuth2 integration
- Endpoints for Google Tasks and Calendar

## Setup
1. Copy `.env.template` to `.env` and fill in your Google credentials.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the server:
   ```sh
   uvicorn main:app --reload
   ```

## Endpoints
- `/tasks` - List Google Tasks
- `/tasks/{task_id}` - Get a single Google Task
- `/calendar/events` - List Google Calendar events

## Notes
- Keep backend and frontend in separate projects for easier maintenance.
- Update `.env` with your Google OAuth2 credentials and scopes.
