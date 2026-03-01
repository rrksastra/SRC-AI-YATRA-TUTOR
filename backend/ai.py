import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found. Set it in .env file")

genai.configure(api_key=api_key)

# Use stable model name
model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_answer(context, question, lang="english"):
    prompt = f"""
You are a friendly AI teacher.

Context:
{context}

Question:
{question}

Instructions:
- Answer in {lang}
- Explain simply for students
- If Tamil, use simple Tamil

Answer:
"""

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text
        else:
            return "⚠️ No response generated"

    except Exception as e:
        return f"❌ Error: {str(e)}"