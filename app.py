"""Interactive chat application with RAG.
"""

import logging
from logging import getLogger
import streamlit as st
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

ROLE_USER = 'user'
ROLE_BOT = 'assistant'

log = getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


def get_splits(url):
    """Load a webpage, returning splits based on a certain chunk size and overlap.
    """
    loader = WebBaseLoader(url)
    loaded_doc = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=10)
    return text_splitter.split_documents(loaded_doc)


def ingest_context(data_splits):
    """Ingest and index a context into the LLM, returning a retriever.
    """
    embeddings = OllamaEmbeddings(model='llama3')
    vectorstore = Chroma.from_documents(
        documents=data_splits, embedding=embeddings)
    return vectorstore.as_retriever()


def show_message(role, message_to_show):
    """Show a message in the chat panel.
    """
    with st.chat_message(role):
        st.markdown(message_to_show)

    st.session_state.messages.append(
        {'role': role, 'content': message_to_show})


def call_llm(question_to_ask, context):
    """Starts the chat with the LLM using the provided question and context.
    """

    prompt = f"Question {question_to_ask}\n\nContext: {context}"

    log.info('Prompt: %s', prompt)

    response_from_llm = ollama.chat(model='llama3', messages=[
        {'role': ROLE_USER, 'content': prompt}])

    log.info('Response: %s', response_from_llm)

    return response_from_llm['message']['content']


def combine_docs(docs):
    """Combine documents in a single string.
    """
    return '\n\n'.join(doc.page_content for doc in docs)


def chat(prompt, context_retriever):
    """Executes a chat question using the provided context.
    """
    retrieved_docs = context_retriever.invoke(prompt)
    context = combine_docs(retrieved_docs)
    return call_llm(question, context)


# Creates the chat webpage.
st.title('Interactive chat with context')
st.caption(
    'This page retrieve the contents of a webpage to use it as context '
    'when asking questions to a chatbot.')

# Gets a webpage to retrieve contents for augmented generation.
webpage_url = st.text_input(
    'Enter the URL of a webpage you want to ask questions about', type='default')

log.info('Check URL')

if webpage_url:
    log.info('Loading %s', webpage_url)

    # Only create the context if it's not in the session.
    if webpage_url not in st.session_state:
        webpage_splits = get_splits(webpage_url)
        retriever = ingest_context(webpage_splits)

        st.session_state[webpage_url] = retriever
        log.info('Context created')

    st.success(f"{webpage_url} loaded.")

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun.
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    log.info('Messages loaded')

    if question := st.chat_input('Ask any questions about the webpage'):
        log.info('Question asked')

        show_message(ROLE_USER, question)

        retriever = st.session_state[webpage_url]
        response = chat(question, retriever)
        show_message(ROLE_BOT, response)
