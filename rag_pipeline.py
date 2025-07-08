from sentence_transformers import SentenceTransformer
import faiss
from chatbot import generate_response  # ✅ Corrected import

# Load the embedding model (used for FAISS)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Chunk the uploaded text (optional: improve chunking with NLP later)
def load_knowledge_base(raw_text):
    chunks = [raw_text[i:i+300] for i in range(0, len(raw_text), 300)]
    return chunks

# Build FAISS index from text chunks
def build_faiss_index(text_chunks):
    import numpy as np
    embeddings = embedding_model.encode(text_chunks, convert_to_numpy=True)
    embeddings = np.array(embeddings)
    assert embeddings.ndim == 2, f"Expected 2D embeddings, got shape {embeddings.shape}"
    
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, text_chunks

# Search top-k chunks for a query
def search_index(index, query, texts, top_k=1):
    query_vec = embedding_model.encode([query])
    scores, results = index.search(query_vec, top_k)
    return [texts[i] for i in results[0]]

# Full RAG pipeline
from transformers import AutoTokenizer

def rag_response(user_query, index, text_chunks, selected_model):
    context = " ".join(search_index(index, user_query, text_chunks))
    prompt = f"Use the following context to answer the question:\n{context}\n\nQ: {user_query}\nA:"

    tokenizer = AutoTokenizer.from_pretrained(selected_model)
    tokens = tokenizer.encode(prompt, truncation=True, max_length=512)
    prompt = tokenizer.decode(tokens, skip_special_tokens=True)

    return generate_response(prompt, selected_model)
