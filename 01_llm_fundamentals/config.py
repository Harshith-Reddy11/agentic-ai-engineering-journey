from dotenv import load_dotenv
import os

load_dotenv()
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
TIMEOUT = float(os.getenv("LLM_TIMEOUT", "30"))

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash"
)

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )