# main.py
import streamlit as st
import langextract_helper as lch
import textwrap

st.title("🎥 YouTube Transcriber (LangExtract Edition)")

with st.sidebar:
    with st.form(key='my_form'):
        youtube_url = st.text_area(
            label="What is the YouTube video URL?",
            max_chars=200
        )
        query = st.text_area(
            label="Ask me about the video?",
            max_chars=200,
            key="query"
        )
        openai_api_key = st.text_input(
            label="OpenAI API Key",
            key="openai_api_key",
            max_chars=200,
            type="password"
        )
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        submit_button = st.form_submit_button(label='Submit')

if submit_button and query and youtube_url:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    else:
        # Set API key dynamically
        lch.set_api_key(openai_api_key)

        try:
            # Add debug information
            st.info("Fetching transcript...")
            transcript = lch.get_transcript(youtube_url)
            
            if not transcript:
                st.error("Could not fetch transcript. Please check if the video has captions available.")
                st.stop()
                
            st.info("Creating database...")
            db = lch.create_db_from_youtube(youtube_url)
            
            st.info("Getting response...")
            response, docs = lch.get_response_from_query(db, query)

            st.subheader("📌 Answer:")
            st.text(textwrap.fill(response, width=85))

            with st.expander("🔎 Transcript snippets used"):
                for d in docs:
                    st.write(d)

        except Exception as e:
            st.error(f"Error: {e}")
            # Add more detailed error information
            import traceback
            st.error(f"Detailed error: {traceback.format_exc()}")