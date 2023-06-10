import streamlit as st
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

from audio_utils import convert_audio_to_text
from file_knowledge import FileKnowledge

def main():
    load_dotenv()
    st.set_page_config(page_title="Journalist's Toolbox", page_icon=":smiley:")
    st.write("Upload your PDF file or audio file")

    st.title("Journalist's Toolbox")
    session = initialize_session_state()

    initialize_sidebar(session)

    splitter = get_splitter()

    col0, col1 = st.columns([1, 1])

    if not st.session_state["knowledge"]:
        st.write("No knowledge found")
        return

    user_question = st.text_input("Ask a question", key="user_question")

    if user_question:
        generate_response(user_question)

    if show_all_konwledge:
        show_all_konwledge()

def show_all_konwledge():

    if hasattr(st.session_state, 'hide_all_konwledge') and st.session_state.hide_all_konwledge:
        return

    if st.session_state.show_all_konwledge:
        hide_all_konwledge = st.button("Hide all knowledge", key="hide_all_konwledge")
        st.header("All knowledge")
    
        
        for file_knowledge in st.session_state["knowledge"].values():
            #list all the files with name and a link to download the text
            col0, col1 = st.columns(2)
            with col0:
                st.write(file_knowledge.name)
            with col1:
                st.download_button(f'Download text', file_knowledge.content)


def initialize_session_state():
    if not hasattr(st.session_state, "knowledge"):
        st.session_state["knowledge"] = {}
    
    return st.session_state["knowledge"]

def initialize_sidebar(session):
    with st.sidebar:
        show_all_konwledge = st.button("Show all knowledge", key="show_all_konwledge")
        with st.expander("Upload files"):
            process_files("pdf", get_splitter(), session)
            process_files("m4a", get_splitter(), session)

        st.header("Journalist toolbox")
        st.write("Upload your PDF file or audio file")
        st.write("Then ask a question and get an answer")
        st.write("You can also download the text of the uploaded files")
        st.divider()
        
        st.slider("Temperature", min_value=0.0, max_value=1.0, step=0.01, value=0.0, key="temperature")


def get_splitter():
    return CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

def process_files(file_type, splitter, session):
    files = st.file_uploader(f"Upload your {file_type} file", type=[file_type], accept_multiple_files=True)
    for file in files:
        if file.name not in st.session_state["knowledge"].keys():
            file_knowledge = FileKnowledge(name=file.name, file=file, filetype=file_type, splitter=splitter)
            session[file.name] = file_knowledge

            add_document_to_vector_store(file_knowledge)

def get_vector_store():
    if not hasattr(st.session_state, "vector_store"):
        raise ValueError("No vector store found")

    return st.session_state["vector_store"]

def initialize_vector_store(file_knowledge):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    chunks = file_knowledge.chunks
    vector_store = FAISS.from_texts(chunks, embeddings)
    st.session_state["vector_store"] = vector_store

    return vector_store

def add_document_to_vector_store(file_knowledge):
    if not hasattr(st.session_state, "vector_store"):
        return initialize_vector_store(file_knowledge)

    vector_store = st.session_state["vector_store"]
    chunks = file_knowledge.chunks
    vector_store.add_texts(chunks)

def generate_response(user_question):
    if user_question:
        respond_to_question(get_vector_store(), user_question)


def respond_to_question(vector_store, user_question):
    """
    Respond to a question using the vector store and the LLM
    """
    docs = vector_store.similarity_search(user_question, top_k=5)
    if docs is None:
        st.write("No results found")
        return

    # llm = OpenAI()
    temperature = st.session_state.temperature or 0.0
    st.write(f"Temperature: {temperature}")
    llm = OpenAI(temperature=temperature, model_name="gpt-3.5-turbo")
    chain = load_qa_chain(llm, chain_type="stuff")

    response = chain.run(input_documents=docs, question=user_question)
    st.write(response)
    st.write("Sources:")
    # print the sources of the answer as collapsible text
    st.write(docs)

import base64

def create_download_link(text: str, filename: str):
    """Generates a link allowing the text to be downloaded"""
    b64 = base64.b64encode(text.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}.txt">Download text file</a>'

if __name__ == "__main__":
    main()
