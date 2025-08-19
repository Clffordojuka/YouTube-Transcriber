🎥 YouTube Transcriber (LangExtract + Streamlit)

This project is an interactive YouTube Q&A Transcriber built with Streamlit and powered by LangExtract for transcript extraction and semantic search.
Users can paste a YouTube link, ask natural language questions about the video, and instantly receive AI-generated answers.

🚀 Features

🔗 Input any YouTube video URL.

🤖 Ask questions about the video content.

🧠 Uses LangExtract for transcript retrieval + embeddings.

🎨 Simple, clean Streamlit interface.

🐳 Containerized with Docker for easy deployment.

📦 Installation

Clone the repo:

git clone https://github.com/your-username/youtube-assistant.git
cd youtube-assistant


Install dependencies:

pip install -r requirements.txt


Run locally:

streamlit run main.py

🔑 Environment Setup

Create a .env file (or pass via Streamlit sidebar):

OPENAI_API_KEY=your_api_key_here


Get your API key: OpenAI API Keys

🐳 Run with Docker

Build the image:

docker build -t youtube-transcriber .


Run the container:

docker run -p 8501:8501 youtube-transcriber


Access the app at: http://localhost:8501

📝 Example

Paste a YouTube URL in the sidebar.

Enter your OpenAI API key.

Ask: “Summarize the main ideas in this video”.

Get instant AI answers based on transcript + embeddings.

🛠 Tech Stack

Python 3.9+

Streamlit – UI

LangExtract – transcript + retrieval

OpenAI – LLM responses

Docker – deployment

📌 Roadmap

 Support multiple videos at once.

 Add caching for transcripts.

 Option to export Q&A results as PDF.

📜 License

MIT License – free to use and modify.