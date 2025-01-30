import re
from typing import List

# Preprocess text data to clean, normalize and join (text, table)
def improved_preprocess_text(text):
    # Step 1: Normalize spaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    # Step 2: Normalize financial terms
    text = text.replace("₹", "INR")
    text = text.replace("crore", "cr")
    text = text.replace("lakh", "lac")

    # Step 3: Retain table-like formatting by preserving line breaks
    lines = text.split(". ")
    cleaned_lines = []
    for line in lines:
        if re.search(r'\d', line):
            cleaned_lines.append(line.strip())
        else:
            cleaned_lines.append(line.strip())

    return "\n".join(cleaned_lines)

# Combine preprocessed text and table data
def combine_text_and_table_data(preprocessed_text: List[str], formatted_tables: List[str]):
    combined_output = []

    for page_num, page_text in enumerate(preprocessed_text, start=1):
        combined_output.append(f"Page {page_num}:")
        combined_output.append(page_text)

        # If tables exist for this page, append them
        if page_num <= len(formatted_tables):
            combined_output.append("Tables:")
            combined_output.append(formatted_tables[page_num - 1])

    return "\n\n".join(combined_output)

def preprocess_data(text_output, table_output):
    # Preprocess the text data
    preprocessed_text = [improved_preprocess_text(page_text) for page_text in text_output]

    # Combine preprocessed text and table data
    final_output = combine_text_and_table_data(preprocessed_text, table_output)

    pages = final_output.split("\n\nPage ")

    # Check "Page X:" is preserved
    pages = [f"Page {page}" if not page.startswith("Page") else page for page in pages]
    return pages
