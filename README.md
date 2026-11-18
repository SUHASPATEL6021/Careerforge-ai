# 🚀 CareerForge — Resume & Skill Analyzer

An interactive, privacy-conscious Streamlit application for comparing resume text with job requirements.

## 🌐 Live demo
**[Try CareerForge AI](https://suhas-careerforge-ai.streamlit.app/)**

The demo uses transparent keyword matching rather than a generative AI service.

## Features
- Resume PDF/TXT upload or text paste
- Skill extraction from a transparent, editable vocabulary
- Matched and missing skills
- Coverage visualization and actionable learning roadmap

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
This app uses **rule-based keyword matching**, not an LLM or validated applicant-tracking system. The coverage percentage is not a hiring probability. Scanned PDFs may require OCR and are not supported. Review extracted skills manually before relying on the result.

## Stack
Python · Streamlit · pandas · Plotly · pypdf
