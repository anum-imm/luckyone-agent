import os

def get_chinook_db():
    from langchain_community.utilities import SQLDatabase
    db_path = os.path.join(os.path.dirname(__file__), "Chinook.db")
    db_path = os.path.abspath(db_path)
    return SQLDatabase.from_uri(f"sqlite:///{db_path}")
