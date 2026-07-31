"""
Utility module for extracting bill data from multiple input sources:
PDF, scanned image (OCR), CSV, and manual entry.

All four public extraction functions return the same contract:

{
    "consumer_no": str,        # "N/A" if unknown
    "consumer_name": str,      # "N/A" if unknown
    "bill_month": str,         # "N/A" if unknown
    "billing_date": str,       # "N/A" if unknown
    "due_date": str,           # "N/A" if unknown
    "metered_units": float,    # 0 if unknown
    "total_amount": float,     # 0 if unknown
    "previous_reading": float, # 0 if unknown
    "current_reading": float,  # 0 if unknown
}

No database logic. No UI logic. No appliance logic.
"""

import csv
import io
import re
from typing import Dict, Any

import pdfplumber



DEFAULT_BILL_DATA: Dict[str, Any] = {
    "consumer_no": "N/A",
    "consumer_name": "N/A",
    "bill_month": "N/A",
    "billing_date": "N/A",
    "due_date": "N/A",
    "metered_units": 0,
    "total_amount": 0,
    "previous_reading": 0,
    "current_reading": 0,
}

TEXT_FIELDS = ["consumer_no", "consumer_name", "bill_month", "billing_date", "due_date"]
NUMERIC_FIELDS = ["metered_units", "total_amount", "previous_reading", "current_reading"]

CSV_EXPECTED_COLUMNS = TEXT_FIELDS + NUMERIC_FIELDS


# --------------------------------------------------
# Shared: text parsing (used by PDF + OCR)
# --------------------------------------------------

CONSUMER_NO_PATTERNS = [

    r'Consumer\s*(?:No|Number|ID)\.?\s*[:\-]?\s*([A-Z0-9\-]+)',

    r'ConsumerNo\.\s*([A-Z0-9\-]+)',

    r'Account\s*Number\s*[:\-]?\s*([A-Z0-9\-]+)',

    r'Service\s*Number\s*[:\-]?\s*([A-Z0-9\-]+)',

]


def _find_first_match(
    patterns: list[str],
    text: str
) -> str | None:
    """
    Searches the text using multiple regex patterns and
    returns the first matched value.

    Args:
        patterns:
            List of regex patterns.

        text:
            Extracted bill text.

    Returns:
        First matched value, or None if no pattern matches.
    """

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return None


def _parse_bill_text(text: str) -> Dict[str, Any]:
    """
    Runs the field-extraction regexes against text extracted from a PDF electricity bill.

    Returns only the fields that were actually found.
    """

    raw: Dict[str, Any] = {}

    consumer_no = _find_first_match(
    CONSUMER_NO_PATTERNS,
    text
    )

    if consumer_no:

        raw["consumer_no"] = consumer_no

    # Standard formats:
    # Consumer Name:
    # Name:
    name_match = re.search(
        r'Mr\./Ms\.?([A-Z\-]+?)\s+MeterserialNo',
        text,
        re.IGNORECASE
    )

    if name_match:
        raw["consumer_name"] = name_match.group(1).strip()

    
    if "consumer_name" not in raw:

        name_match = re.search(
            r'Mr\./Ms\.?\s*([A-Z\s]+?)\s+MeterserialNo',
            text,
            re.IGNORECASE
        )

        if name_match:
            name = (
                name_match.group(1)
                .replace("-", " ")
                .strip()
            )

            # Remove common prefixes
            name = re.sub(
                r"^(SH|SMT|MR|MRS|MS)\s*",
                "",
                name,
                flags=re.IGNORECASE
            )

            raw["consumer_name"] = name.title()
            
        

    month_match = re.search(
        r'(?:Bill(?:ing)?\s*(?:Period|Month|Date)|For\s*the\s*(?:month|period)\s*of)'
        r'[:\s]*([A-Za-z]{3,9}[-\s]?\d{4}|\d{1,2}/\d{4})',
        text,
        re.IGNORECASE
    )
    if month_match:
        raw["bill_month"] = month_match.group(1).strip()

    bill_date_match = re.search(
        r'Bill(?:ing)?\s*Date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE
    )
    if bill_date_match:
        raw["billing_date"] = bill_date_match.group(1).strip()

    due_date_match = re.search(
        r'Due\s*Date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE
    )
    if due_date_match:
        raw["due_date"] = due_date_match.group(1).strip()

    units_match = re.search(
        r'(?:Total\s*)?(?:Units?|Consumption|kWh)[:\s]*(\d+(?:\.\d+)?)', text, re.IGNORECASE
    )
    if units_match:
        raw["metered_units"] = units_match.group(1)


    amount_patterns = [
        r'TotalAmountPayable(?:TillDueDate|AfterDueDate)?[:\s]*INR\s*(\d+(?:\.\d+)?)',
        r'CurrentMonthBillAmount[:\s]*(\d+(?:\.\d+)?)',
        r'TotalAmountPayable[:\s]*(\d+(?:\.\d+)?)',
        r'(?:Total\s*(?:Amount|Bill)|Amount\s*Payable|Net\s*Amount)'
        r'[:\s]*(?:Rs\.?|₹|\$|INR)?\s*(\d+(?:,\d{3})*(?:\.\d+)?)'
    ]

    for pattern in amount_patterns:
        amount_match = re.search(pattern, text, re.IGNORECASE)
        if amount_match:
            raw["total_amount"] = amount_match.group(1).replace(",", "")
            break
    if amount_match:
        raw["total_amount"] = amount_match.group(1).replace(",", "")

        prev_reading_match = re.search(
            r'Previous\s*Reading[:\s]*(\d+)',
            text,
            re.IGNORECASE
        )

        if prev_reading_match:
            raw["previous_reading"] = prev_reading_match.group(1)

        current_reading_match = re.search(
            r'Current\s*Reading[:\s]*(\d+)',
            text,
            re.IGNORECASE
        )

        if current_reading_match:
            raw["current_reading"] = current_reading_match.group(1)
        

        if "total_amount" not in raw:

            amount = re.search(
                r'Current\s*Month\s*Bill\s*Amount[^0-9]*(\d+\.\d+)',
                text,
                re.IGNORECASE
            )

            if amount:
                raw["total_amount"] = amount.group(1)

    return raw


# --------------------------------------------------
# Shared: normalization + validation (used by all 4 paths)
# --------------------------------------------------

def _normalize_extracted_fields(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Single source of truth for turning partial/raw field data into
    the final bill data contract. Handles defaulting, type coercion,
    and validation in one place so all four input paths behave
    identically.

    Raises ValueError on invalid (not missing) data — a present but
    unparseable or negative value is a real error, not something to
    silently default away.
    """

    result = dict(DEFAULT_BILL_DATA)

    for field in TEXT_FIELDS:
        value = raw.get(field)
        if value is not None and str(value).strip():
            result[field] = str(value).strip()

    for field in NUMERIC_FIELDS:
        value = raw.get(field)

        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue

        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid numeric value for '{field}': {value!r}")

        if number < 0:
            raise ValueError(f"'{field}' cannot be negative: {number}")

        result[field] = number

    # Derive metered_units from readings if not otherwise provided
    if (
        result["metered_units"] == 0
        and result["current_reading"] > 0
        and result["current_reading"] >= result["previous_reading"]
    ):
        result["metered_units"] = result["current_reading"] - result["previous_reading"]

    if (
        result["previous_reading"] > 0
        and result["current_reading"] > 0
        and result["current_reading"] < result["previous_reading"]
    ):
        raise ValueError("current_reading cannot be less than previous_reading")

    return result


# --------------------------------------------------
# Path 1: PDF
# --------------------------------------------------

def extract_bill_data(pdf_file) -> Dict[str, Any]:
    """
    Extracts bill data from an uploaded PDF.

    Strategy:

    1. Extract raw text using pdfplumber
    2. Run normal regex extraction
    3. If important fields are missing, use fallback parsing
       for table-based electricity bills.
    4. Normalize and validate.
    """

    try:
        with pdfplumber.open(pdf_file) as pdf:

            full_text = ""

            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    full_text += page_text + "\n"

    except Exception as error:
        raise ValueError(
            f"Unable to read PDF file: {error}"
        ) from error

    if not full_text.strip():
        raise ValueError(
            "No extractable text found in PDF "
            "(it may be scanned, empty, or password-protected)."
        )

    # --------------------------------------------------
    # Normal regex extraction
    # --------------------------------------------------

    raw = _parse_bill_text(full_text)

    # --------------------------------------------------
    # Fallback 1
    # MPPKVVCL-style Reading Detail table
    #
    # Example:
    #
    # 52284.00 08-07-2025 51863.00 1 421.00 0.00 421.00 13.58
    #
    # current reading
    # reading date
    # previous reading
    # MF
    # metered units
    # assessed units
    # final units
    # average/day
    # --------------------------------------------------

    if (
        "metered_units" not in raw
        or float(raw.get("metered_units", 0)) == 0
    ):

        table_match = re.search(
            r"(\d+\.\d+)\s+"
            r"\d{2}-\d{2}-\d{4}\s+"
            r"(\d+\.\d+)\s+"
            r"\d+\s+"
            r"(\d+\.\d+)\s+"
            r"\d+\.\d+\s+"
            r"\d+\.\d+\s+"
            r"\d+\.\d+",
            full_text
        )

        if table_match:

            raw["current_reading"] = table_match.group(1)

            raw["previous_reading"] = table_match.group(2)

            raw["metered_units"] = table_match.group(3)

    # --------------------------------------------------
    # Fallback 2
    # Consumer Name
    # --------------------------------------------------

    if "consumer_name" not in raw:

        name_match = re.search(
            r"Mr\./Ms\.?\s*([A-Z][A-Z\s]+)",
            full_text,
            re.IGNORECASE
        )

        if name_match:

            raw["consumer_name"] = (
                name_match.group(1)
                .replace("-", " ")
                .title()
                .strip()
            )

    # --------------------------------------------------
    # Fallback 3
    # Bill Month
    # --------------------------------------------------

    if "bill_month" not in raw:

        month_match = re.search(
            r"BillMonth[:\s]*([A-Z]{3}-\d{4})",
            full_text,
            re.IGNORECASE
        )

        if month_match:

            raw["bill_month"] = month_match.group(1)

    # --------------------------------------------------
    # Normalize
    # --------------------------------------------------

    return _normalize_extracted_fields(raw)


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts raw text from a PDF file.
    Debugging helper.
    """

    try:

        with pdfplumber.open(pdf_file) as pdf:

            full_text = ""

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    full_text += page_text + "\n"

        return full_text

    except Exception as error:

        return f"Error extracting text: {error}"


# --------------------------------------------------
# Path 2: CSV import
# --------------------------------------------------

def extract_bill_data_from_csv(csv_file) -> Dict[str, Any]:
    """
    Extracts bill data from a single-row CSV.

    Expected header columns (any subset is fine, missing columns
    just default per the contract):
    consumer_no, consumer_name, bill_month, billing_date, due_date,
    metered_units, total_amount, previous_reading, current_reading
    """

    content = csv_file.read()
    if isinstance(content, bytes):
        content = content.decode("utf-8")

    reader = csv.DictReader(io.StringIO(content))
    row = next(reader, None)

    if row is None:
        raise ValueError("CSV file is empty or missing a data row.")

    raw = {field: row.get(field) for field in CSV_EXPECTED_COLUMNS}

    return _normalize_extracted_fields(raw)


# --------------------------------------------------
# Path 3: Manual entry
# --------------------------------------------------

def build_manual_bill_data(fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Builds bill data from manually entered fields (e.g. a Streamlit form).
    """

    return _normalize_extracted_fields(fields)