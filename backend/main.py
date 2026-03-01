from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os

from utils import load_pdf_with_pages
from rag import RAG
from ai import generate_answer

app = FastAPI()
rag = RAG()

os.makedirs("data", exist_ok=True)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Tutor Running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Upload PDF
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"data/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = load_pdf_with_pages(path)
    rag.add(pages)

    return {"message": "PDF processed"}

# Ask question
@app.post("/ask")
async def ask(question: str = Form(...), lang: str = Form("english")):
    docs = rag.search(question)

    if not docs:
        return {"answer": "Please upload PDF first 📄", "source": []}

    context = ""
    pages = set()

    for d in docs:
        context += d["text"] + "\n"
        pages.add(d["page"])

    answer = generate_answer(context, question, lang)

    return {
        "answer": answer,
        "source": list(pages)
    }

# 🔥 IMPORTANT FOR RENDER
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
