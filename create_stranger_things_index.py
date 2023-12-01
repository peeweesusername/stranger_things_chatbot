from llama_index import VectorStoreIndex, ServiceContext, Document, GPTVectorStoreIndex, SimpleDirectoryReader, download_loader
from llama_index.llms import OpenAI
import streamlit as st
import openai
import os

os.environ["OPENAI_API_KEY"] = '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'

WikipediaReader = download_loader('WikipediaReader')

def load_data():
    loader = WikipediaReader()
    docs = loader.load_data(pages=['Stranger Things'], auto_suggest=False)
    service_context = ServiceContext.from_defaults(llm=OpenAI(model='gpt-3.5-turbo', temperature=0.5, system_prompt='You are an expert on Stranger Things and your job is to answer questions about Stranger Things. Assume that all questions are related to Stranger Things. Do not answer any questions unrelated to Stranger Things.  If you do not know an answer to a question, simply reply with "I do not know the answer".'))
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    #index = GPTVectorStoreIndex(docs, service_context=service_context)
    return index

index = load_data()
index.storage_context.persist('./Stranger_Things_Index')
