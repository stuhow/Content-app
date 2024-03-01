import streamlit as st
from chains import map_reduce_chain
from loader import document_loader
from headers import headers
from prompts import map_template, reduce_template
from langchain_openai import ChatOpenAI
from langchain.callbacks.manager import collect_runs
from streamlit_feedback import streamlit_feedback
from langsmith import Client
import os

os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]

client = Client()

def main():
    st.title("Hotel content app")

    # Initialize session state if it doesn't exist
    if "text_summary" not in st.session_state:
        st.session_state.text_summary = None
    if "run_id" not in st.session_state:
        st.session_state.run_id = None

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=st.secrets["OPENAI_API_KEY"])


    # Input
    url = st.text_input("Enter the hotel website address:")

    # Button to trigger the processing
    if st.button("Summarise"):
        with st.spinner("Checking website..."):
            documents = document_loader(url, headers)

        if len(documents) > 0:

            with st.spinner(f"Summarising {len(documents)} pages..."):
                with collect_runs() as cb:
                    text_summary = map_reduce_chain(map_template, reduce_template, documents, llm)
                    run_id = cb.traced_runs[0].id

                    #store as session states
                    st.session_state.text_summary = text_summary
                    st.session_state.run_id = run_id
        else:
            st.write("Something went wrong. Please send the hotel website to Stu.")

    # Display the result if run_id is not None
    if st.session_state.run_id is not None:
        st.write(st.session_state.text_summary)

    feedback_option = ("thumbs")

    if st.session_state.run_id:
        feedback = streamlit_feedback(
            feedback_type=feedback_option,
            optional_text_label="Please provide an explanation",
            key=f"feedback_{st.session_state.run_id}",
        )

        # Define score mappings for both "thumbs" and "faces" feedback systems
        score_mappings = {
            "thumbs": {"👍": 1, "👎": 0},
            "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
        }

        # Get the score mapping based on the selected feedback option
        scores = score_mappings[feedback_option]

        if feedback:
            # Get the score from the selected feedback option's score mapping
            score = scores.get(feedback["score"])

            if score is not None:
                # Formulate feedback type string incorporating the feedback option
                # and score value
                feedback_type_str = f"{feedback_option} {feedback['score']}"

                # Record the feedback with the formulated feedback type string
                # and optional comment
                feedback_record = client.create_feedback(
                    st.session_state.run_id,
                    feedback_type_str,
                    score=score,
                    comment=feedback.get("text"),
                )
                st.session_state.feedback = {
                    "feedback_id": str(feedback_record.id),
                    "score": score,
                }
            else:
                st.warning("Invalid feedback score.")




if __name__ == "__main__":
    main()
