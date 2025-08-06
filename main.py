import streamlit as st

st.header(body="Analyze Any Document", anchor='center')
#
# pdf_image = st.image(image="assects/pdf.png")

st.divider()

pdf, docs, excel = st.columns(3)

pdf.image(image="assects/pdf.png")
pdf.page_link(page="pages/page_pdf.py", label="For PDF.")

docs.image(image="assects/docs.png")
docs.page_link(page="pages/page_docs.py", label="For Docs.")

excel.image(image="assects/excel.png")
excel.page_link(page="pages/page_excel.py", label="For Excel.")

