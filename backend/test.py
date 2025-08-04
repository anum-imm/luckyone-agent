from databases.db import SessionLocal, ChatSession, Conversation

db = SessionLocal()

# Delete conversations first (foreign key constraint)
db.query(Conversation).delete()
db.query(ChatSession).delete()

db.commit()
db.close()

print("✅ All chat sessions and conversations cleared.")
