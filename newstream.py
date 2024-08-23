import streamlit as st
from PIL import Image
from identify import *
from io import BytesIO
import os

st.set_page_config(page_title="AI For Business Workshop", page_icon=":smiley:")

def save_uploaded_file(uploaded_file, folder_name):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Determine the new file path
    file_count = len([name for name in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, name))])
    file_extension = uploaded_file.name.split('.')[-1]
    
    # Make sure the file name is in lowercase
    folder_base_name = os.path.basename(folder_name).lower()
    new_file_name = f"{folder_base_name}_{file_count + 1}.{file_extension.lower()}"
    new_file_path = os.path.join(folder_name, new_file_name)
    
    # Save the uploaded file to the specified folder
    with open(new_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return new_file_path

def main():
    st.title("AI For Business Workshop")

    # Sample image download section
    sample_image_path = "./sample_image.jpg"
    sample_image = Image.open(sample_image_path)

    buf = BytesIO()
    sample_image.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    sample_image_name = "sample_image.jpg"
    st.download_button(label="Download Sample Image", data=byte_im, file_name=sample_image_name, key="download_button")

    # Section to upload a picture to the database
    st.subheader("Upload a Picture to the Database")
    person_name = st.text_input("Enter the name of the person:")
    database_uploaded_file = st.file_uploader("Choose a picture to upload to the database...", type=["jpg", "jpeg", "png"], key="db_upload")

    if person_name and database_uploaded_file:
        folder_name = os.path.join("database", person_name)
        
        if st.button("Upload Picture to Database"):
            file_path = save_uploaded_file(database_uploaded_file, folder_name)
            st.success(f"Picture successfully uploaded to {file_path}!")

    # Section to upload an image for face recognition
    st.subheader("Face Recognition")
    uploaded_file = st.file_uploader("Choose an image to analyze...", type=["jpg", "jpeg", "png"], key="analyze_upload")

    if uploaded_file is not None:
        image_placeholder = st.empty()
        recognizing_message = st.empty()

        image_placeholder.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        recognizing_message.write("Recognizing...")
       
        total_faces = faceDetection(uploaded_file)
        names = faceRecognition(uploaded_file)

        # Face Detection Results Section
        recognizing_message.empty()  
        st.header("Face Detection Results:")
        st.write(f"Total Faces Detected: {total_faces}")
        st.write(f"Total Recognized Faces: {getKnownFaces()}")
        st.write(f"Total Unrecognized Faces: {getUnknownFaces()}")

        # Names Section
        if names:
            st.header("Names:")
            for name in names:
                st.write(f"- {name}")

        # Known Faces Section
        known_names = getKnownName()
        if known_names:
            st.header("Known Faces:")
            for name in known_names:
                known_image_path = f"./known/{name}.jpg"
                known_image = Image.open(known_image_path)
                st.image(known_image, caption=name, width=200)

        # Unknown Faces Section
        st.header("Unknown Faces:")
        if getUnknownFaces() == 0:
            st.write("None")
        else:
            for i in range(getUnknownFaces()):
                unknown_image_path = f"./unknown/{i}.jpg"
                unknown_image = Image.open(unknown_image_path)
                st.image(unknown_image, caption=f"Unknown Face #{i + 1}", width=200)

        # Reset the known names and face counts
        setKnownName()
        setFacesToZero()

if __name__ == "__main__":
    main()
