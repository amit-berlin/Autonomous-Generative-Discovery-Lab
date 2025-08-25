import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import spacy
from textblob import TextBlob

# ------------------ Setup ------------------
st.set_page_config(page_title="AMPIP Minimal MVP", layout="wide")
st.title("AMPIP Minimal MVP – Lightweight Patent Draft Generator")

# Load lightweight models
@st.cache_resource
def load_models():
    nlp = spacy.load("en_core_web_sm")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return nlp, model

nlp, embed_model = load_models()

# Demo prior-art dataset (small)
prior_art_docs = [
    "Method for autonomous data extraction in IT research labs.",
    "System for automated document analysis and novelty scoring.",
    "Technique for intelligent RPA to submit patent applications."
]
prior_art_embeddings = embed_model.encode(prior_art_docs, convert_to_tensor=True)

# ------------------ Helper Functions ------------------
def compute_novelty(doc_text):
    doc_embedding = embed_model.encode(doc_text, convert_to_tensor=True)
    similarity_scores = util.cos_sim(doc_embedding, prior_art_embeddings)
    novelty_score = 1 - similarity_scores.max().item()  # Higher = more novel
    return round(novelty_score,2)

def compute_usefulness(doc_text):
    blob = TextBlob(doc_text)
    polarity = blob.sentiment.polarity
    usefulness_score = round((polarity +1)/2, 2)  # scale 0-1
    return usefulness_score

def extract_keywords(doc_text):
    doc = nlp(doc_text)
    keywords = list(set([ent.text for ent in doc.ents if len(ent.text)>1]))
    if not keywords:
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop][:5]
    return keywords

def generate_patent_draft(doc_name, doc_text, novelty, usefulness, keywords):
    abstract = f"Abstract for {doc_name}: Innovation involving {', '.join(keywords)}."
    claims = f"Claim 1: Novel method using {', '.join(keywords)}. Novelty Score: {novelty}"
    description = f"Description: The method leverages {', '.join(keywords)}. Usefulness Score: {usefulness}"
    return {"Document": doc_name, "Abstract": abstract, "Claims": claims, "Description": description}

# ------------------ Demo Section ------------------
st.header("Demo Documents")
demo_docs = {
    "Demo_Document_1": "This invention improves automated patent application process in research labs.",
    "Demo_Document_2": "A novel system for multi-agent AI patent drafting in enterprise environments."
}

demo_results = []
for name, text in demo_docs.items():
    novelty = compute_novelty(text)
    usefulness = compute_usefulness(text)
    keywords = extract_keywords(text)
    draft = generate_patent_draft(name, text, novelty, usefulness, keywords)
    demo_results.append(draft)

st.subheader("Patent Drafts – Demo")
st.table(pd.DataFrame(demo_results))

# ------------------ User Upload Section ------------------
st.header("Upload Your Document")
uploaded_file = st.file_uploader("Upload PDF/TXT/DOCX", type=['txt'], key="file_upload")
if uploaded_file:
    text = uploaded_file.read().decode('utf-8')
    novelty = compute_novelty(text)
    usefulness = compute_usefulness(text)
    keywords = extract_keywords(text)
    draft = generate_patent_draft(uploaded_file.name, text, novelty, usefulness, keywords)

    st.subheader("Step-by-Step Processing")
    st.write(f"- Document Uploaded: {uploaded_file.name}")
    st.write(f"- Keywords Extracted: {', '.join(keywords)}")
    st.write(f"- Novelty Score Computed: {novelty}")
    st.write(f"- Usefulness Score Computed: {usefulness}")
    st.write(f"- Patent Draft Generated")

    st.subheader("Patent Draft Output")
    st.table(pd.DataFrame([draft]))

    st.subheader("Download Patent Draft")
    content = f"{draft['Abstract']}\n{draft['Claims']}\n{draft['Description']}"
    st.download_button(
        label=f"Download Draft for {uploaded_file.name}",
        data=content,
        file_name=f"{uploaded_file.name}_PatentDraft.txt",
        mime="text/plain"
    )
