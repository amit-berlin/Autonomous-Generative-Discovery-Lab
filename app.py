import streamlit as st
import time

st.set_page_config(page_title="AMPIP AGDL Pure MVP", layout="wide")
st.title("AMPIP AGDL MVP – Error-Free Demo (No Dependencies)")

# -------------------- Helper Functions --------------------
def log_step(steps_log, message):
    steps_log.append(message)
    st.write(f"- {message}")
    time.sleep(0.05)  # simulate processing

def preprocess_text(text):
    # Simple lowercase + remove punctuation
    return ''.join([c.lower() if c.isalnum() or c.isspace() else ' ' for c in text])

def extract_keywords(text):
    # Simple word frequency for keywords
    words = text.split()
    freq = {}
    for w in words:
        if len(w)>3:
            freq[w] = freq.get(w,0)+1
    keywords = sorted(freq, key=freq.get, reverse=True)[:5]
    return keywords

def compute_novelty(text):
    # Simulated novelty score
    score = 0.7 + 0.3*min(len(text)/500,1.0)
    return round(score,2)

def compute_usefulness(text):
    # Simulated usefulness score
    score = 0.5 + 0.5*min(text.count("improve")/5,1.0)
    return round(score,2)

def generate_patent_draft(doc_name, text, novelty, usefulness, keywords):
    abstract = f"Abstract for {doc_name}: Innovation using {', '.join(keywords)}."
    claims = f"Claim 1: Novel method using {', '.join(keywords)}. Novelty Score: {novelty}"
    description = f"Description: The method leverages {', '.join(keywords)}. Usefulness Score: {usefulness}"
    return {"Document": doc_name, "Abstract": abstract, "Claims": claims, "Description": description}

def simulate_rpa(doc_name):
    return [
        "Prepare submission form",
        "Fill abstract field",
        "Fill claims field",
        "Fill description field",
        "Submit application",
        "Receive confirmation"
    ]

# -------------------- Step Log --------------------
step_log = []

# -------------------- Demo Section --------------------
st.header("Demo Documents")
demo_docs = {
    "Demo_Document_1": "This invention improves automated patent application process in research labs.",
    "Demo_Document_2": "A novel system for multi-agent AI patent drafting in enterprise environments."
}

demo_results = []
for name,text in demo_docs.items():
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
    rpa_steps = simulate_rpa(name)
    for s in rpa_steps:
        log_step(step_log, f"RPA Step: {s}")
    log_step(step_log, f"Demo document {name} processing complete\n")
    demo_results.append(draft)

st.subheader("Patent Drafts – Demo")
st.table(demo_results)

# -------------------- User Upload --------------------
st.header("Upload Your Document")
uploaded_file = st.file_uploader("Upload TXT file", type=['txt'])
if uploaded_file:
    text = uploaded_file.read().decode('utf-8')
    doc_name = uploaded_file.name
    log_step(step_log, f"User uploaded document: {doc_name}")
    pre_text = preprocess_text(text)
    log_step(step_log, "Preprocessing completed")
    keywords = extract_keywords(pre_text)
    log_step(step_log, f"Keywords extracted: {', '.join(keywords)}")
    novelty = compute_novelty(pre_text)
    log_step(step_log, f"Novelty score computed: {novelty}")
    usefulness = compute_usefulness(pre_text)
    log_step(step_log, f"Usefulness score computed: {usefulness}")
    draft = generate_patent_draft(doc_name, pre_text, novelty, usefulness, keywords)
    log_step(step_log, "Patent draft generated")
    rpa_steps = simulate_rpa(doc_name)
    for s in rpa_steps:
        log_step(step_log, f"RPA Step: {s}")
    log_step(step_log, f"User document {doc_name} processing complete\n")

    st.subheader("Patent Draft Output")
    st.table([draft])

    st.subheader("Download Patent Draft")
    content = f"{draft['Abstract']}\n{draft['Claims']}\n{draft['Description']}"
    st.download_button(
        label=f"Download Draft for {doc_name}",
        data=content,
        file_name=f"{doc_name}_PatentDraft.txt",
        mime="text/plain"
    )

# -------------------- Frontend Step-by-Step UX --------------------
st.header("Backend Processing Steps – Tutorial")
st.write("The following 30–40 steps are simulated for demonstration:")
for step in step_log:
    st.write(f"- {step}")

st.success("MVP processing completed successfully. Fully deterministic and error-free on Streamlit Free.")
st.info("Note: In a real web app, these steps would use real NLP/ML APIs, LLMs, RPA automation, and enterprise tools. Currently, this MVP is lightweight and deterministic for demo purposes.")
