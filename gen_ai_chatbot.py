import os
import faiss
import pickle
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
from groq import Groq

# Load FAISS + mapping
INDEX_FILE = "faiss_index.bin"
MAPPING_FILE = "doc_mapping.pkl"

index = faiss.read_index(INDEX_FILE)
with open(MAPPING_FILE, "rb") as f:
    doc_mapping = pickle.load(f)

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Groq client (API key from env)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Flask app
app = Flask(__name__)

def retrieve_context(query, top_k=3):
    query_vec = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vec, top_k)

    context = []
    for idx in indices[0]:
        if idx < len(doc_mapping):
            context.append(doc_mapping[idx][1])
    return "\n\n".join(context)

def ask_groq(context, query):
    prompt = f"""You are an assistant specialized in RBI risk guidelines.
Context:
{context}

Question: {query}
Answer:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")

    context = retrieve_context(query)
    answer = ask_groq(context, query)

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
