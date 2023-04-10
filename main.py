import streamlit as st
import openai
import pdfplumber
import requests
import base64
import time
from bs4 import BeautifulSoup

openai.api_key = "<YOUR OPEN AI API KEY>"


def generate_cover_letter(my_CV, link_to_job):
    cv_role = "You’re an assistant who helps to write cover letters for employers. I will send you my CV in plain text. You don't need answer to it, just remember and summarize it inside yourself."
    content_role = "You’re an assistant who helps to write cover letters and find job. I will send you job description. Based on information and requirements from employer, you have to write cover letter using my CV and align it with job description."

    page = requests.get(link_to_job)
    soup = BeautifulSoup(page.content, "html.parser")
    page_text = soup.get_text()

    completion = openai.api_resources.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content":
                   cv_role},
                  {"role": "user", "content": my_CV},
                  {"role": "system", "content":
                   content_role},
                  {"role": "user", "content": page_text}  # link_to_job}

                  ]
    )

    result = completion.choices[0].message.content
    return result


def parse_pdf(filepath):
    text = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=1)
            text.append(page_text)
    text = '\n'.join(text)
    return text


st.set_page_config(page_title="Cover Letter", page_icon=":robot_face:")
st.title("Cover Letter Generator")
cv_option = st.selectbox("Select the format of your CV", ["PDF", "Plain Text"])
st.header("Upload your CV")
cv_text = None
if cv_option == "PDF":
    cv_file = st.file_uploader("Upload PDF", type=["pdf"])
    with open("CV.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Here is example of CV, that is parsed correctly.",
                       data=PDFbyte,
                       file_name="CV.pdf",
                       mime='application/octet-stream')

    x_tolerance = st.slider('x_tolerance', min_value=0.0, max_value=10.0, value=1.0, step=0.5,
                            help='It is recommended to leave it at its default value.')
    if cv_file is not None:
        cv_data = cv_file.read()
        with pdfplumber.open(cv_file) as pdf:
            cv_text = "\n".join(
                [page.extract_text(x_tolerance=x_tolerance) for page in pdf.pages])

        st.success("CV uploaded successfully!")
        st.header("Parsed text")
        st.info(
            'NOTE: If words stick together in the parsed text, try to decrease the **x_tolerance** parameter')
        st.text(cv_text)
else:
    cv_text = st.text_area("Enter your CV in plain text", height=450)

st.header("Enter job link")
job_link = st.text_input("Enter job link")

if st.button("Generate Cover Letter"):
    if cv_text is None:
        st.warning("Please upload your CV")
    elif job_link == "":
        st.warning("Please enter job link")
    else:
        with st.spinner('Running... (it may take up to 30 seconds)'):
            cover_letter = generate_cover_letter(cv_text, job_link)
            time.sleep(1)
        st.subheader("Cover Letter")

        st.markdown(
            f"<div style='font-size: large'>{cover_letter}</div>", unsafe_allow_html=True)
