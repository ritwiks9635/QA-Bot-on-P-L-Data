import pdfplumber
from tabula import read_pdf
import pandas as pd
import string
import logging
logging.getLogger("tabula").setLevel(logging.ERROR)



# Extract plain text using pdfplumber
def extract_text_from_pdf(pdf_path):
    text_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[1:]:
            text = page.extract_text()
            if text:
                text_data.append(text)
    return text_data


# Extract tables using Tabula with custom formatting
def extract_tables_with_tabula(pdf_path):
    tables = read_pdf(pdf_path, pages="all", multiple_tables=True, pandas_options={"header": 0})
    formatted_tables = []

    for table in tables:
        if len(table) <= 2:
            continue

        # Replace NaN with empty strings
        table = table.fillna("")

        # Remove punctuation from cell values
        table = table.map(lambda x: str(x).translate(str.maketrans("", "", string.punctuation)))

        # Join columns and rows into key-value pairs
        formatted_table = []
        headers = table.columns
        for _, row in table.iterrows():
            row_data = " | ".join(
                f"{headers[col_index]}: {str(cell)}" for col_index, cell in enumerate(row)
            )
            formatted_table.append(row_data)

        formatted_tables.append("\n".join(formatted_table))

    return formatted_tables


# Main pipeline to extract both text and formatted tables
def process_pdf(pdf_path):
    text_data = extract_text_from_pdf(pdf_path)

    formatted_tables = extract_tables_with_tabula(pdf_path)

    return text_data, formatted_tables
