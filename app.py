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

        table_settings = {
            "vertical_strategy": "explicit", 
            "explicit_vertical_lines": [50, 340, 410, 490, 550],
            "horizontal_strategy": "text",
        }
        tables = page.extract_table(table_settings)
        items_raw = []

        if tables:
            for row in tables:
                if not row or len(row) < 4: continue

                desc = str(row[0])
                qty = str(row[1])
                price = str(row[2])
                total = str(row[3])

                if not qty or qty == "None" or qty == "" or "Qty" in qty:
                    continue

                item = {
                    "Description": desc,
                    "Qty": qty,
                    "Unit Price": price,
                    "Line Total": total
                }

                items_raw.append(item)
        data['line_items'] = items_raw
    
    return data

st.set_page_config(page_title="Invoice Parser", page_icon= "✨")

st.title("Invoice Parser")
st.write("Upload a pdf invoice and watch the magic happen")

uploaded_file = st.file_uploader("Upload Invoice (PDF)", type = "pdf")

if uploaded_file is not None:
    with st.spinner("Analyzing PDF..."):
        try:
            extracted_data = extract(uploaded_file)

            st.success("Extraction Complete!")
            st.divider()

            col1, col2 = st.columns(2)
            col1.metric("Invoice Number", extracted_data['invoice_number'])
            col2.metric("Total Amount", f"${float(extracted_data['total_amount']):.2f}")

            st.subheader("Line Items (Review)")
            df = pd.DataFrame(extracted_data['line_items'])
            edited_df = st.data_editor(df, num_rows="dynamic", width="stretch")

            st.divider()
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Excel/CSV", csv, "invoice_data.csv", "text/csv")

        except Exception as e:
            st.error(f"Error parsing file: {e}")