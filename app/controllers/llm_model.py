import os
from pathlib import Path
import json

# from langchain_openai import ChatOpenAI
# from langchain_google_vertexai import ChatVertexAI
from langchain_cohere import ChatCohere
from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain import hub
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# from langchain_openai import OpenAIEmbeddings
from langchain_cohere import CohereEmbeddings
# from langchain_core.embeddings import FakeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..utils.utility_functions import (
    get_file_type
)
from ..utils.global_variables import (
    JSON, PDF
)

# llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
# llm = ChatVertexAI(model="gemini-pro")


llm = ChatCohere(model="command-r")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_model_from_document(document_file_path):
    # Load, chunk and index the contents of the blog.
    
    rag_chain, error = None, None
    loader = None
    
    file_type = get_file_type(document_file_path)

    
    if file_type == PDF:
        loader = PyPDFLoader(document_file_path)
    elif file_type == JSON:
        loader = JSONLoader(
                    file_path=document_file_path,
                    jq_schema='.[]',
                    text_content=False
                    )

    else:
        error = "File Type not supported."
        return rag_chain, error

    docs = loader.load()


    splits = text_splitter.split_documents(docs)
    # embeddings = FakeEmbeddings(size=150)
    vectorstore = Chroma.from_documents(documents=splits, embedding=CohereEmbeddings(model="embed-english-v3.0"))


    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


    return rag_chain, error