from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from databases import db
from sessions import list_sessions, get_session_conversation
from chat import ask_question

print("USING DB FILE:", db.db_path)

# Initialize DB
db.init_db()

# FastAPI app
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return "✅ FastAPI SQL + Analytics Agent is running"

# Attach endpoints
app.post("/api/ask")(ask_question)
app.get("/api/sessions")(list_sessions)
app.get("/api/sessions/{session_id}")(get_session_conversation)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
