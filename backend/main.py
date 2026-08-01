"""
Smart Energy Advisor
FastAPI Backend API Layer

Responsibilities:
- REST API endpoints
- Request validation
- Connecting backend modules

No:
- Database SQL logic
- Energy calculations
- Appliance rules
- UI logic

Uses:
- database.py
- utils.extract_data
- utils.suggestions
"""

from contextlib import asynccontextmanager
from typing import List, Dict, Any, Optional


from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from pydantic import BaseModel


from database import (
    initialize_database,

    create_appliance,
    get_all_appliances,
    get_appliance_by_id,
    update_appliance,
    delete_appliance,

    create_saved_record,
    get_saved_records,
    get_saved_record_by_id,
    rename_saved_record,
    delete_saved_record
)


from utils.extract_data import (
    extract_bill_data,
    extract_bill_data_from_csv,
    build_manual_bill_data
)


from utils.suggestions import (
    generate_suggestions
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Smart Energy Advisor API",
    version="1.0.0",
    description="Offline electricity consumption analysis API",
    lifespan=lifespan
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class ApplianceCreate(BaseModel):
    name: str
    category: str
    wattage: float
    hours_per_day: float
    quantity: int


class SavedRecordCreate(BaseModel):
    bill_data: Dict[str, Any]
    appliance_snapshot: List[Dict[str, Any]]


class RenameRecordRequest(BaseModel):
    label: str


class SuggestionRequest(BaseModel):
    appliances: List[Dict[str, Any]]
    bill_data: Dict[str, Any]


class ManualBillEntry(BaseModel):
    consumer_no: Optional[str] = None
    consumer_name: Optional[str] = None
    bill_month: Optional[str] = None
    billing_date: Optional[str] = None
    due_date: Optional[str] = None
    metered_units: Optional[float] = None
    total_amount: Optional[float] = None
    previous_reading: Optional[float] = None
    current_reading: Optional[float] = None


# --------------------------------------------------
# Appliance CRUD
# --------------------------------------------------

@app.get("/appliances")
def read_appliances(session_id: str):
    return get_all_appliances(session_id)


@app.post("/appliances")
def add_appliance(appliance: ApplianceCreate, session_id: str):
    appliance_id = create_appliance(
        session_id,
        appliance.name,
        appliance.category,
        appliance.wattage,
        appliance.hours_per_day,
        appliance.quantity
    )
    return {"success": True, "id": appliance_id}


@app.put("/appliances/{appliance_id}")
def edit_appliance(appliance_id: int, appliance: ApplianceCreate, session_id: str):
    updated = update_appliance(
        session_id,
        appliance_id,
        appliance.name,
        appliance.category,
        appliance.wattage,
        appliance.hours_per_day,
        appliance.quantity
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return {"success": True}


@app.delete("/appliances/{appliance_id}")
def remove_appliance(appliance_id: int, session_id: str):
    deleted = delete_appliance(session_id, appliance_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return {"success": True}
    return {"success": True}


# --------------------------------------------------
# Bill Extraction
# --------------------------------------------------

@app.post("/extract-bill")
async def extract_bill(file: UploadFile = File(...)):
    try:
        return extract_bill_data(file.file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/extract-bill/csv")
async def extract_bill_csv(file: UploadFile = File(...)):
    try:
        return extract_bill_data_from_csv(file.file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/extract-bill/manual")
def extract_bill_manual(entry: ManualBillEntry):
    try:
        return build_manual_bill_data(entry.model_dump(exclude_none=True))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# --------------------------------------------------
# Saved Records
# --------------------------------------------------

@app.post("/saved-records")
def save_record(record: SavedRecordCreate, session_id: str):
    record_id = create_saved_record(session_id, record.bill_data, record.appliance_snapshot)
    return {"success": True, "id": record_id}


@app.get("/saved-records")
def read_saved_records(session_id: str):
    return get_saved_records(session_id)


@app.get("/saved-records/{record_id}")
def read_saved_record(record_id: int, session_id: str):
    record = get_saved_record_by_id(session_id, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Saved record not found")
    return record


@app.patch("/saved-records/{record_id}")
def rename_record(record_id: int, request: RenameRecordRequest, session_id: str):
    updated = rename_saved_record(session_id, record_id, request.label)
    if not updated:
        raise HTTPException(status_code=404, detail="Saved record not found")
    return {"success": True}


@app.delete("/saved-records/{record_id}")
def remove_saved_record(record_id: int, session_id: str):
    deleted = delete_saved_record(session_id, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Saved record not found")
    return {"success": True}


# --------------------------------------------------
# Suggestions
# --------------------------------------------------

@app.post("/suggestions")
def get_suggestions(request: SuggestionRequest):
    return generate_suggestions(request.appliances, request.bill_data)