import streamlit as st
import base64
import os
from streamlit_pdf_viewer import pdf_viewer

from utils.extract_pdf import *
from utils.embed_pdf import *
from utils.load_model import *
from utils.embedding import *
from utils.answer_question import *

try:
    ############################################### Webpage Configuration ##############################################
    st.set_page_config(page_title="RAGent", page_icon=":page_with_curl:", layout="wide")

    load_clip_model()
    load_clip_embeddings()

    main_col1, main_col2 = st.columns([0.5, 0.5])

    ############################################################## Wrapper for Left Section ###########################################################################################
    with main_col1:
        st.markdown("<h1 style='text-align: center;'>RAGent</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>The Multimodal Retrieval-Augmented Generation assistant you need</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Upload document(s) in PDF format</p>", unsafe_allow_html=True)
        #######################################################################################################################

        ########################################## PDF Upload #####################################################
        try:
            if "uploaded_files" not in st.session_state:
                st.session_state.uploaded_files = None

            if "file_upload_check" not in st.session_state:
                st.session_state.file_upload_check = False

            st.session_state.uploaded_files = st.file_uploader(" ", type="pdf", accept_multiple_files=True)
        except:
            st.error('Error in file upload.')
        ########################################################################################################

        # ############################################### Adding Chunks and Mappings to session state ################################################
        # Process each uploaded PDF and add to FAISS index
        if "all_chunks" not in st.session_state:
            st.session_state.all_chunks = []  # Store all chunks from all PDFs

        if 'all_file_page_mappings' not in st.session_state:
            st.session_state.all_file_page_mappings = []  # Store file and page mappings for all PDFs
        # ####################################################################################################################

        if 'files_processed_check' not in st.session_state:
            st.session_state.files_processed_check = False

        if 'file_type_check' not in st.session_state:
            st.session_state.file_type_check = None

        # ############################################## Create Embedding from the uploaded PDFs ##########################################
        try:
            button_col1, button_col2 = st.columns(2)
            with button_col1:
                if st.button('Process Files'):
                    if st.session_state.uploaded_files :
                        for uploaded_file in st.session_state.uploaded_files:
                            with st.spinner(f"Processing {uploaded_file.name}..."):
                                #if 'embed_check' not in st.session_state:
                                text_chunks, image_chunks, file_page_mapping_text, file_page_mapping_image = extract_pdf_data(uploaded_file, uploaded_file.name)
                                embed_pdf(text_chunks, image_chunks)
                                st.session_state.all_chunks.extend(text_chunks)
                                st.session_state.all_file_page_mappings.extend(file_page_mapping_text)
                                st.session_state.all_chunks.extend(image_chunks)
                                st.session_state.all_file_page_mappings.extend(file_page_mapping_image)

                        st.success("All PDFs have been processed and indexed.")
                        st.session_state.files_processed_check = True
                        #st.write(st.session_state.all_file_page_mappings)
        except:
            #st.error('Error in creating embeddings.')
            pass
        #############################################################################################################################

        try:
            if st.session_state.files_processed_check:
                text_question = st.text_area("Enter your question", value = "")

                if text_question:
                    text_question_list = [text_question]

                    if 'answer_list' not in st.session_state:
                        st.session_state.answers_list = []

                    if 'files_pages_list' not in st.session_state:
                        st.session_state.files_pages_list = []

                    if st.button('Generate Answer') and text_question:
                        answers_list, files_pages_list = answer_question(text_question_list, st.session_state.all_chunks, st.session_state.all_file_page_mappings)
                        # st.session_state.ans_generated_check = True
                        st.session_state.answers_list = answers_list
                        st.session_state.files_pages_list = files_pages_list
                    try:
                        st.write("---")
                        st.write("**Answer:**")
                        st.write(st.session_state.answers_list[0])
                        st.write("---")
                        st.write("**Reference(s):**")
                        for file_name, page_num in st.session_state.files_pages_list[0]:
                                st.write(f"- File: {file_name}, Page: {page_num}")
                    except Exception as e:
                        #st.error(e)
                        pass
        
        except Exception as e:
            #st.error(e)
            pass

    ################################################################################## Wrapper for Left Section End ######################################################################

    ################################################################################## Wrapper for Right Section Start ####################################################################
    with main_col2:
        try:
            if st.session_state.uploaded_files:
                # Display the uploaded files in a selection box
                pdf_file_names = [uploaded_file.name for uploaded_file in st.session_state.uploaded_files]
                pdf_file_names.insert(0, "Select PDF File")
                selected_pdf = st.selectbox("Select a PDF to view", pdf_file_names)

                # Retrieve the selected PDF file
                selected_file = None
                for uploaded_file in st.session_state.uploaded_files:
                    if uploaded_file.name == selected_pdf:
                        selected_file = uploaded_file
                        break
        # Display the selected PDF
            if selected_file:
                st.subheader(f"Viewing PDF: {selected_pdf}")

                binary_data = selected_file.getvalue()
                pdf_viewer(input=binary_data, width=700)

        except Exception as e:
            st.error(e)

    ######################################### Making only the second column scrollable ######################################
    css = '''
    <style>
        section.main>div {
            padding-bottom: 1rem;
        }
        /* Target only the second column to make it scrollable */
        [data-testid="stColumn"]:nth-child(2) > div > div {
            overflow-y: auto;
            max-height: 90vh;  /* Allow scrolling when content overflows */
        }
    </style>
    '''

    # Inject the CSS into the Streamlit app
    st.markdown(css, unsafe_allow_html=True)
    ######################################### Making only the second column scrollable ######################################

except Exception as e:
    #st.error({e})
    pass