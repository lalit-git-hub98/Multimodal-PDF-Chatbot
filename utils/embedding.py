from transformers import CLIPModel, CLIPProcessor
from sentence_transformers import SentenceTransformer
import faiss
import streamlit as st

def load_clip_embeddings():
    try:
        if 'clip_model' not in st.session_state:
            st.session_state.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            st.session_state.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        if 'clip_dimension' not in st.session_state:
            st.session_state.clip_dimension = 512

        if 'clip_index' not in st.session_state:
            st.session_state.clip_index = faiss.IndexFlatL2(st.session_state.clip_dimension)

        if 'embedding_model' not in st.session_state:
            st.session_state.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        st.error(f"Error in function --> **load_clip_embeddings**: {e}")
