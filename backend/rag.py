import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAG:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.data = []
        self.embeddings = None

    # --------------------------
    # CLEAN TEXT
    # --------------------------
    def clean_text(self, text):
        return " ".join(text.split())

    # --------------------------
    # CHUNKING
    # --------------------------
    def chunk(self, pages, size=500, overlap=100):
        chunks = []

        for item in pages:
            text = self.clean_text(item["text"])
            page = item["page"]

            if not text.strip():
                continue

            start = 0
            while start < len(text):
                chunk = text[start:start+size]

                chunks.append({
                    "text": chunk,
                    "page": page
                })

                start += size - overlap

        return chunks

    # --------------------------
    # ADD DOCUMENT
    # --------------------------
    def add(self, pages):
        chunks = self.chunk(pages)

        if not chunks:
            print("⚠️ No valid text found in PDF")
            return

        texts = [c["text"] for c in chunks]

        embeddings = self.model.encode(texts)

        # Convert to numpy float32
        embeddings = np.array(embeddings).astype("float32")

        # If first time create index
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack((self.embeddings, embeddings))

        # Add to index
        self.index.add(embeddings)

        # Save metadata
        self.data.extend(chunks)

        print(f"✅ Added {len(chunks)} chunks")

    # --------------------------
    # SEARCH
    # --------------------------
    def search(self, query, k=3):
        if self.index is None:
            return []

        q_vec = self.model.encode([query])
        q_vec = np.array(q_vec).astype("float32")

        distances, indices = self.index.search(q_vec, k)

        results = []
        for i in indices[0]:
            if i < len(self.data):
                results.append(self.data[i])

        return results