import streamlit as st
import langextract_helper as lch 
import textwrap
import os
from openai import OpenAI

st.set_page_config(page_title="YouTube Transcriber", page_icon="🎥")

st.title("YouTube Transcriber")

with st.sidebar:
    st.header("Input Parameters")
    with st.form(key="input_form"):
        youtube_url = st.text_area(
            label="YouTube Video URL",
            max_chars=200,
            placeholder="Enter the full YouTube video URL here"
        )
        query = st.text_area(
            label="Ask me about the video",
            max_chars=200,
            placeholder="Type your question about the video here",
            key="query"
        )
        openai_api_key = st.text_input(
            label="OpenAI API Key",
            type="password",
            max_chars=200,
            placeholder="Paste your OpenAI API Key here"
        )
        st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
        st.markdown("[View the source code](https://github.com/Clffordojuka/YouTube-Transcriber.git)")

        submit_button = st.form_submit_button(label="Submit")

if submit_button:
    # Validate inputs
    if not youtube_url.strip():
        st.warning("Please enter a YouTube video URL.")
        st.stop()
    if not query.strip():
        st.warning("Please enter a question about the video.")
        st.stop()
    if not openai_api_key.strip():
        st.warning("Please add your OpenAI API key to continue.")
        st.stop()

    # Set OpenAI API key for this session
    os.environ["OPENAI_API_KEY"] = openai_api_key
    client = OpenAI()

    with st.spinner("Fetching transcript and generating response..."):
        try:
            # Create FAISS index and vector DB from transcript (embedding done via OpenAI SDK inside helper)
            db = lch.create_db_from_youtube_video_url(youtube_url)

            # Query and get answer
            response, docs = lch.get_response_from_query(db, query)

            st.subheader("Answer:")
            st.text(textwrap.fill(response, width=85))
        except Exception as e:
            st.error(f"An error occurred: {e}")