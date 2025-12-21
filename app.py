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