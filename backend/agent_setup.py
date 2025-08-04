from tools.sqltool import create_agent
from databases.chinook import get_chinook_db
from llm import llm

sql_db = get_chinook_db()
agent = create_agent(sql_db, llm)
