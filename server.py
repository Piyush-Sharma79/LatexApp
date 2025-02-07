from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/chat"  # Local Ollama API

class RequestData(BaseModel):
    model: str
    prompt: str

@app.post("/generate")
def generate_response(data: RequestData):
    payload = {
        "model": data.model,
        "messages": [{"role": "user", "content": data.prompt}]
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return {"response": response.json()["message"]["content"]}
    return {"error": "Failed to get response from Ollama"}
