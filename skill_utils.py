"""Transparent skill matching, independent of Streamlit."""
import re

SKILLS = ["python","java","javascript","typescript","sql","excel","machine learning","deep learning","data analysis","pandas","numpy","scikit-learn","tensorflow","pytorch","streamlit","flask","fastapi","react","html","css","git","github","docker","aws","linux","arduino","esp32","iot","embedded systems","c++","communication","leadership","problem solving"]

def skills_in(text):
    text = text.casefold()
    return {skill for skill in SKILLS if re.search(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", text)}

def compare(resume, job):
    required = skills_in(job)
    present = skills_in(resume)
    matched = sorted(required & present)
    missing = sorted(required - present)
    coverage = (len(matched) / len(required) * 100) if required else None
    return matched, missing, coverage
