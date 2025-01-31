import gradio as gr
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from backend.process_pdf import process_pdf
from backend.preprocessing_data import preprocess_data
from backend.store_embedding import chunk_with_langchain, generate_embeddings, upsert_embeddings
from backend.query_pipeline import generate_pipeline


def qa_bot_interface(pdf_file, query):
    """
    Handles user interaction with the QA bot.

    Args:
    - pdf_file (UploadedFile): The uploaded PDF file.
    - query (str): The financial query entered by the user.

    Returns:
    - str: Retrieved data (contexts).
    - str: Generated answer.
    """
    if pdf_file is None:
        return "No PDF uploaded.", "Please upload a PDF to start."

    if not query:
        return "No query provided.", "Please enter a query to get an answer."

    # Step 1: Extract text and table data from the PDF
    text_data, table_data = process_pdf(pdf_file.name)

    # Step 2: Preprocess the extracted data
    preprocessed_data = preprocess_data(text_data, table_data)

    # Step 3: Chunk the data
    chunked_data = [chunk_with_langchain(page) for page in preprocessed_data]

    # Step 4: Generate and store embeddings
    embeddings = generate_embeddings(chunked_data)
    upsert_embeddings(embeddings, chunked_data)

    # Step 5: Retrieve relevant documents and generate answer
    answer = generate_pipeline(query)

    # Return retrieved data and the final answer
    return answer


# Build the Gradio interface
with gr.Blocks() as interface:
    gr.Markdown("# 📊 Financial Data QA Bot")
    gr.Markdown(
        "Upload a PDF containing financial data (e.g., P&L tables) and ask questions about the data."
    )

    # File upload
    with gr.Row():
        pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])

    # Query input
    query_input = gr.Textbox(label="Enter your financial query", placeholder="e.g., What are the total expenses for Q2 2023?")

    # Output areas
    with gr.Row():
        #retrieved_data_output = gr.Textbox(label="Retrieved Financial Data", lines=10, interactive=False)
        answer_output = gr.Textbox(label="Generated Answer", lines=5, interactive=False)

    # Submit button
    submit_button = gr.Button("Submit")

    # Link the interface with the function
    submit_button.click(
        fn=qa_bot_interface,
        inputs=[pdf_input, query_input],
        outputs=[answer_output],
    )

# Launch the interface
interface.launch()