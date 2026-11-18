import re
import streamlit as st
import pandas as pd
import plotly.express as px
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(page_title="CareerForge AI",page_icon="🚀",layout="wide")
st.title("🚀 CareerForge — Resume & Skill Analyzer")
st.caption("Transparent keyword-based resume comparison • No external AI API required")
SKILLS = ["python","java","javascript","typescript","sql","excel","machine learning","deep learning","data analysis","pandas","numpy","scikit-learn","tensorflow","pytorch","streamlit","flask","fastapi","react","html","css","git","github","docker","aws","linux","arduino","esp32","iot","embedded systems","c++","communication","leadership","problem solving"]
def skills_in(text):
    text = text.lower()
    return {s for s in SKILLS if re.search(r"(?<![a-z0-9])"+re.escape(s)+r"(?![a-z0-9])",text)}
def pdf_text(upload):
    return "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(upload.getvalue())).pages)
with st.sidebar:
    st.header("Input")
    uploaded = st.file_uploader("Resume (optional PDF or TXT)",type=["pdf","txt"])
    st.caption("Uploaded documents are processed in the app session. Avoid uploading sensitive personal information.")
default_resume = "Python, pandas, numpy, Streamlit, SQL, Git, Arduino, data analysis"
resume = st.text_area("Resume text",value=default_resume,height=180)
if uploaded:
    try:
        resume = pdf_text(uploaded) if uploaded.name.lower().endswith(".pdf") else uploaded.getvalue().decode("utf-8")
        st.info(f"Analyzing uploaded file: {uploaded.name}")
    except Exception as e:
        st.error(f"Could not read file: {e}")
        st.stop()
job = st.text_area("Paste job requirements",value="Looking for Python, SQL, machine learning, scikit-learn, Git, Docker, AWS and communication skills.",height=150)
required = skills_in(job)
present = skills_in(resume)
matched = sorted(required & present)
missing = sorted(required - present)
score = len(matched)/len(required)*100 if required else 0
a,b,c = st.columns(3)
a.metric("Skill coverage",f"{score:.0f}%" if required else "N/A")
b.metric("Matched skills",len(matched))
c.metric("Missing skills",len(missing))
if not required:
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
