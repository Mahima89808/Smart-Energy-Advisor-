import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from utils.extract_data import (
    extract_bill_data,
    extract_bill_data_from_image,
    extract_bill_data_from_csv,
    build_manual_bill_data,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CONTRACT_KEYS = {
    "consumer_no", "consumer_name", "bill_month", "billing_date", "due_date",
    "metered_units", "total_amount", "previous_reading", "current_reading"
}


def test_pdf_extracts_all_fields():
    with open(FIXTURES / "sample_bill.pdf", "rb") as f:
        result = extract_bill_data(f)

    assert result["consumer_no"] == "123456789"
    assert result["consumer_name"] == "John Doe"
    assert result["bill_month"] == "July 2026"
    assert result["metered_units"] == 300.0
    assert result["total_amount"] == 2500.0
    assert result["previous_reading"] == 1000.0
    assert result["current_reading"] == 1300.0


def test_pdf_empty_text_raises_value_error():
    fake_pdf = io.BytesIO(b"%PDF-1.4\n%%EOF")
    with pytest.raises(ValueError):
        extract_bill_data(fake_pdf)


def test_pdf_result_matches_contract():
    with open(FIXTURES / "sample_bill.pdf", "rb") as f:
        result = extract_bill_data(f)
    assert set(result.keys()) == CONTRACT_KEYS


def test_ocr_extracts_fields_from_image():
    with open(FIXTURES / "sample_bill.png", "rb") as f:
        result = extract_bill_data_from_image(f)

    assert result["consumer_no"] == "987654321"
    assert result["consumer_name"] == "Jane Smith"
    assert result["bill_month"] == "August 2026"
    assert result["metered_units"] == 250.0
    assert result["total_amount"] == 2000.0


def test_ocr_blank_image_raises_value_error():
    from PIL import Image
    blank = Image.new("RGB", (200, 200), color="white")
    buf = io.BytesIO()
    blank.save(buf, format="PNG")
    buf.seek(0)
    with pytest.raises(ValueError):
        extract_bill_data_from_image(buf)


def test_ocr_unreadable_file_raises_value_error():
    not_an_image = io.BytesIO(b"this is not image data")
    with pytest.raises(ValueError):
        extract_bill_data_from_image(not_an_image)


def test_ocr_result_matches_contract():
    with open(FIXTURES / "sample_bill.png", "rb") as f:
        result = extract_bill_data_from_image(f)
    assert set(result.keys()) == CONTRACT_KEYS


def test_csv_full_row():
    csv_content = (
        "consumer_no,consumer_name,bill_month,billing_date,due_date,"
        "metered_units,total_amount,previous_reading,current_reading\n"
        "C001,Test User,July 2026,01/07/2026,15/07/2026,300,2500,1000,1300\n"
    )
    result = extract_bill_data_from_csv(io.StringIO(csv_content))
    assert result["consumer_no"] == "C001"
    assert result["metered_units"] == 300.0
    assert result["total_amount"] == 2500.0


def test_csv_partial_row_defaults_missing_columns():
    csv_content = "metered_units,total_amount\n300,2500\n"
    result = extract_bill_data_from_csv(io.StringIO(csv_content))
    assert result["consumer_no"] == "N/A"
    assert result["metered_units"] == 300.0


def test_csv_bad_numeric_type_raises_value_error():
    csv_content = "metered_units,total_amount\nnot_a_number,2500\n"
    with pytest.raises(ValueError):
        extract_bill_data_from_csv(io.StringIO(csv_content))


def test_csv_empty_file_raises_value_error():
    csv_content = "consumer_no,metered_units\n"
    with pytest.raises(ValueError):
        extract_bill_data_from_csv(io.StringIO(csv_content))


def test_csv_result_matches_contract():
    csv_content = "metered_units,total_amount\n300,2500\n"
    result = extract_bill_data_from_csv(io.StringIO(csv_content))
    assert set(result.keys()) == CONTRACT_KEYS


def test_manual_minimal_valid_input():
    result = build_manual_bill_data({"metered_units": 300, "total_amount": 2500})
    assert result["metered_units"] == 300.0
    assert result["consumer_no"] == "N/A"


def test_manual_negative_units_rejected():
    with pytest.raises(ValueError):
        build_manual_bill_data({"metered_units": -50, "total_amount": 2500})


def test_manual_negative_amount_rejected():
    with pytest.raises(ValueError):
        build_manual_bill_data({"metered_units": 300, "total_amount": -100})


def test_manual_current_less_than_previous_reading_rejected():
    with pytest.raises(ValueError):
        build_manual_bill_data({"previous_reading": 1500, "current_reading": 1000})


def test_manual_derives_units_from_readings():
    result = build_manual_bill_data({
        "previous_reading": 1000, "current_reading": 1300, "total_amount": 2500,
    })
    assert result["metered_units"] == 300.0


def test_manual_result_matches_contract():
    result = build_manual_bill_data({"metered_units": 300, "total_amount": 2500})
    assert set(result.keys()) == CONTRACT_KEYS


def test_all_four_paths_return_identical_key_sets():
    with open(FIXTURES / "sample_bill.pdf", "rb") as f:
        pdf_result = extract_bill_data(f)
    with open(FIXTURES / "sample_bill.png", "rb") as f:
        ocr_result = extract_bill_data_from_image(f)
    csv_result = extract_bill_data_from_csv(io.StringIO("metered_units,total_amount\n300,2500\n"))
    manual_result = build_manual_bill_data({"metered_units": 300, "total_amount": 2500})

    assert set(pdf_result.keys()) == CONTRACT_KEYS
    assert set(ocr_result.keys()) == CONTRACT_KEYS
    assert set(csv_result.keys()) == CONTRACT_KEYS
    assert set(manual_result.keys()) == CONTRACT_KEYS