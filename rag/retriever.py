from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_retriever():

    embedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vector_db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding
    )

    retriever = vector_db.as_retriever()

    return retriever