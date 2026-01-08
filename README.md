## Tech Stack

* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **Data Processing:** Pandas
* **PDF Parsing:** PDFPlumber
* **Pattern Matching:** RegEx

## How It Works

1.  The app accepts a PDF file and reads the text stream.
2.  Instead of using hard-coded coordinates (which break if a vendor changes their logo size), the script searches for the "Description" table header.
3.  The page is dynamically cropped to start exactly at the table header, eliminating false positives from the top-of-page metadata.
4.  PDFPlumber analyzes the "gutters" (whitespace) in the cropped area to define column boundaries.
5.  A cleaning loop iterates through the rows, discarding any line items that lack a valid quantity or price.

## Installation & Usage

To run this project:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/spencerkrafczek/invoice-parser.git](https://github.com/spencerkrafczek/invoice-parser.git)
    cd invoice-parser
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install streamlit pandas pdfplumber
    ```

4.  **Run the App**
    ```bash
    python -m streamlit run app.py
    ```
