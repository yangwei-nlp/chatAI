import os
from dotenv import load_dotenv
from .llm_for_local import MyLLM

load_dotenv()
RUNTIME_BACKEND = os.getenv("RUNTIME_BACKEND")

