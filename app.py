import streamlit as st
import time
# from main import sumarisation

def main():
    st.title("Web content app")

    # Input
    url = st.text_input("Enter an email address:")

    # Button to trigger the processing
    if st.button("Process"):
        with st.spinner("Summarising..."):
            time.sleep(10)
            # Processing
            # result = sumarisation(url)
            result = "sdnvlnsd"

        # Display the result
        st.write(result)

if __name__ == "__main__":
    main()
