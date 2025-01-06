from langchain.schema import SystemMessage, HumanMessage
from utils.get_relevant_chunks import get_relevant_chunks
import streamlit as st

def answer_question(questions, all_chunks, all_file_page_mappings):
    try:
        answers_list = []
        files_pages_list = []
        for question in questions:
            relevant_chunks, relevant_files_pages = get_relevant_chunks(question, all_chunks, all_file_page_mappings)
            context = " ".join(relevant_chunks)
            unique_files_pages = sorted(set(relevant_files_pages))  # Unique (file, page) pairs

            messages = [
                SystemMessage(content="You are a knowledgeable and resourceful assistant expert in answering questions beased on the given context."),
                HumanMessage(content=f"Based on the context provided, respond to the following question:\n\nContext: {context}\n\nQuestion: {question}")
            ]
            response = st.session_state.llm(messages=messages)
            answers_list.append(response.content.strip())
            files_pages_list.append(unique_files_pages)
        return answers_list, files_pages_list
    except Exception as e:
        pass
        # st.error(e)
        # st.error('Error in function --> **answer_question**')