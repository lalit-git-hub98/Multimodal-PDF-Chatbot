import os
from dotenv import load_dotenv
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()
# Set OpenAI API key as environment variable
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

def load_clip_model():
    """
    Loads the CLIP model for text-to-image and image-to-text embeddings.
    Stores the model in the Streamlit session state.
    """
    try:
        # Load CLIP for embeddings
        if 'clip_model' not in st.session_state:
            st.session_state.clip_model = OpenAIEmbeddings(model="clip-vit-base-patch32")
            st.success("CLIP model loaded successfully for embeddings.")
    except Exception as e:
        st.error(f"Error in function --> **load_clip_model**: {e}")
