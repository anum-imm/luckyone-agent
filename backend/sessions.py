from sqlalchemy.orm import Session as OrmSession
from fastapi import Depends
from databases.db import SessionLocal, ChatSession, Conversation

def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

def list_sessions(db: OrmSession = Depends(get_db)):
    sessions = db.query(ChatSession).order_by(ChatSession.started_at.desc()).all()
    return [
        {
            "id": s.id,
            "title": s.title,
            "started_at": s.started_at.strftime("%Y-%m-%d %H:%M:%S") if s.started_at else None
        }
        for s in sessions
    ]

def get_session_conversation(session_id: str, db: OrmSession = Depends(get_db)):
    messages = db.query(Conversation).filter_by(session_id=session_id).order_by(Conversation.created_at).all()
    return [
        {
            "user": m.user_message,
            "bot": m.bot_response,
            "type": getattr(m, "response_type", "text"),
            "created_at": m.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for m in messages
    ]
