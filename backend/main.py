import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# (опционально) чтобы локально читать .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tg-mini-gpt")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "*").strip()

def parse_origins(raw: str):
    # Можно поставить "*" на время разработки
    if not raw or raw == "*":
        return ["*"], False
    origins = [o.strip() for o in raw.split(",") if o.strip()]
    return origins, True

origins, allow_credentials = parse_origins(CORS_ORIGINS_RAW)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

class ChatIn(BaseModel):
    text: str

@app.get("/ping")
def ping():
    return {"pong": True}

@app.post("/chat")
def chat(payload: ChatIn):
    text = (payload.text or "").strip()
    if not text:
        raise HTTPException(status_code=422, detail="text is empty")

    if client is None:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is missing")

    try:
        # Responses API
        resp = client.responses.create(
            model=OPENAI_MODEL,
            input=text,
        )
        answer = (getattr(resp, "output_text", "") or "").strip()
        return {"answer": answer or "(пустой ответ)"}

    except Exception as e:
        log.exception("OpenAI call failed")
        # ВАЖНО: __name__, а не .name
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI error: {type(e).__name__}: {str(e)}"
        )
