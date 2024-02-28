import streamlit as st
from chains import map_reduce_chain
from loader import document_loader
from headers import headers
from prompts import map_template, reduce_template
from langchain_openai import ChatOpenAI

def main():
    st.title("Web content app")

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # Input
    url = st.text_input("Enter an email address:")

    # Button to trigger the processing
    if st.button("Summarise"):
        with st.spinner("Checking website..."):
            documents = document_loader(url, headers)

        with st.spinner(f"Summarising {len(documents)} pages..."):
            text_summary = map_reduce_chain(map_template, reduce_template, documents, llm)

        # Display the result
        st.write(text_summary)

if __name__ == "__main__":
    main()
