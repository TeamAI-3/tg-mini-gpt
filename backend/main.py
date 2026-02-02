import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from openai import OpenAI

# Модель можно переопределить в Render env: OPENAI_MODEL
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")

# OpenAI SDK сам читает ключ из переменной окружения OPENAI_API_KEY :contentReference[oaicite:1]{index=1}
client = OpenAI()

app = FastAPI()

# Разрешаем запросы с фронта (Vercel)
# Можно добавить ещё домены через Render env CORS_ORIGINS (через запятую)
default_origins = [
    "https://tg-mini-gpt.vercel.app",
]
cors_env = os.getenv("CORS_ORIGINS", "").strip()
origins = [o.strip() for o in cors_env.split(",") if o.strip()] or default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    answer: str

@app.get("/ping")
def ping():
    return {"ok": True, "service": "tg-mini-gpt-backend"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is empty")

    instructions = (
        "Ты — помощник внутри Telegram Mini App. "
        "Отвечай по-русски, коротко и по делу. "
        "Если вопрос непонятен — попроси уточнить."
    )

    try:
        # Responses API — рекомендуемый вариант для новых проектов :contentReference[oaicite:2]{index=2}
        resp = await asyncio.to_thread(
            client.responses.create,
            model=OPENAI_MODEL,
            instructions=instructions,
            input=text,
        )
        answer = (resp.output_text or "").strip()
        if not answer:
            answer = "(пустой ответ)"
        return ChatResponse(answer=answer)

    except Exception as e:
        # не светим детали наружу, но понятно что упало
        raise HTTPException(status_code=500, detail=f"OpenAI error: {type(e).name}")