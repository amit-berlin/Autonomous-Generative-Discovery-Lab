import streamlit as st
from io import BytesIO
import PyPDF2

st.set_page_config(page_title="AMPIP Smallest MVP", layout="wide")
st.title("AMPIP MVP – Patent Draft & RPA Demo")

# -------------------- Helper Functions --------------------
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def draft_patent(text, doc_name):
    keywords = list(set([w for w in text.split() if len(w)>4][:5]))
    abstract = f"Abstract for {doc_name}: Innovation involving {', '.join(keywords)}."
    claims = f"Claim 1: Method using {', '.join(keywords)}."
    description = f"Description: Detailed method leveraging {', '.join(keywords)}."
    return f"{abstract}\n\n{claims}\n\n{description}"

def simulate_rpa(doc_name):
    return f"RPA Simulation: Patent for {doc_name} submitted successfully."

def generate_certificate(doc_name):
    return f"Patent Certificate for {doc_name}\nStatus: Granted\nCongratulations!"

# -------------------- User Upload --------------------
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    doc_name = uploaded_file.name.split(".")[0]

    st.subheader("Patent Draft")
    draft_text = draft_patent(text, doc_name)
    st.text_area("Drafted Patent Application", draft_text, height=250)

    st.subheader("RPA Submission")
    rpa_text = simulate_rpa(doc_name)
    st.write(rpa_text)

    st.subheader("Download Your Patent Certificate")
    certificate_text = generate_certificate(doc_name)
    st.download_button(
        label="Download Patent Certificate",
        data=certificate_text,
        file_name=f"{doc_name}_PatentCertificate.txt",
        mime="text/plain"
    )

    st.success("Patent Drafting and RPA Simulation Complete!")
