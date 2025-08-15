from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
from dotenv import load_dotenv
import os
import shutil
from typing import List
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()
openai.api_key = os.environ.get("For testing purposes you can use the OpenAI API key here")

# Paths configuration
CHROMA_PATH = "chroma"
DATA_PATH = "data/books"

def main() -> None:
    generate_data_store()

def generate_data_store() -> None:
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents() -> List[Document]:
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    logging.info(f"Loaded {len(documents)} documents from {DATA_PATH}.")
    return documents

def split_text(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    logging.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    if len(chunks) > 10:
        logging.debug(f"Sample chunk content: {chunks[10].page_content}")
        logging.debug(f"Sample chunk metadata: {chunks[10].metadata}")
    return chunks

def save_to_chroma(chunks: List[Document]) -> None:
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        logging.info(f"Removed existing Chroma database {CHROMA_PATH}.")

    # Create and persist new database
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    logging.info(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
if __name__ == "__main__":
    main()
