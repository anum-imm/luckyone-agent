from langchain_openai import ChatOpenAI
import tiktoken
from config import OPENAI_API_KEY

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=OPENAI_API_KEY,
    temperature=0
)

# Initialize tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")
