from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    text: str

@app.get("/ping")
def ping():
    return {"pong": True}

@app.post("/chat")
def chat(req: ChatRequest):
    return {"answer": f"Эхо: {req.text}"}