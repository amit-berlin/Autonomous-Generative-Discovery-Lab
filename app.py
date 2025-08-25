import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from textblob import TextBlob
import time

st.set_page_config(page_title="AMPIP AGDL MVP", layout="wide")
st.title("AMPIP AGDL v5 – Autonomous Multi-Agent Patent Innovation Platform (Demo)")

# -------------------- Setup Models --------------------
@st.cache_resource
def load_models():
    nlp = spacy.load("en_core_web_sm")
    return nlp

nlp = load_models()

# Demo prior-art dataset (tiny)
prior_art_docs = [
    "Automated document analysis in IT research labs.",
    "System for multi-agent AI patent drafting.",
    "Technique for RPA-based patent submission."
]

vectorizer = TfidfVectorizer()
prior_art_tfidf = vectorizer.fit_transform(prior_art_docs)

# -------------------- Helper Functions --------------------
def log_step(step_log, message):
    step_log.append(message)
    st.write(f"- {message}")
    time.sleep(0.1)  # simulate real-time processing

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text

def compute_novelty(doc_text):
    doc_vector = vectorizer.transform([doc_text])
    sim_scores = cosine_similarity(doc_vector, prior_art_tfidf)
    novelty_score = 1 - sim_scores.max()
    return round(float(novelty_score),2)

def compute_usefulness(doc_text):
    blob = TextBlob(doc_text)
    polarity = blob.sentiment.polarity
    return round((polarity + 1)/2,2)

def extract_keywords(doc_text):
    doc = nlp(doc_text)
    keywords = list(set([ent.text for ent in doc.ents if len(ent.text)>1]))
    if not keywords:
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop][:5]
    return keywords

def generate_patent_draft(doc_name, doc_text, novelty, usefulness, keywords):
    abstract = f"Abstract for {doc_name}: Innovation involving {', '.join(keywords)}."
    claims = f"Claim 1: Method using {', '.join(keywords)}. Novelty Score: {novelty}"
    description = f"Description: Method leverages {', '.join(keywords)}. Usefulness Score: {usefulness}"
    return {"Document": doc_name, "Abstract": abstract, "Claims": claims, "Description": description}

def simulate_rpa(doc_name):
    steps = [
        "Prepare submission form",
        "Fill abstract field",
        "Fill claims field",
        "Fill description field",
        "Submit application",
        "Receive confirmation"
    ]
    return steps

# -------------------- Demo Section --------------------
st.header("Demo Documents")
demo_docs = {
    "Demo_Document_1": "This invention improves automated patent application process in research labs.",
    "Demo_Document_2": "A novel system for multi-agent AI patent drafting in enterprise environments."
}

demo_results = []
step_log = []

for name, text in demo_docs.items():
    log_step(step_log, f"Processing demo document: {name}")
    pre_text = preprocess_text(text)
    log_step(step_log, "Preprocessing completed")
    keywords = extract_keywords(pre_text)
    log_step(step_log, f"Keywords extracted: {', '.join(keywords)}")
    novelty = compute_novelty(pre_text)
    log_step(step_log, f"Novelty score computed: {novelty}")
    usefulness = compute_usefulness(pre_text)
    log_step(step_log, f"Usefulness score computed: {usefulness}")
    draft = generate_patent_draft(name, pre_text, novelty, usefulness, keywords)
    log_step(step_log, "Patent draft generated")
    demo_results.append(draft)
    rpa_steps = simulate_rpa(name)
    for s in rpa_steps:
        log_step(step_log, f"RPA Step: {s}")
    log_step(step_log, f"Demo document {name} processing complete\n")

st.subheader("Patent Drafts – Demo")
st.table(pd.DataFrame(demo_results))

# -------------------- User Upload Section --------------------
st.header("Upload Your Own Document")
uploaded_file = st.file_uploader("Upload TXT file", type=['txt'], key="file_upload")
if uploaded_file:
    text = uploaded_file.read().decode('utf-8')
    log_step(step_log, f"User uploaded document: {uploaded_file.name}")
    pre_text = preprocess_text(text)
    log_step(step_log, "Preprocessing completed")
    keywords = extract_keywords(pre_text)
    log_step(step_log, f"Keywords extracted: {', '.join(keywords)}")
    novelty = compute_novelty(pre_text)
    log_step(step_log, f"Novelty score computed: {novelty}")
    usefulness = compute_usefulness(pre_text)
    log_step(step_log, f"Usefulness score computed: {usefulness}")
    draft = generate_patent_draft(uploaded_file.name, pre_text, novelty, usefulness, keywords)
    log_step(step_log, "Patent draft generated")
    rpa_steps = simulate_rpa(uploaded_file.name)
    for s in rpa_steps:
        log_step(step_log, f"RPA Step: {s}")
    log_step(step_log, f"User document {uploaded_file.name} processing complete\n")

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

# -------------------- Frontend UX Tutorial --------------------
st.header("Backend Processing Steps – Step-by-Step Tutorial")
st.write("The following 30–40 steps simulate a real enterprise AMPIP AGDL workflow:")
for step in step_log:
    st.write(f"- {step}")

st.success("MVP processing completed successfully. All steps deterministic and error-free on Streamlit Free.")
st.info("Note: In a real web app, these steps would use full LLMs, RPA automation, and enterprise APIs. Currently, this MVP is lightweight and fully deterministic for demo purposes.")
