import streamlit as st
import pickle
import time
import os
import faiss
from langchain_openai import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Streamlit app setup
st.title("News Research Tool 📈")
st.sidebar.title("Configuration")

# User input for OpenAI API key
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# Dynamic URL fields management
if 'url_count' not in st.session_state:
    st.session_state.url_count = 3

def add_url_field():
    st.session_state.url_count += 1

def remove_url_field():
    if st.session_state.url_count > 1:  # Prevents removing all fields
        st.session_state.url_count -= 1

st.sidebar.button("Add another URL", on_click=add_url_field)
st.sidebar.button("Remove last URL", on_click=remove_url_field)

# Collect URLs from the user
urls = [st.sidebar.text_input(f"URL {i+1}", key=f"url{i}") for i in range(st.session_state.url_count)]
urls = [url for url in urls if url.strip()]  # Filter out empty URLs
process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

# Define a caching function for loading and processing URLs using the OpenAI API key
@st.cache_data(show_spinner=True)
def load_and_process(urls, api_key):
    if urls and api_key:
        loader = UnstructuredURLLoader(urls=urls)
        data = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n', '\n', '.', ','], chunk_size=1000)
        docs = text_splitter.split_documents(data)
        
        embeddings = OpenAIEmbeddings(api_key=api_key)
        vector_store = FAISS.from_documents(docs, embeddings)
        return vector_store.serialize_to_bytes()
    else:
        return None

# Process URLs if the button is clicked and API key is provided
if process_url_clicked and urls and api_key:
    main_placeholder = st.empty()
    main_placeholder.text("Processing URLs...")
    serialized_vector_store = load_and_process(urls, api_key)
    
    if serialized_vector_store:
        # Save the FAISS index to a file
        with open(file_path, "wb") as f:
            pickle.dump(serialized_vector_store, f)

        time.sleep(2)
        main_placeholder.text("URLs processed and indexed.")
    else:
        main_placeholder.text("No valid URLs to process or API key is missing.")

# Query handling
query = st.text_input("Question:")
if query:
    if os.path.exists(file_path) and api_key:
        with open(file_path, "rb") as f:
            serialized_data = pickle.load(f)
            embeddings = OpenAIEmbeddings(api_key=api_key)
            vector_store = FAISS.deserialize_from_bytes(serialized_data, embeddings)
            llm = OpenAI(temperature=0.9, max_tokens=500, api_key=api_key)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vector_store.as_retriever())
            result = chain.invoke({"question": query}, return_only_outputs=True)
            
            st.header("Answer")
            st.write(result["answer"])
            
            # Display sources if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                for source in sources.split("\n"):
                    st.write(source)
