import os
from youtube_transcript_api import YouTubeTranscriptApi
import numpy as np
import faiss
from langextract.embeddings.openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI API key environment variable
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("Please set OPENAI_API_KEY in your environment or .env file")

embeddings = OpenAIEmbeddings()
client = OpenAI()

def fetch_youtube_transcript(video_url: str) -> str:
    if "v=" in video_url:
        video_id = video_url.split("v=")[-1].split("&")[0]
    else:
        video_id = video_url.split("/")[-1]
    transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = " ".join([entry['text'] for entry in transcript_data])
    return transcript_text

def chunk_text(text: str, chunk_size=1000, overlap=100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def create_faiss_index(text_chunks):
    embed_vectors = embeddings.embed_texts(text_chunks)
    dim = len(embed_vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embed_vectors).astype('float32'))
    return index, embed_vectors

def similarity_search(index, query, text_chunks, k=4):
    query_embed = embeddings.embed_texts([query])
    D, I = index.search(np.array(query_embed).astype('float32'), k)
    return [text_chunks[i] for i in I[0]]

def get_answer_from_docs(docs, question):
    docs_text = " ".join(docs)
    prompt = f"""
You are a helpful assistant answering questions about YouTube videos based on the transcript only.

Question: {question}

Transcript excerpts: {docs_text}

Answer in a detailed and factual manner. If not enough information is available, say "I don't know".
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Example usage:
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
    transcript = fetch_youtube_transcript(video_url)
    chunks = chunk_text(transcript)
    faiss_index, _ = create_faiss_index(chunks)

    query = "Your question about the video here"
    relevant_chunks = similarity_search(faiss_index, query, chunks, k=4)
    answer = get_answer_from_docs(relevant_chunks, query)

    print("Answer:", answer)