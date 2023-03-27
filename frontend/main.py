import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="Meeting Intelligence Application")

# Define allowed file types
ALLOWED_EXTENSIONS = {'mp3'}

# Define function to check file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create home page
# Define Streamlit app
def main():
    st.title("Upload MP3 to AWS S3")
    
    # Allow user to upload file
    uploaded_file = st.file_uploader("Choose an MP3 file", type=["mp3"])
    
    # If file uploaded, show file details and allow user to save to S3
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        
        # # Allow user to choose S3 file name and folder
        # s3_folder = st.text_input("Enter S3 folder name", "my-folder/")
        # s3_file = st.text_input("Enter S3 file name", uploaded_file.name)
        
        # # If folder doesn't end with a '/', add one
        # if not s3_folder.endswith("/"):
        #     s3_folder += "/"
        
        # If user clicks "Save to S3", upload file to S3
        if st.button("Save to S3"):
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
                payload = {'local_file': uploaded_file, 's3_file': uploaded_file.name}
                r = requests.post("http://localhost:8000/uploadfile/", data=payload)
                if r.status_code == 200:
                    st.success("File uploaded to S3!")
                if r.status_code == 500:
                    st.error("Error uploading file to S3")



    
if __name__ == '__main__':
    main()


