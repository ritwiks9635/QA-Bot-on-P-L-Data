import google.generativeai as genai
from google.api_core import retry
from backend.store_embedding import index
from backend.config import GEMINI_API_KEY
from sentence_transformers import SentenceTransformer

genai.configure(api_key=GEMINI_API_KEY)
retrieval_model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_documents(query, top_k=5):
    # Generate query embedding
    query_embedding = retrieval_model.encode(query).tolist()

    # Search for the most relevant documents
    results = index.query(vector = query_embedding, top_k=top_k, include_metadata=True)

    # Extract the text from the metadata
    retrieved_texts = [match['metadata']['text'] for match in results['matches']]
    return retrieved_texts


gen_model = genai.GenerativeModel(
    'gemini-1.5-flash-latest',
    generation_config=genai.GenerationConfig(
        temperature=0.3,
        top_p=1,
        max_output_tokens=200,
    ))


def generate_answer(query, contexts):
    prompt = (
        "You are an expert financial analyst specializing in interpreting financial data and metrics from tabular and textual formats. "
        "Your task is to analyze the provided financial contexts carefully and provide a clear, concise, and well-reasoned answer to the query. "
        "If the data is insufficient to answer the query, state explicitly what is missing and why the question cannot be fully answered.\n\n"
        "### Contexts:\n"
        + "\n".join([f"Context {i+1}:\n{context}" for i, context in enumerate(contexts)]) +
        "\n\n"
        "### Query:\n"
        + query +
        "\n\n"
        "### Instructions:\n"
        "1. Summarize any relevant financial data from the provided contexts.\n"
        "2. Use logical reasoning to answer the query based on the summarized data.\n"
        "3. If the data is insufficient, explain what information is missing and why it is needed.\n\n"
        "### Answer:"
    )

    retry_policy = {
        "retry": retry.Retry(predicate=retry.if_transient_error, initial=10, multiplier=1.5, timeout=300)
    }
    response = gen_model.generate_content(
        prompt,
        request_options=retry_policy
    )
    return response.text

def generate_pipeline(query, top_k=5):
    # Step 1: Retrieve relevant contexts
    contexts = retrieve_documents(query, top_k=top_k)

    # Step 2: Generate an answer using the retrieved contexts
    answer = generate_answer(query, contexts)
    return answer
