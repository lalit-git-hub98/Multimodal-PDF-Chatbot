import os
from dotenv import load_dotenv
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from transformers import CLIPProcessor, CLIPModel
import faiss

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

def load_clip_model():
    """
    Loads the CLIP model for text-to-image and image-to-text embeddings.
    Stores the model in the Streamlit session state.
    """
    try:
        # Load CLIP for embeddings
        if 'clip_model' not in st.session_state:
            st.session_state.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        
        if 'clip_processor' not in st.session_state:
            st.session_state.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            st.success("CLIP model loaded successfully for embeddings.")
        if 'clip_dimension' not in st.session_state:
            st.session_state.clip_dimension = 512

        if 'clip_index' not in st.session_state:
            st.session_state.clip_index = faiss.IndexFlatL2(st.session_state.clip_dimension)
            
        if 'llm' not in st.session_state:
            st.session_state.llm = ChatOpenAI(model="gpt-3.5-turbo")
    except Exception as e:
        st.error(f"Error in function --> **load_clip_model**: {e}")
