import os, json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from telegram_auth import verify_telegram_init_data

load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

app = FastAPI()
client = OpenAI(api_key=OPENAI_API_KEY)

MEM = {}

class ChatIn(BaseModel):
    initData: str
    text: str

@app.post("/chat")
def chat(payload: ChatIn):
    try:
        data = verify_telegram_init_data(payload.initData, BOT_TOKEN)
        user = json.loads(data.get("user", "{}"))
        user_id = int(user["id"])

        history = MEM.get(user_id, [])
        if not history:
            history.append({
                "role": "system",
                "content": [{"type":"text","text":"Ты полезный ассистент. Отвечай кратко и по делу."}]
            })

        history.append({"role":"user","content":[{"type":"text","text":payload.text}]})

        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=history
        )

        answer = getattr(resp, "output_text", "")
        history.append({"role":"assistant","content":[{"type":"text","text":answer}]})
        MEM[user_id] = history[-30:]

        return {"ok": True, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))