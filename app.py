import re
import streamlit as st
import pandas as pd
import plotly.express as px
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(page_title="CareerForge AI",page_icon="🚀",layout="wide")
st.title("🚀 CareerForge — Resume & Skill Analyzer")
st.caption("Transparent keyword-based resume comparison • No external AI API required")
from skill_utils import compare
def pdf_text(upload):
    if upload.size > 2_000_000:
        raise ValueError("File must be 2 MB or smaller.")
    reader = PdfReader(BytesIO(upload.getvalue()))
    if reader.is_encrypted:
        raise ValueError("Password-protected PDFs are not supported.")
    if len(reader.pages) > 20:
        raise ValueError("PDF must be 20 pages or fewer.")
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not text.strip():
        raise ValueError("No selectable text found. Scanned PDFs are not supported.")
    return text
with st.sidebar:
    st.header("Input")
    uploaded = st.file_uploader("Resume (optional PDF or TXT)",type=["pdf","txt"])
    st.caption("Uploaded documents are processed in the app session. Avoid uploading sensitive personal information.")
default_resume = "Python, pandas, numpy, Streamlit, SQL, Git, Arduino, data analysis"
resume = st.text_area("Resume text",value=default_resume,height=180)
if uploaded:
    try:
        if uploaded.size > 2_000_000:
            raise ValueError("File must be 2 MB or smaller.")
        resume = pdf_text(uploaded) if uploaded.name.lower().endswith(".pdf") else uploaded.getvalue().decode("utf-8-sig")
        if not resume.strip():
            raise ValueError("Uploaded resume is empty.")
        st.info(f"Analyzing uploaded file: {uploaded.name}")
    except Exception:
        st.error("Could not read the resume. Upload a valid, unencrypted text-based PDF or UTF-8 TXT (maximum 2 MB).")
        st.stop()
job = st.text_area("Paste job requirements",value="Looking for Python, SQL, machine learning, scikit-learn, Git, Docker, AWS and communication skills.",height=150)
matched, missing, score = compare(resume, job)
a,b,c = st.columns(3)
a.metric("Skill coverage",f"{score:.0f}%" if score is not None else "N/A")
b.metric("Matched skills",len(matched))
c.metric("Missing skills",len(missing))
if score is None:
    st.warning("No known skills found in the job description. Add more specific skill requirements.")
else:
    st.progress(score/100)
    st.plotly_chart(px.bar(pd.DataFrame({"Category":["Matched","Missing"],"Skills":[len(matched),len(missing)]}),x="Category",y="Skills",title="Requirement coverage"),use_container_width=True)
left,right = st.columns(2)
with left:
    st.subheader("Skills matched")
    st.write(", ".join(matched) if matched else "None identified")
with right:
    st.subheader("Skills to learn")
    st.write(", ".join(missing) if missing else "No gaps identified")
st.subheader("Suggested learning roadmap")
if missing:
    for i,s in enumerate(missing,1):
        st.write(f"{i}. **{s.title()}** — study fundamentals, build a small project, and document it on GitHub.")
else:
    st.write("Add a job description to generate a roadmap.")
st.info("Coverage is a simple keyword-overlap metric, NOT an ATS score, hiring probability, or validated assessment. PDF extraction may miss scanned documents.")
