import streamlit as st
import pdfplumber
import pandas as pd
import re

def extract(file):

    data = {}

    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

        inv_match = re.search(r'#INV-\d{4}-\d{3}', text)
        data['invoice_number'] = inv_match.group(0) if inv_match else "Not found"

        total_match = re.search(r'TOTAL:\s*\$([\d\.]+)', text)
        data['total_amount'] = total_match.group(1) if total_match else 0.0

        tables = page.extract_table()
        items_raw = []

        if tables:
            for row in tables:
                if not row or "Description" in row[0] or row[0] == "":
                    continue

                item = {
                    "Description" : row[0],
                    "Qty" : row[1],
                    "Unit Price" : row[2],
                    "Total" : row[3]
                }

                items_raw.append(item)
        data['line items'] = items_raw
    
    return data

st.set_page_config(page_title="vellum", page_icon= "✨")

st.title("vellum")
st.write("upload a pdf invoice and watch the magic happen")

uploaded_file = st.file_uploader("Upload Invoice (PDF)", type = "pdf")