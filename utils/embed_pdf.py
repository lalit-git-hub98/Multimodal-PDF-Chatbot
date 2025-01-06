import streamlit as st
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from io import BytesIO
import torch

def embed_pdf(text_chunks, image_chunks):
    try:
        text_embeddings = []
        for chunk in text_chunks:
            embedding = st.session_state.embedding_model.encode(text_chunks, convert_to_tensor=True) 
            linear_layer = torch.nn.Linear(384, 512)
            text_features = linear_layer(embedding)
            st.session_state.clip_index.add(np.array(text_features.detach().numpy()))  # Add embeddings to FAISS index

        image_embeddings = []
        for image in image_chunks:
            inputs = st.session_state.clip_processor(images=image, return_tensors="pt")
            with torch.no_grad():
                image_features = st.session_state.clip_model.get_image_features(**inputs)
            image_embeddings.append(image_features.numpy())  # Convert tensor to numpy array
            st.session_state.clip_index.add(np.array(image_features.numpy()))  # Add embeddings to FAISS index

    except Exception as e:
        pass
        #st.error(f"Error in function --> **embed_pdf**: {e}")