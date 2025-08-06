import streamlit as st
import helpers.PDF_helper as p
import json as j
import os

def get_pdf_json(name: str) -> str:
    pdf = p.Pdf(name)
    return pdf.get_pdf()


st.header("PDF to JSON convertor")
st.divider()
uploaded = st.file_uploader("Upload your pdf", type=['pdf'], accept_multiple_files=False)



if uploaded is not None:
    try:
        temp_file = uploaded.name
        with open(temp_file, 'wb') as f:
            f.write(uploaded.getvalue())

        json = get_pdf_json(temp_file)

        left, right = st.columns([0.7, .3])

        left.write("Preview")
        json_container = left.container(height=500, border=True)

        json_container.json(json, width=900)

        right.download_button(label="Download", data=json, file_name=temp_file.split('.')[0]+".json")

        os.remove(os.curdir+'/'+temp_file)

    except Exception as e:
        st.error(f"Error reading or processing PDF file: {e}")
        st.warning("Please make sure you are uploading a valid PDF file")