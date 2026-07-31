import pdfplumber

with pdfplumber.open("../electricity_bill.pdf") as pdf:  # adjust path to wherever you saved the uploaded PDF
    for page in pdf.pages:
        text = page.extract_text()
        print(repr(text))