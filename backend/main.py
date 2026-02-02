# backend/main.py
from __future__ import annotations

import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from openai import OpenAI

from telegram_auth import validate_init_data

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

if not OPENAI_API_KEY:
    # Render покажет это в логах; лучше упасть сразу
    raise RuntimeError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="tg-mini-gpt backend")

# Для MVP можно "*". Потом сузишь до конкретных доменов:
# allow_origins=["https://tg-mini-gpt.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)
    initData: str = ""


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {"ok": True, "service": "tg-mini-gpt backend"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty message")

    # Проверка initData (если есть). Если пустой — пропускаем (удобно для тестов).
    user_hint = ""
    if req.initData.strip():
        if not BOT_TOKEN:
            raise HTTPException(status_code=500, detail="BOT_TOKEN is missing on server")
        try:
            tg = validate_init_data(req.initData, BOT_TOKEN)
            if tg.user and tg.user.get("first_name"):
                user_hint = f"User: {tg.user.get('first_name')}"
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

    try:
        # Модель можешь поменять. Для дешёвого старта ок:
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        system = (
            "Ты помощник в Telegram Mini App. Отвечай по-русски, кратко и по делу."
        )
        if user_hint:
            system += f" ({user_hint})"

        resp = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
        )

        answer = resp.choices[0].message.content or ""
        return ChatResponse(answer=answer.strip() or "(пустой ответ)")
    except Exception as e:
        # Чтобы не сливать внутренности, но было понятно, что упало:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {type(e).__name__}")