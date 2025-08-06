from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")
GOOGLE_SCOPES = os.getenv("GOOGLE_SCOPES")
if GOOGLE_SCOPES:
    GOOGLE_SCOPES = GOOGLE_SCOPES.split()
else:
    GOOGLE_SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/tasks"
    ]

def get_google_creds():
    creds = Credentials(
        None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=GOOGLE_SCOPES,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return creds

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: str = Path(..., description="The ID of the task to retrieve")):
    try:
        creds = get_google_creds()
        service = build('tasks', 'v1', credentials=creds)
        task = service.tasks().get(tasklist='@default', task=task_id).execute()
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
        return {"task": task}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/calendar/events")
def get_calendar_events():
    try:
        creds = get_google_creds()
        service = build('calendar', 'v3', credentials=creds)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
def get_tasks():
    try:
        creds = get_google_creds()
        service = build('tasks', 'v1', credentials=creds)
        tasks_result = service.tasks().list(tasklist='@default').execute()
        tasks = tasks_result.get('items', [])
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
