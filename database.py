"""
Smart Energy Advisor
SQLite Database Layer

Responsibilities:
- Database connection management
- Schema initialization
- CRUD operations
- Saved analysis snapshots

No business logic.
No calculations.
No UI logic.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "energy_advisor.db"


def get_connection():
    """
    Creates and returns a SQLite connection.
    """

    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def _add_column_if_missing(connection, table: str, column: str, definition: str):
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    existing_columns = {row[1] for row in cursor.fetchall()}

    if column not in existing_columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        connection.commit()


def initialize_database():
    """
    Creates all required database tables, and adds any
    columns that are missing from an older schema version.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS appliances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL DEFAULT '',
            name TEXT NOT NULL,
            category TEXT,
            wattage REAL NOT NULL,
            hours_per_day REAL NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS saved_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL DEFAULT '',
            label TEXT NOT NULL,
            consumer_no TEXT,
            consumer_name TEXT,
            bill_month TEXT,
            billing_date TEXT,
            due_date TEXT,
            metered_units REAL,
            total_amount REAL,
            previous_reading REAL,
            current_reading REAL,
            source_type TEXT,
            saved_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS saved_record_appliances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            saved_record_id INTEGER NOT NULL,

            name TEXT NOT NULL,
            category TEXT,
            wattage REAL NOT NULL,
            hours_per_day REAL NOT NULL,
            quantity INTEGER NOT NULL,

            FOREIGN KEY(saved_record_id)
            REFERENCES saved_records(id)
            ON DELETE CASCADE
        )
        """
    )

    connection.commit()

    _add_column_if_missing(connection, "appliances", "session_id", "TEXT NOT NULL DEFAULT ''")
    _add_column_if_missing(connection, "saved_records", "session_id", "TEXT NOT NULL DEFAULT ''")

    connection.close()


def create_appliance(
    session_id: str,
    name: str,
    category: str,
    wattage: float,
    hours_per_day: float,
    quantity: int
):
    """
    Adds a new appliance to the appliance table.
    """

    connection = get_connection()

    cursor = connection.cursor()

    current_time = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO appliances
        (
            session_id,
            name,
            category,
            wattage,
            hours_per_day,
            quantity,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            name,
            category,
            wattage,
            hours_per_day,
            quantity,
            current_time,
            current_time
        )
    )

    connection.commit()

    appliance_id = cursor.lastrowid

    connection.close()

    return appliance_id


def get_all_appliances(session_id: str):
    """
    Returns all stored appliances for a given session.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM appliances
        WHERE session_id = ?
        ORDER BY id ASC
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]



def get_appliance_by_id(session_id: str, appliance_id: int):
    """
    Returns one appliance by id, , scoped to the given session.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM appliances
        WHERE id = ? AND session_id = ?
        """,
        (appliance_id, session_id)
    )

    row = cursor.fetchone()

    connection.close()

    if row:
        return dict(row)

    return None



def update_appliance(
    session_id: str,
    appliance_id: int,
    name: str,
    category: str,
    wattage: float,
    hours_per_day: float,
    quantity: int
):
    """
    Updates an existing appliance, scoped to the given session.
    """

    connection = get_connection()

    cursor = connection.cursor()

    updated_time = datetime.now().isoformat()

    cursor.execute(
        """
        UPDATE appliances
        SET
            name = ?,
            category = ?,
            wattage = ?,
            hours_per_day = ?,
            quantity = ?,
            updated_at = ?
        WHERE id = ? AND session_id = ?
        """,
        (
            name,
            category,
            wattage,
            hours_per_day,
            quantity,
            updated_time,
            appliance_id,
            session_id
        )
    )

    connection.commit()

    affected_rows = cursor.rowcount

    connection.close()

    return affected_rows > 0


def delete_appliance(session_id: str, appliance_id: int):
    """
    Deletes an appliance, scoped to the given session.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM appliances
        WHERE id = ? AND session_id = ?
        """,
        (appliance_id, session_id)
    )

    connection.commit()

    affected_rows = cursor.rowcount

    connection.close()

    return affected_rows > 0


def create_saved_record(
    session_id: str,
    bill_data: Dict[str, Any],
    appliance_snapshot: List[Dict[str, Any]]
):
    """
    Creates a saved analysis record with frozen appliance snapshots.

    Uses a transaction:
    saved_records + saved_record_appliances
    are saved together.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        saved_time = datetime.now().isoformat()

        label = bill_data.get("label")

        if not label:
            bill_month = bill_data.get("bill_month")
            consumer_name = bill_data.get("consumer_name")

            if consumer_name and bill_month:
                label = f"{consumer_name} - {bill_month}"

            elif bill_month:
                label = bill_month

            else:
                label = f"Saved Analysis {saved_time[:10]}"
        cursor.execute(
            """
            INSERT INTO saved_records
            (
                session_id,
                label,
                consumer_no,
                consumer_name,
                bill_month,
                billing_date,
                due_date,
                metered_units,
                total_amount,
                previous_reading,
                current_reading,
                source_type,
                saved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                label,   
                bill_data.get("consumer_no"),
                bill_data.get("consumer_name"),
                bill_data.get("bill_month"),
                bill_data.get("billing_date"),
                bill_data.get("due_date"),
                bill_data.get("metered_units"),
                bill_data.get("total_amount"),
                bill_data.get("previous_reading"),
                bill_data.get("current_reading"),
                bill_data.get("source_type"),
                saved_time
            )
        )

        saved_record_id = cursor.lastrowid

        # (keep everything below this exactly as it was — the
        # saved_record_appliances loop, commit, except, finally)


        for appliance in appliance_snapshot:

            cursor.execute(
                """
                INSERT INTO saved_record_appliances
                (
                    saved_record_id,
                    name,
                    category,
                    wattage,
                    hours_per_day,
                    quantity
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    saved_record_id,
                    appliance.get("name"),
                    appliance.get("category"),
                    appliance.get("wattage"),
                    appliance.get("hours_per_day"),
                    appliance.get("quantity")
                )
            )


        connection.commit()

        return saved_record_id


    except Exception:

        connection.rollback()

        raise


    finally:

        connection.close()



def get_saved_records(session_id: str):
    """
    Returns all saved analysis records for a given session.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM saved_records
        WHERE session_id = ?
        ORDER BY id DESC
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]



def get_saved_record_by_id(session_id: str, record_id: int):
    """
    Returns complete saved analysis:
    bill snapshot + appliance snapshot.
    Scoped to the given session.
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM saved_records
        WHERE id = ? AND session_id = ?
        """,
        (record_id, session_id)
    )

    record = cursor.fetchone()


    if record is None:

        connection.close()

        return None


    cursor.execute(
        """
        SELECT *
        FROM saved_record_appliances
        WHERE saved_record_id = ?
        """,
        (record_id,)
    )

    appliances = cursor.fetchall()


    connection.close()


    return {
        "record": dict(record),
        "appliances": [
            dict(item)
            for item in appliances
        ]
    }




def rename_saved_record(
    session_id: str,
    record_id: int,
    new_label: str
):
    """
    Updates saved record label only, scoped to the given session.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE saved_records
        SET label = ?
        WHERE id = ? AND session_id = ?
        """,
        (
            new_label,
            record_id,
            session_id
        )
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated



def delete_saved_record(session_id: str, record_id: int):
    """
    Deletes saved record, scoped to the given session.
    Appliance snapshots are deleted automatically
    because of ON DELETE CASCADE.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM saved_records
        WHERE id = ? AND session_id = ?
        """,
        (record_id, session_id)
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted