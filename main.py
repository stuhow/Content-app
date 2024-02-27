
from headers import headers
from prompts import map_template, reduce_template
from chains import map_reduce_chain
from loader import document_loader

def sumarisation(url, headers, map_template, reduce_template, llm):
    documents = document_loader(url, headers)
    text_summary = map_reduce_chain(map_template, reduce_template, documents, llm)
    return text_summary
