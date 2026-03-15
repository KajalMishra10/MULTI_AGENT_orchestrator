from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

from rag.ingest_docs import load_documents

def create_vector_store():

    documents = load_documents()

    embedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vector_db = Chroma.from_documents(
        documents,
        embedding,
        persist_directory="chroma_db"
    )

    return vector_db