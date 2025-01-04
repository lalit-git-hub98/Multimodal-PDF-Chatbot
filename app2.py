import streamlit as st
import os
import io
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize embedding model
embedding_model = OpenAIEmbeddings()

# FAISS store variables
text_store = None
table_store = None
image_store = None

# Function to initialize FAISS store
def initialize_faiss_store():
    """Initialize FAISS store with placeholder data."""
    placeholder_embedding = embedding_model.embed_query("placeholder")
    return FAISS.from_embeddings([(placeholder_embedding, "placeholder")])

# Function to extract content from PDFs using PdfReader (PyPDF2)
def extract_pdf_content(pdf_file):
    """Extract text, tables, and images from the uploaded PDF."""
    pdf_reader = PdfReader(pdf_file)
    text_data = []
    table_data = []  # Placeholder for table extraction logic
    image_data = []  # Placeholder for image extraction logic
    
    # Extract text content from each page
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text_data.append(page.extract_text())

    return text_data, table_data, image_data

# Function to index content into FAISS stores
def index_content(content, content_type="text"):
    """Index content into the appropriate FAISS store."""
    global text_store, table_store, image_store
    
    # Lazy initialization of stores if None
    if text_store is None:
        text_store = initialize_faiss_store()
    if table_store is None:
        table_store = initialize_faiss_store()
    if image_store is None:
        image_store = initialize_faiss_store()

    if content_type == "text":
        text_store.add_texts(content)
    elif content_type == "table":
        table_store.add_texts(content)  # Add table content as text
    elif content_type == "image":
        image_embeddings = [embedding_model.embed_query(f"Image content: {img}") for img in content]
        image_store.add_embeddings(image_embeddings, content)

# Function to retrieve relevant content
def retrieve_content(query, store, top_k=3):
    """Retrieve the top-k most relevant documents from the FAISS store."""
    if store is None:
        return []  # No content to retrieve
    retriever = store.as_retriever()
    retriever.search_kwargs = {"k": top_k}
    return retriever.get_relevant_documents(query)

# Function to generate the answer using a language model
def generate_answer(query, text_results, table_results, image_results):
    """Generate the response by combining relevant text, table, and image results."""
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
    combined_context = "\n\n".join([doc.page_content for doc in text_results] +
                                   [doc.page_content for doc in table_results] +
                                   [doc.page_content for doc in image_results])
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=None)
    answer = qa_chain.run({"query": query, "context": combined_context})
    return answer

# Streamlit UI
st.title("Multimodal Document Search and Chatbot")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
if uploaded_file is not None:
    # Convert the uploaded file into a file-like object
    pdf_file = io.BytesIO(uploaded_file.read())
    
    st.write(f"Processing {uploaded_file.name}...")
    text_data, table_data, image_data = extract_pdf_content(pdf_file)

    # Index content
    st.write("Indexing content into FAISS store...")
    if text_data:
        index_content(text_data, "text")
    if table_data:
        index_content(table_data, "table")
    if image_data:
        index_content(image_data, "image")
    
    st.write("Content indexed successfully!")

# Query input
query = st.text_input("Ask a question based on the document:")
if query:
    st.write("Retrieving relevant content...")
    text_results = retrieve_content(query, text_store)
    table_results = retrieve_content(query, table_store)
    image_results = retrieve_content(query, image_store)

    st.write("Generating response...")
    answer = generate_answer(query, text_results, table_results, image_results)

    st.write("### Answer:")
    st.write(answer)
