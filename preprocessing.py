import tiktoken
import re

def summarisation_preprocessing(documents):
# remove long documents
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    new_docs = []
    for doc in documents:
        if len(encoding.encode(doc.page_content)) < 2500:
            new_docs.append(doc)

    # Remove 2 or more consecutive \n with a single \n in each document
    for doc in new_docs:
        doc.page_content = re.sub(r'\n{2,}', '\n', doc.page_content)

    # Remove 2 or more consecutive \n with a single \n in each document
    for doc in new_docs:
        doc.page_content = re.sub(r'\t{2,}', '\t', doc.page_content)

    return new_docs
