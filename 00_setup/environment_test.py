import sys
import pydantic
import fastapi
import httpx

print("Python:", sys.version)
print("Pydantic:", pydantic.__version__)
print("FastAPI:", fastapi.__version__)
print("HTTPX:", httpx.__version__)

print("\nEnvironment is working.")