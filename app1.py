import streamlit as st
import requests

API_URL = "https://api.yourdomain.com/generate"  # Replace with your Cloudflare URL

st.title("LaTeX Formula Generator by Piyush")

SYSTEM_PROMPT = "You are a LaTeX generation model. The user will give you the name or description of a formula. Provide the LaTeX code that visualizes it. No text or explanation. No clarification. No context."

def generate_response(questionToAsk):
    payload = {
        "model": "falcon3:3b",
        "prompt": SYSTEM_PROMPT + questionToAsk
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        content = response.json()["response"]
    else:
        content = "Error: Unable to fetch response from API."

    try:
        try:
            latex_code = content.split("$$")[1].split("$$")[0].strip()
        except IndexError:
            latex_code = content.split("```latex")[1].split("```")[0].strip()

        formatted_latex_string = latex_code
    except (KeyError, IndexError):
        formatted_latex_string = "Error: LaTeX code not found."

    st.latex(formatted_latex_string)

with st.form("my_form"):
    text = st.text_area("Enter your question here", "")
    submitted = st.form_submit_button("Generate")
    if submitted:
        generate_response(text)
