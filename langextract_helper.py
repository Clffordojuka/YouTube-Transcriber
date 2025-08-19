import os
import openai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import faiss
import numpy as np

load_dotenv()

def set_api_key(api_key: str):
    """Set API key dynamically from Streamlit input"""
    openai.api_key = api_key

def get_transcript(video_url: str) -> str:
    """Fetch YouTube transcript as plain text."""
    if "v=" in video_url:
        video_id = video_url.split("v=")[-1]
    else:
        video_id = video_url.split("/")[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t["text"] for t in transcript])

def chunk_text(text: str, chunk_size=1000, overlap=100):
    """Split transcript into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def embed_texts(texts: list[str]) -> np.ndarray:
    """Get OpenAI embeddings for list of texts."""
    resp = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return np.array([d["embedding"] for d in resp["data"]])

def create_db_from_youtube(video_url: str):
    """Create FAISS index from YouTube transcript."""
    transcript = get_transcript(video_url)
    chunks = chunk_text(transcript)

    embeddings = embed_texts(chunks)

    # Build FAISS index
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    return {"index": index, "chunks": chunks}

def search_db(db, query: str, k=4):
    """Search FAISS index for relevant transcript chunks."""
    q_emb = embed_texts([query])
    distances, indices = db["index"].search(np.array(q_emb).astype("float32"), k)
    return [db["chunks"][i] for i in indices[0]]

def get_response_from_query(db, query: str, k=4):
    """Ask LLM a question using retrieved transcript chunks."""
    docs = search_db(db, query, k)
    docs_content = " ".join(docs)

    prompt = f"""
    You are a helpful assistant that answers questions about YouTube videos 
    based only on the transcript provided.

    Question: {query}

    Transcript: {docs_content}

    Answer in a detailed and factual way. 
    If the transcript does not contain enough information, reply "I don't know".
    """

    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message["content"], docs
