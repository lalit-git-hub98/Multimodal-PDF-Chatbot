import streamlit as st
import base64
import os

try:
    ############################################### Webpage Configuration ##############################################
    st.set_page_config(page_title="RAGent", page_icon=":page_with_curl:", layout="wide")

    main_col1, main_col2 = st.columns([0.5, 0.5])

    ############################################################## Wrapper for Middle Section ###########################################################################################
    with main_col1:
        st.markdown("<h1 style='text-align: center;'>RAGent</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>The Multimodal Retrieval-Augmented Generation assistant you need</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Upload contract document(s) in PDF format</p>", unsafe_allow_html=True)
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
        # # Process each uploaded PDF and add to FAISS index
        # if "all_chunks" not in st.session_state:
        #     st.session_state.all_chunks = []  # Store all chunks from all PDFs

        # if 'all_file_page_mappings' not in st.session_state:
        #     st.session_state.all_file_page_mappings = []  # Store file and page mappings for all PDFs
        # ####################################################################################################################

        # if 'files_processed_check' not in st.session_state:
        #     st.session_state.files_processed_check = False

        # if 'file_type_check' not in st.session_state:
        #     st.session_state.file_type_check = None

        # ############################################## Create Embedding from the uploaded PDFs ##########################################
        # try:
        #     file_types = ['General', 'Shipping & Logistics', 'RFI/RFP (Bid)', 'Contract']
        #     selected_file_type = st.selectbox('Select File Type', file_types)
        #     button_col1, button_col2 = st.columns(2)
        #     with button_col1:
        #         if st.button('Process Files'):
        #             if st.session_state.uploaded_files :
        #                 for uploaded_file in st.session_state.uploaded_files:
        #                     with st.spinner(f"Processing {uploaded_file.name}..."):
        #                         #if 'embed_check' not in st.session_state:
        #                         chunks, file_page_mapping = embed_pdf(uploaded_file, uploaded_file.name)
        #                             #st.session_state.embed_check = True
        #                             #st.session_state.chunks = chunks
        #                             #st.session_state.file_page_mapping = file_page_mapping
        #                         st.session_state.chunks = chunks
        #                         st.session_state.file_page_mapping = file_page_mapping
        #                         st.session_state.all_chunks.extend(st.session_state.chunks)
        #                         st.session_state.all_file_page_mappings.extend(st.session_state.file_page_mapping)
        #                         #st.write(f'Processed file: {uploaded_file.name}')

        #                 st.success("All PDFs have been processed and indexed.")
        #                 st.session_state.files_processed_check = True
        #                 #st.write(st.session_state.all_file_page_mappings)
        # except:
        #     st.error('Error in creating embeddings.')
        #############################################################################################################################

    ################################################################################## Wrapper for Middle Section End ###############################################################

    ################################################################################## Wrapper for Left Section Start ####################################################################
    # with main_col1:
    #     try:
    #         if st.session_state.files_processed_check:
    #             text_question = st.text_area("Enter your question", value = "")

    #             text_question_list = [text_question]

    #             if st.button('Generate Answer') and text_question:
    #                 answers_list_side, files_pages_list_side = answer_question(text_question_list, st.session_state.all_chunks, st.session_state.all_file_page_mappings)
    #                 # st.session_state.ans_generated_check = True
    #                 st.session_state.answers_list_side = answers_list_side
    #                 st.session_state.files_pages_list_side = files_pages_list_side
    #             try:
    #                 st.write("---")
    #                 st.write("**Answer:**")
    #                 st.write(st.session_state.answers_list_side[0])
    #                 st.write("---")
    #                 st.write("**Reference(s):**")
    #                 for file_name, page_num in st.session_state.files_pages_list_side[0]:
    #                         st.write(f"- File: {file_name}, Page: {page_num}")
    #             except:
    #                 pass
                    
    #                 #st.write(files_pages_list_side)
        
    #     except:
    #         pass

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

                # Read PDF file
                pdf_bytes = selected_file.read()

                # Encode the PDF file in base64 for displaying in iframe
                pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

                # Display the PDF file in an iframe using an HTML embed
                pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="1000" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
        except:
            pass

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


    ################################################################################## Wrapper for Right Section End ######################################################################


    ########################################################################## Second Wrapper for Middle Section Start #####################################################################
    
    ############################################################################## Second Wrapper for Middle Section Start ###############################################################

except:
    st.error('Some error occurred.')