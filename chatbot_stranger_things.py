#streamlit listens on port 8080
#see .streamlit/config.toml
#it can't bind to port 80 as that needs root privs
#to have it listen on port 80,
#setup port forwarding from 80 to 8080
#in /etc/ufw/before.rules
#*nat
#:PREROUTING ACCEPT [0:0]
#-A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
#COMMIT

#might need this to open port 8080
#sudo ufw allow 8080/tcp

#to run do this from the command line:
#streamlit run chatbot_stranger_things.py

from llama_index import VectorStoreIndex, ServiceContext, Document, StorageContext, load_index_from_storage, SimpleDirectoryReader
from llama_index.llms import OpenAI
from PIL import Image
import streamlit as st
import openai
import os

openai.api_key = 'YOUR_KEY_HERE'
os.environ['OPENAI_API_KEY'] = 'YOUR_KEY_HERE'

st.set_page_config(page_title="Stranger Things Chatbot", layout="centered", initial_sidebar_state="auto", menu_items=None)

image = Image.open('st.png')

st.image(image)
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Stranger Things!"}
    ]

storage_context = StorageContext.from_defaults(persist_dir='./Stranger_Things_Index')
index = load_index_from_storage(storage_context)
qe = index.as_query_engine()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            #response = st.session_state.chat_engine.chat(prompt)
            response = qe.query(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
