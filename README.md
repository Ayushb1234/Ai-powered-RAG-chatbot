# Ai-powered-RAG-chatbot

Deplyment Link - https://ai-powered-rag-chatbot-doif8yx5anjemfudrydmk9.streamlit.app/

✨ Features
Multi-doc ingestion: PDF (PyMuPDF) & DOCX (python-docx)

Chunking & semantic search with FAISS (CPU)

High-quality embeddings via sentence-transformers

Local/Offline LLM support using transformers + torch

Source-aware responses: shows which chunks were used

Clean Streamlit UI with drag-and-drop upload

Simple codebase: clear modules for parsing, indexing, retrieval, and generation

🧱 Tech Stack
Frontend: Streamlit

RAG Core: FAISS (vector index), sentence-transformers (embeddings)

LLM: Hugging Face transformers + torch (CPU by default)

Parsers: PyMuPDF (PDF), python-docx (DOCX)

Packaging: requirements.txt for quick setup


🗂️ Project Structure
bash
Copy
Edit
.
├── app.py                 # Streamlit UI (entrypoint)
├── chatbot.py             # Chat loop, formatting, citations
├── file_parser.py         # PDF/DOCX loaders + clean text extraction
├── rag_pipeline.py        # Chunking, embeddings, FAISS index, retrieval
├── requirements.txt
├── README.md
└── LICENSE

⚙️ Quickstart (Local)
Python 3.9+ recommended

bash
Copy
Edit
# 1) Clone
git clone <your-repo-url>
cd Ai-powered-RAG-chatbot

# 2) Create & activate venv (optional but recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Run the app
streamlit run app.py
Open the local URL Streamlit prints (usually http://localhost:8501) and start chatting.

🧠 How It Works (RAG Flow)
mermaid
Copy
Edit
flowchart LR
  A[Upload PDFs/DOCX] --> B[Parse & Clean Text<br/>(PyMuPDF / python-docx)]
  B --> C[Chunking (overlap-aware)]
  C --> D[Embeddings (sentence-transformers)]
  D --> E[FAISS Index (CPU)]
  F[User Query] --> G[Query Embedding]
  G --> H[Top-k Similarity Search from FAISS]
  H --> I[Context Builder (citations)]
  I --> J[LLM Generation (transformers/torch)]
  J --> K[Answer + Sources in UI]
Key ideas

Grounded answers: The LLM only sees retrieved context from your docs.

Portable: No cloud dependencies by default; runs on CPU.

Swappable: You can change the embedding model or the LLM in one place.

🔧 Configuration
You can tweak these in rag_pipeline.py:

Embedding model (e.g., all-MiniLM-L6-v2, multi-qa-mpnet-base-dot-v1)

Chunk size & overlap (balance recall vs. speed)

Top-k retrieval (number of chunks to pass to the LLM)

Index persistence (save FAISS index to disk for reuse)

Example (pseudo):

python
Copy
Edit
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
TOP_K = 5
INDEX_DIR = "index_store/"
🖱️ Usage
Launch the app.

Upload one or more PDF/DOCX files.

Ask a question in the chat box.

The answer includes citations (document names + chunk refs).

Example prompts

“Summarize Chapter 2 in 5 bullet points.”

“Compare approach A vs B mentioned across these docs.”

“What are the key risks and mitigations noted?”

📦 Requirements
From requirements.txt:

nginx
Copy
Edit
streamlit
transformers
torch
faiss-cpu
sentence-transformers
python-docx
PyMuPDF
packaging
🛣️ Roadmap
 Add index persistence + background re-builds

 Add OpenAI / local LLM switch via sidebar

 Optional chat history + session persistence

 Reranking (e.g., Cross-Encoder) for better retrieval quality

 Eval suite: context precision/recall & latency metrics

🤝 Contributing
PRs are welcome!

Fork the repo

Create a feature branch: feat/<short-name>

Add tests or a short demo clip if UI-related

Open a PR with a clear description

📝 License
This project is released under the MIT License. See LICENSE.

🙏 Acknowledgements
FAISS for fast similarity search

Sentence-Transformers for robust embeddings

Streamlit for painless prototyping

Hugging Face transformers for model loading

