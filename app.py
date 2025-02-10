import streamlit as st
import ollama

desiredModel = "falcon3:3b"

st.title("Latex Formula Generator")

SYSTEM_PROMPT = "You are a LaTeX generation model. The user will give you the name or description of a formula. Provide only the LaTeX code that visualizes it. No text or explanation."

def generate_response(questionToAsk):
    response = ollama.chat(
        model=desiredModel,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": questionToAsk},
        ],
    )
    #print(response)
    #print("\n")
    content = response.get("message", {}).get("content", "").strip()

    if not content:
        st.error("No response received from the model.")
        return

    latex_code = None
    if "$$" in content:
        parts = content.split("$$")
        if len(parts) >= 3:
            latex_code = parts[1].strip()
    elif "```latex" in content:
        parts = content.split("```latex")
        if len(parts) >= 2:
            latex_code = parts[1].split("```")[0].strip()

    if latex_code:
        st.latex(latex_code)
    else:
        st.error("Failed to extract LaTeX code.")
        st.text(content)


with st.form("my_form"):
    text = st.text_area("Enter your formula name or description", "")
    submitted = st.form_submit_button("Generate LaTeX")

    if submitted and text.strip():
        generate_response(text)
