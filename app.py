import streamlit as st
import ollama

desiredModel = "falcon3:3b"

st.title("Latex Formula Generator by Piyush")

SYSTEM_PROMPT = "You are a LaTeX generation model. The user will give you the name or description of a formula.provide the LaTeX code that visualizes it.Always provide the LaTeX code. No text or explanation. No clarification. No context"


def generate_response(questionToAsk):
    response = ollama.chat(
        model=desiredModel,
        messages=[
            {
                "role": "user",
                "content": questionToAsk,
            },
        ],
    )
    print(response)
    # print a line break
    print("\n")
    content = response["message"]["content"]

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

    text = SYSTEM_PROMPT + text
    submitted = st.form_submit_button("come on")
    if submitted:
        generate_response(text)
