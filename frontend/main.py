import streamlit as st
import random

# Set page title and favicon
st.set_page_config(page_title="Meeting Intelligence Application", page_icon=":microphone:")

# Define allowed file types
ALLOWED_EXTENSIONS = {'mp3'}

# Define function to check file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Define page layout
def page_layout():
    # Define header
    st.header("Meeting Intelligence Application")
    st.subheader("Upload an MP3 file and ask questions about it")
    
    # Define file upload section
    st.write("## Upload a file")
    file = st.file_uploader("Choose an MP3 file", type=["mp3"])
    
    # Check file upload
    if file is not None:
        if allowed_file(file.name):
            st.success("File uploaded successfully!")
            st.audio(file)
        else:
            st.error("Invalid file type. Please upload an MP3 file.")
    
    # Define question section
    st.write("## Ask a question")
    uploaded_files = st.selectbox("Select an uploaded file", [file.name] if file else [], key="uploaded_files")
    
    # Define question input
    questions = ["Summary of the meeting", "Language used in the meeting", "Bottomline of the meeting", "Custom question"]
    question_type = st.selectbox("Select a question type", questions)
    
    if question_type == "Custom question":
        question = st.text_input("Enter a question related to the uploaded file")
    elif question_type:
        question = question_type
    
    # Define submit button
    if file and question_type:
        if st.button("Go"):
            st.write("### Results")
            st.write(f"You asked: **{question}**")
            st.write("Dummy text box")
    
    

# Display page layout
page_layout()
