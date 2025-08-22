import os
import pickle
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# Paths
DATA_DIR = "data"
INDEX_FILE = "faiss_index.bin"
MAPPING_FILE = "doc_mapping.pkl"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_pdfs(data_dir):
    docs = []
    for file in os.listdir(data_dir):
        if file.endswith(".pdf"):
            path = os.path.join(data_dir, file)
            print(f"📄 Reading {file} ...")
            reader = PdfReader(path)
            text = " ".join([page.extract_text() or "" for page in reader.pages])
            docs.append((file, text))
    return docs

def build_faiss_index(docs):
    texts = [doc[1] for doc in docs]
    embeddings = model.encode(texts, convert_to_numpy=True)

    # ✅ Fix here
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index + mapping
    faiss.write_index(index, INDEX_FILE)
    with open(MAPPING_FILE, "wb") as f:
        pickle.dump([doc[0] for doc in docs], f)

    print(f"\n✅ FAISS index built with {len(docs)} documents.")
    print(f"📦 Saved index to {INDEX_FILE} and mapping to {MAPPING_FILE}")

if __name__ == "__main__":
    docs = load_pdfs(DATA_DIR)
    if not docs:
        print("❌ No PDFs found in 'data/' folder.")
    else:
        build_faiss_index(docs)
