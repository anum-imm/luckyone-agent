from fastapi import Request
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
import traceback
from databases.db import SessionLocal, ChatSession, Conversation
from agent_setup import agent
from utils import is_base64_image
from llm import tokenizer

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str]

async def ask_question(req: QueryRequest):
    if not req.query.strip():
        return {"status": "failed", "error": "Query cannot be empty."}

    if not req.session_id:
        req.session_id = str(uuid4())

    db_session = SessionLocal()

    try:
        chat_session = db_session.query(ChatSession).filter_by(id=req.session_id).first()
        if not chat_session:
            chat_session = ChatSession(id=req.session_id, title="untitled", total_tokens=0)
            db_session.add(chat_session)
            db_session.commit()

        if chat_session.title == "untitled":
            chat_session.title = req.query[:50]
            db_session.commit()

        history = db_session.query(Conversation).filter_by(
            session_id=req.session_id
        ).order_by(Conversation.created_at).all()

        past_messages = []
        for h in history:
            past_messages.append({"role": "user", "content": h.user_message})
            if getattr(h, "response_type", None) == "image":
                past_messages.append({"role": "assistant", "content": "[Chart image omitted for context]"})
            else:
                past_messages.append({"role": "assistant", "content": h.bot_response})

        past_messages.append({"role": "user", "content": req.query})

        result = None
        for step in agent.stream(
            {"messages": [{"role": "user", "content": req.query}]},
            {"configurable": {"thread_id": str(req.session_id)}},
            stream_mode="values"
        ):
            if step.get("messages"):
                final_msg = step["messages"][-1]
                result = getattr(final_msg, "content", str(final_msg))

        if not result:
            result = "No response."

        if is_base64_image(result):
            response_type = "image"
            final_result = f"data:image/png;base64,{result}"
        else:
            response_type = "text"
            final_result = result

        try:
            query_tokens = len(tokenizer.encode(req.query))
            response_tokens = len(tokenizer.encode(result)) if result else 0
            total_tokens = query_tokens + response_tokens
        except Exception:
            query_tokens, response_tokens, total_tokens = 0, 0, 0

        convo = Conversation(
            session_id=req.session_id,
            user_message=req.query,
            bot_response=final_result,
            response_type=response_type,
            tokens_used=total_tokens
        )
        db_session.add(convo)
        chat_session.total_tokens += total_tokens
        db_session.commit()

        return {
            "status": "success",
            "answer": final_result,
            "session_id": req.session_id,
            "type": response_type
        }

    except Exception as e:
        traceback.print_exc()
        return {"status": "failed", "error": str(e)}

    finally:
        db_session.close()
