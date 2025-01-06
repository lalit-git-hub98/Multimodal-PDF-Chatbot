import streamlit as st
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from io import BytesIO
import torch

def extract_pdf_data(file, file_name):
    text_chunks = []
    image_chunks = []
    file_page_mapping_text = []  # Metadata for text chunks
    file_page_mapping_image = []  # Metadata for image chunks
    
    try:
        # Process Text and Images using PyMuPDF (fitz)
        pdf_document = fitz.open(file)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Extract Text
            text = page.get_text("text")
            if text:
                # Split text into chunks (e.g., 500 characters per chunk)
                chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
                text_chunks.extend(chunks)
                file_page_mapping_text.extend([(file_name, page_num + 1)] * len(chunks))  # Store references for text
                
            # Extract Images
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_data = base_image["image"]

                # Convert image bytes to a PIL Image for further processing
                image = Image.open(BytesIO(image_data))

                # Store image and its metadata
                image_chunks.append(image)  # Store the raw image for embedding purposes
                file_page_mapping_image.append((file_name, page_num + 1, img_index + 1))  # Store references for images

        return text_chunks, image_chunks, file_page_mapping_text, file_page_mapping_image
    except Exception as e:
        st.write(f"Error in extract_pdf_data: {e}")