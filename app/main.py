from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.chatbot import generate_answer


app = FastAPI()


class ChatRequest(BaseModel):
    message: str


# Serve files from the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    answer = generate_answer(request.message)

    return {
        "answer": answer
    }