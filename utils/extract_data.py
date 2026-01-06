"""
Utility module for extracting data from electricity bills (PDF).
Extracts key information like consumer details, billing period, units consumed, and total amount.
"""

import pdfplumber
import re
from typing import Dict, Any


def extract_bill_data(pdf_file) -> Dict[str, Any]:
    """
    Extracts details from an uploaded electricity bill PDF.
    
    Args:
        pdf_file: Uploaded PDF file object from Streamlit
        
    Returns:
        Dictionary containing:
        - consumer_no: Consumer number
        - consumer_name: Name of the consumer
        - bill_month: Billing month/period
        - billing_date: Date when bill was generated
        - due_date: Payment due date
        - metered_units: Total units consumed (kWh)
        - total_amount: Total bill amount
        - previous_reading: Previous meter reading
        - current_reading: Current meter reading
    """
    
    extracted_data = {
        'consumer_no': 'N/A',
        'consumer_name': 'N/A',
        'bill_month': 'N/A',
        'billing_date': 'N/A',
        'due_date': 'N/A',
        'metered_units': 0,
        'total_amount': 0,
        'previous_reading': 0,
        'current_reading': 0
    }
    
    try:
        with pdfplumber.open(pdf_file) as pdf:
            # Extract text from all pages
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
            
            # Extract consumer number
            consumer_match = re.search(r'Consumer\s*(?:No|Number|ID)[:\s]*([A-Z0-9\-]+)', full_text, re.IGNORECASE)
            if consumer_match:
                extracted_data['consumer_no'] = consumer_match.group(1).strip()
            
            # Extract consumer name
            name_match = re.search(r'(?:Consumer\s*)?Name[:\s]*([A-Za-z\s\.]+)(?:\n|Consumer)', full_text, re.IGNORECASE)
            if name_match:
                extracted_data['consumer_name'] = name_match.group(1).strip()
            
            # Extract bill month/period
            month_match = re.search(r'(?:Bill(?:ing)?\s*(?:Period|Month|Date)|For\s*the\s*(?:month|period)\s*of)[:\s]*([A-Za-z]+\s*\d{4}|\d{1,2}/\d{4})', full_text, re.IGNORECASE)
            if month_match:
                extracted_data['bill_month'] = month_match.group(1).strip()
            
            # Extract billing date
            bill_date_match = re.search(r'Bill(?:ing)?\s*Date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', full_text, re.IGNORECASE)
            if bill_date_match:
                extracted_data['billing_date'] = bill_date_match.group(1).strip()
            
            # Extract due date
            due_date_match = re.search(r'Due\s*Date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', full_text, re.IGNORECASE)
            if due_date_match:
                extracted_data['due_date'] = due_date_match.group(1).strip()
            
            # Extract metered units (kWh)
            units_match = re.search(r'(?:Total\s*)?(?:Units?|Consumption|kWh)[:\s]*(\d+(?:\.\d+)?)', full_text, re.IGNORECASE)
            if units_match:
                extracted_data['metered_units'] = float(units_match.group(1))
            
            # Extract total amount
            amount_match = re.search(r'(?:Total\s*(?:Amount|Bill)|Amount\s*Payable|Net\s*Amount)[:\s]*(?:Rs\.?|₹|\$)?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', full_text, re.IGNORECASE)
            if amount_match:
                amount_str = amount_match.group(1).replace(',', '')
                extracted_data['total_amount'] = float(amount_str)
            
            # Extract meter readings
            prev_reading_match = re.search(r'Previous\s*Reading[:\s]*(\d+)', full_text, re.IGNORECASE)
            if prev_reading_match:
                extracted_data['previous_reading'] = int(prev_reading_match.group(1))
            
            current_reading_match = re.search(r'Current\s*Reading[:\s]*(\d+)', full_text, re.IGNORECASE)
            if current_reading_match:
                extracted_data['current_reading'] = int(current_reading_match.group(1))
            
            # If units not found but readings available, calculate
            if extracted_data['metered_units'] == 0 and extracted_data['current_reading'] > 0:
                extracted_data['metered_units'] = extracted_data['current_reading'] - extracted_data['previous_reading']
                
    except Exception as e:
        print(f"Error extracting bill data: {str(e)}")
    
    return extracted_data


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts raw text from a PDF file.
    
    Args:
        pdf_file: Uploaded PDF file object
        
    Returns:
        Extracted text as string
    """
    try:
        with pdfplumber.open(pdf_file) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
            return full_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"
