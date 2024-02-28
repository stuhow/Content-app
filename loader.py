import tiktoken
import re
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup

def document_loader(url, headers):
    #load documents
    loader = RecursiveUrlLoader(
        url=url, max_depth=1, headers=headers, extractor=lambda x: Soup(x, "html.parser").text
    )
    docs = loader.load()

    # remove long documents
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    new_docs = []
    for doc in docs:
        if len(encoding.encode(doc.page_content)) < 2500:
            new_docs.append(doc)

    # Remove 2 or more consecutive \n with a single \n in each document
    for doc in new_docs:
        doc.page_content = re.sub(r'\n{2,}', '\n', doc.page_content)

    # Remove 2 or more consecutive \n with a single \n in each document
    for doc in new_docs:
        doc.page_content = re.sub(r'\t{2,}', '\t', doc.page_content)

    return new_docs
