import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("PDF to XML Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("Uploading and converting PDF..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{API_URL}/convert-pdf-to-xml", files=files)
        if response.status_code == 200:
            data = response.json()
            st.success(data["message"])
            xml_file = data["xml_file"]
            download_url = f"{API_URL}/download/{xml_file}"
            preview_url = f"{API_URL}/preview/{xml_file}"
            st.markdown(f"[Download XML]({download_url})")
            if st.button("Preview XML"):
                preview_response = requests.get(preview_url)
                if preview_response.status_code == 200:
                    xml_content = preview_response.json()["xml_content"]
                    st.code(xml_content, language="xml")
                else:
                    st.error("Could not preview XML file.")
        else:
            st.error(response.json().get("detail", "Conversion failed."))
