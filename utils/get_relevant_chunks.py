import numpy as np
import streamlit as st
import torch

def get_relevant_chunks(question, all_chunks, all_file_page_mappings, top_k=5):
    try:
        embedding = st.session_state.embedding_model.encode(question, convert_to_tensor=True) 
        linear_layer = torch.nn.Linear(384, 512)
        question_embedding = linear_layer(embedding) 
        question_embedding_np = question_embedding.detach().numpy()
        
        # Perform search on the CLIP index
        _, indices = st.session_state.clip_index.search(np.array([question_embedding_np]), top_k)
        
        # Get relevant chunks and file-page mappings
        relevant_chunks = [all_chunks[idx] for idx in indices[0]]
        relevant_files_pages = [all_file_page_mappings[idx] for idx in indices[0]]
        return relevant_chunks, relevant_files_pages
    except Exception as e:
        # st.error(e)
        # st.error('Error in function --> **get_relevant_chunks**')
        pass
