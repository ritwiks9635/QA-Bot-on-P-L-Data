from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, INDEX_NAME

pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
index = pc.Index(INDEX_NAME)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")



def chunk_with_langchain(text, chunk_size=8000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = text_splitter.split_text(text)

    return chunks



def generate_embeddings(chunked_data):
    embeddings = []
    for page_chunks in chunked_data:
        page_embeddings = embed_model.encode(page_chunks, convert_to_tensor=True)
        embeddings.append(page_embeddings)
    return embeddings



def upsert_embeddings(embeddings, chunked_data):
    for page_num, page_embeddings in enumerate(embeddings):
        for chunk_num, embedding in enumerate(page_embeddings):
            metadata = {
                "page": page_num + 1,
                "chunk": chunk_num,
                "text": chunked_data[page_num][chunk_num],
            }
            # Generate unique ID for each embedding
            unique_id = f"page-{page_num+1}-chunk-{chunk_num}"
            embedding_list = embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
            index.upsert([(unique_id, embedding_list, metadata)])
