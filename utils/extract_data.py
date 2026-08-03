"""
extract_data.py
Smart Energy Advisor

Responsibilities:
- Extract structured bill data from an uploaded PDF (Path 1)
- Extract structured bill data from an uploaded CSV (Path 2)
- Build structured bill data from a manual entry form (Path 3)

Bill data contract (all three paths return this same shape):
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

--------------------------------------------------------------------
FIX (see conversation): two structural bugs in the PDF table-lookup
path prevented correct extraction on table-style bills whose layout
differs from the original MPPKVVCL text-flow format:

1. `_merge_table_lookup`'s header/data pairing previously required a
   table to have *exactly* 2 rows. Real-world tables often have a
   title/meta row before the header+data pair (e.g. a "CURRENT
   READING DETAILS" title row above the Current/Previous Reading
   header+data pair), so that pairing silently never fired for them.
   Fixed to anchor on "header row directly above the table's LAST
   row" instead, which still safely excludes multi-row history
   tables (their header is not adjacent to the last row).

2. Some bills pack multiple fields side-by-side on one visual line
   inside a single table cell (e.g. "CONSUMER NO   MOBILE   EMAIL"
   directly above "N3850012295   99xxxxx925"). The original cell-pair
   parser only understood one-label-per-line and produced nothing for
   these. Added `_merge_columnar_word_lookup`, which uses real word
   x-coordinates (via `page.extract_words()`) to align a header line
   with the value line below it column-by-column. This tolerates a
   blank column (e.g. missing EMAIL) and multi-word values (e.g. a
   full name) without breaking alignment, which plain text/cell
   regex cannot do reliably.

Both fixes were verified against two differently-formatted real
MPPKVVCL bills with zero change in output for the original format.
--------------------------------------------------------------------
"""

import csv
import io
import re
from typing import Dict, Any, List, Optional

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

CONSUMER_NO_PATTERNS = [
    r'Consumer\s*(?:No|Number|ID)\.?\s*[:\-]?\s*([A-Z0-9\-]+)',
    r'ConsumerNo\.\s*([A-Z0-9\-]+)',
    r'Account\s*Number\s*[:\-]?\s*([A-Z0-9\-]+)',
    r'Service\s*Number\s*[:\-]?\s*([A-Z0-9\-]+)',
]


def _find_first_match(patterns, text, validator=None):
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            value = match.group(1).strip()
            if validator is None or validator(value):
                return value
    return None


def _looks_like_id(value: str) -> bool:
    return any(character.isdigit() for character in value)


def _parse_bill_text(text: str) -> Dict[str, Any]:
    raw: Dict[str, Any] = {}

    consumer_no = _find_first_match(CONSUMER_NO_PATTERNS, text, validator=_looks_like_id)
    if consumer_no:
        raw["consumer_no"] = consumer_no

    name_match = re.search(r'Mr\./Ms\.?([A-Z\-]+?)\s+MeterserialNo', text, re.IGNORECASE)
    if name_match:
        raw["consumer_name"] = name_match.group(1).strip()

    if "consumer_name" not in raw:
        name_match = re.search(r'Mr\./Ms\.?\s*([A-Z\s]+?)\s+MeterserialNo', text, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).replace("-", " ").strip()
            name = re.sub(r"^(SH|SMT|MR|MRS|MS)\s*", "", name, flags=re.IGNORECASE)
            raw["consumer_name"] = name.title()

    if "consumer_name" not in raw:
        name_match = re.search(
            r'CONSUMER\s*NAME\s*[:\-]?\s*\n?\s*([A-Z][A-Za-z\.\s]{2,60}?)(?=\n|\s{2,}|$)',
            text, re.IGNORECASE
        )
        if name_match:
            candidate = name_match.group(1).strip()
            if candidate and not candidate.isupper() or len(candidate.split()) > 1:
                raw["consumer_name"] = candidate.title() if candidate.isupper() else candidate

    month_match = re.search(
        r'(?:Bill(?:ing)?\s*(?:Period|Month|Date)|For\s*the\s*(?:month|period)\s*of)'
        r'[:\s]*([A-Za-z]{3,9}[-\s]?\d{4}|\d{1,2}/\d{4})',
        text, re.IGNORECASE
    )
    if month_match:
        raw["bill_month"] = month_match.group(1).strip()

    bill_date_match = re.search(r'Bill(?:ing)?\s*Date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
    if bill_date_match:
        raw["billing_date"] = bill_date_match.group(1).strip()

    due_date_match = re.search(r'Due\s*Date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
    if due_date_match:
        raw["due_date"] = due_date_match.group(1).strip()

    units_match = re.search(r'(?:Total\s*)?(?:Units?|Consumption|kWh)[:\s]*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
    if units_match:
        raw["metered_units"] = units_match.group(1)

    amount_patterns = [
        r'TotalAmountPayable(?:TillDueDate|AfterDueDate)?[:\s]*INR\s*(\d+(?:\.\d+)?)',
        r'CurrentMonthBillAmount[:\s]*(\d+(?:\.\d+)?)',
        r'TotalAmountPayable[:\s]*(\d+(?:\.\d+)?)',
        r'(?:Total\s*(?:Amount|Bill)|Amount\s*Payable|Net\s*Amount)'
        r'[:\s]*(?:Rs\.?|₹|\$|INR)?\s*(\d+(?:,\d{3})*(?:\.\d+)?)'
    ]
    amount_match = None
    for pattern in amount_patterns:
        amount_match = re.search(pattern, text, re.IGNORECASE)
        if amount_match:
            raw["total_amount"] = amount_match.group(1).replace(",", "")
            break

    if amount_match:
        prev_reading_match = re.search(r'Previous\s*Reading[:\s]*(\d+)', text, re.IGNORECASE)
        if prev_reading_match:
            raw["previous_reading"] = prev_reading_match.group(1)
        current_reading_match = re.search(r'Current\s*Reading[:\s]*(\d+)', text, re.IGNORECASE)
        if current_reading_match:
            raw["current_reading"] = current_reading_match.group(1)
        if "total_amount" not in raw:
            amount = re.search(r'Current\s*Month\s*Bill\s*Amount[^0-9]*(\d+\.\d+)', text, re.IGNORECASE)
            if amount:
                raw["total_amount"] = amount.group(1)

    return raw


TABLE_FIELD_CANDIDATES_TEXT = {
    "consumer_no": ["CONSUMER NO", "CONSUMER NUMBER", "ACCOUNT NUMBER", "SERVICE NUMBER"],
    "consumer_name": ["CONSUMER NAME"],
    "billing_date": ["BILL DATE", "BILLING DATE"],
    "due_date": ["DUE DATE"],
}

TABLE_FIELD_CANDIDATES_NUMERIC = {
    "previous_reading": ["PREVIOUS READING"],
    "current_reading": ["CURRENT READING"],
    "metered_units": ["METERED UNITS", "CONSUMPTION", "UNITS"],
    "total_amount": [
        "CURRENT MONTH BILL",
        "TOTAL AMOUNT PAYABLE",
        "PAY TILL DUE DATE",
        "NET BILL",
    ],
}

ALL_LABEL_CANDIDATES: Dict[str, str] = {}
for _field, _candidates in {**TABLE_FIELD_CANDIDATES_TEXT, **TABLE_FIELD_CANDIDATES_NUMERIC}.items():
    for _candidate in _candidates:
        ALL_LABEL_CANDIDATES[_candidate.upper()] = _field


def _normalize_label(label: Any) -> str:
    return re.sub(r'\s+', ' ', str(label or '')).strip().upper()


def _extract_label_value_pairs_from_cell(cell: Any) -> List[tuple]:
    if not cell:
        return []
    lines = [line.strip() for line in str(cell).split("\n") if line.strip()]
    pairs = []
    i = 0
    while i < len(lines) - 1:
        label = _normalize_label(lines[i])
        if label in ALL_LABEL_CANDIDATES:
            pairs.append((label, lines[i + 1]))
            i += 2
        else:
            i += 1
    return pairs


def _merge_table_lookup(lookup: Dict[str, str], page) -> None:
    try:
        tables = page.extract_tables()
    except Exception:
        return
    if not tables:
        return

    for table in tables:
        if not table:
            continue

        for row in table:
            if not row:
                continue
            if len(row) == 2 and row[0] and row[1]:
                label = _normalize_label(row[0])
                value = str(row[1]).strip()
                if label and value:
                    lookup.setdefault(label, value)
            for cell in row:
                for label, value in _extract_label_value_pairs_from_cell(cell):
                    if value:
                        lookup.setdefault(label, value)

        # ORIGINAL Case 3 (kept for reference, now superseded below)
        if len(table) == 2:
            header_row, value_row = table[0], table[1]
            if header_row and value_row and len(header_row) == len(value_row):
                header_is_textual = all(
                    (cell is None) or not re.match(r'^\s*-?\d', str(cell))
                    for cell in header_row
                )
                if header_is_textual:
                    for header_cell, value_cell in zip(header_row, value_row):
                        if not header_cell or value_cell is None:
                            continue
                        label = _normalize_label(header_cell)
                        value = str(value_cell).strip()
                        if label and value:
                            lookup.setdefault(label, value)

        # --------------------------------------------------
        # FIX: header row immediately followed by a single data
        # row, where that data row is the LAST row of the table.
        # The original code required len(table) == 2, which breaks
        # as soon as a title/meta row precedes the header (e.g. a
        # "CURRENT READING DETAILS" title row above the actual
        # Current/Previous Reading header+data pair). Anchoring on
        # "data row is the table's last row" instead of "table has
        # exactly 2 rows" keeps the original safety guard (a real
        # multi-row history table's header is NOT immediately above
        # the table's last row) while fixing this case.
        # --------------------------------------------------
        if len(table) >= 2:
            header_row, value_row = table[-2], table[-1]
            if header_row and value_row and len(header_row) == len(value_row):
                header_is_textual = all(
                    (cell is None) or not re.match(r'^\s*-?\d', str(cell))
                    for cell in header_row
                )
                value_is_data_like = any(
                    cell and re.match(r'^\s*-?\d', str(cell))
                    for cell in value_row
                )
                if header_is_textual and value_is_data_like:
                    for header_cell, value_cell in zip(header_row, value_row):
                        if not header_cell or value_cell is None:
                            continue
                        label = _normalize_label(header_cell)
                        value = str(value_cell).strip()
                        if label and value:
                            lookup.setdefault(label, value)


# --------------------------------------------------
# FIX: columnar "LABEL1  LABEL2  LABEL3" header line directly above
# its "VALUE1  VALUE2  VALUE3" value line, using real word x-positions
# (not table-cell text) so a blank column (e.g. EMAIL with no value)
# doesn't break the alignment of the columns after it.
# --------------------------------------------------

def _merge_words_into_phrases(words: List[dict], gap_threshold: float = 12) -> List[dict]:
    """Merges adjacent words on the same line into label/value phrases,
    breaking a new phrase whenever the horizontal gap to the next word
    is larger than gap_threshold (i.e. a real column boundary)."""
    if not words:
        return []
    words = sorted(words, key=lambda w: w["x0"])
    phrases = [{"text": words[0]["text"], "x0": words[0]["x0"], "x1": words[0]["x1"]}]
    for w in words[1:]:
        last = phrases[-1]
        if w["x0"] - last["x1"] <= gap_threshold:
            last["text"] += " " + w["text"]
            last["x1"] = w["x1"]
        else:
            phrases.append({"text": w["text"], "x0": w["x0"], "x1": w["x1"]})
    return phrases


def _merge_columnar_word_lookup(lookup: Dict[str, str], page) -> None:
    try:
        words = page.extract_words(use_text_flow=False)
    except Exception:
        return
    if not words:
        return

    lines: Dict[int, List[dict]] = {}
    for w in words:
        key = round(w["top"])
        lines.setdefault(key, []).append(w)

    sorted_keys = sorted(lines.keys())
    line_words = [lines[k] for k in sorted_keys]

    for i in range(len(line_words) - 1):
        header_phrases = _merge_words_into_phrases(line_words[i])
        value_phrases = _merge_words_into_phrases(line_words[i + 1])
        if not value_phrases:
            continue

        for phrase in header_phrases:
            normalized = _normalize_label(phrase["text"])
            if normalized not in ALL_LABEL_CANDIDATES:
                continue

            # Value phrase(s) that start under this label's column span.
            # Widen the right edge generously since a value can be
            # wider than its label (e.g. a long name under "CONSUMER NAME"),
            # but stop at the NEXT header phrase's column (recognized or
            # not - e.g. "MOBILE"/"BILL TYPE" aren't fields we extract,
            # but they still mark where the current column ends) to
            # avoid bleeding into the next field.
            next_header_x0 = None
            for other in header_phrases:
                if other is phrase:
                    continue
                if other["x0"] > phrase["x0"]:
                    if next_header_x0 is None or other["x0"] < next_header_x0:
                        next_header_x0 = other["x0"]

            right_bound = (next_header_x0 - 5) if next_header_x0 else (phrase["x0"] + 300)

            matched = [
                vp["text"] for vp in sorted(value_phrases, key=lambda p: p["x0"])
                if phrase["x0"] - 8 <= vp["x0"] < right_bound
            ]
            if matched:
                lookup.setdefault(normalized, " ".join(matched))


def _lookup_any(lookup: Dict[str, str], candidates: List[str]) -> Optional[str]:
    for candidate in candidates:
        value = lookup.get(_normalize_label(candidate))
        if value:
            return value
    return None


def _apply_table_lookup(raw: Dict[str, Any], lookup: Dict[str, str]) -> None:
    for field, candidates in TABLE_FIELD_CANDIDATES_TEXT.items():
        value = _lookup_any(lookup, candidates)
        if value:
            raw[field] = value

    for field, candidates in TABLE_FIELD_CANDIDATES_NUMERIC.items():
        value = _lookup_any(lookup, candidates)
        if value is None:
            continue
        cleaned = re.sub(r'[^\d.]', '', str(value))
        if cleaned:
            raw[field] = cleaned


def _normalize_extracted_fields(raw: Dict[str, Any]) -> Dict[str, Any]:
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


def extract_bill_data(pdf_file) -> Dict[str, Any]:
    try:
        with pdfplumber.open(pdf_file) as pdf:
            full_text = ""
            table_lookup: Dict[str, str] = {}

            for page in pdf.pages:
                try:
                    page_text = page.extract_text(layout=True)
                except Exception:
                    page_text = None
                if not page_text:
                    page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

                _merge_table_lookup(table_lookup, page)
                _merge_columnar_word_lookup(table_lookup, page)

    except Exception as error:
        raise ValueError(f"Unable to read PDF file: {error}") from error

    if not full_text.strip():
        raise ValueError("No extractable text found in PDF (it may be scanned, empty, or password-protected).")

    raw = _parse_bill_text(full_text)

    if "metered_units" not in raw or float(raw.get("metered_units", 0)) == 0:
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

    if "consumer_name" not in raw:
        name_match = re.search(r"Mr\./Ms\.?\s*([A-Z][A-Z\s]+)", full_text, re.IGNORECASE)
        if name_match:
            raw["consumer_name"] = name_match.group(1).replace("-", " ").title().strip()

    if "bill_month" not in raw:
        month_match = re.search(r"BillMonth[:\s]*([A-Z]{3}-\d{4})", full_text, re.IGNORECASE)
        if month_match:
            raw["bill_month"] = month_match.group(1)

    if "bill_month" not in raw:
        month_match = re.search(r"BILL\s*MONTH\s*[:\-]?\s*([A-Z]{3}-\d{4})", full_text, re.IGNORECASE)
        if month_match:
            raw["bill_month"] = month_match.group(1)

    _apply_table_lookup(raw, table_lookup)

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
