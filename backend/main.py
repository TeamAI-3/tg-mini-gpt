from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    text: str

@app.get("/ping")
def ping():
    return {"pong": True}

@app.post("/chat")
def chat(req: ChatRequest):
    # ЭХО-ответ, чтобы проверить всю цепочку
    return {"answer": f"Эхо: {req.text}"}