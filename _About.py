"""
About Page
Smart Energy Advisor

Responsibilities:
- Describe the Smart Energy Advisor system
- Explain the application architecture
- Introduce project features
- Provide an overview of technologies used

No:
- Database operations
- API requests
- Business logic
- Energy calculations
"""

import streamlit as st


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="About - Smart Energy Advisor",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About Smart Energy Advisor")

st.write(
    """
Smart Energy Advisor is an offline electricity consumption
analysis system that helps users understand their electricity
usage, estimate appliance-wise energy consumption, and receive
rule-based recommendations for improving energy efficiency.
"""
)

st.divider()


# --------------------------------------------------
# Project Overview
# --------------------------------------------------

st.header("🎯 Project Overview")

st.markdown(
    """
The Smart Energy Advisor combines a Streamlit frontend with a
FastAPI backend to provide a complete electricity analysis
workflow.

Users can upload electricity bills, import appliance
information, analyze household energy consumption, and receive
practical energy-saving suggestions.

The application is designed with a modular architecture where
each component has a single responsibility, making the system
easy to maintain, test, and extend.
"""
)


# --------------------------------------------------
# System Architecture
# --------------------------------------------------

st.header("🏗️ System Architecture")

st.code(
"""
                Streamlit Frontend
                        │
                        ▼
                  utils/api_client.py
                        │
                        ▼
                 FastAPI REST API
                        │
     ┌──────────────┬───────────────┬───────────────┐
     ▼              ▼               ▼
database.py   extract_data.py   suggestions.py
                        │
                        ▼
                analyze_data.py
                        │
                        ▼
             appliance_matcher.py
                        │
                        ▼
      knowledge/appliance_rules.json
""",
language="text"
)

st.info(
    """
The frontend never accesses the database or performs energy
calculations directly. All business logic is handled by the
FastAPI backend.
"""
)

st.divider()


# --------------------------------------------------
# Core Features
# --------------------------------------------------

st.header("⭐ Core Features")

left_column, right_column = st.columns(2)

with left_column:

    st.subheader("📄 Bill Processing")

    st.markdown(
        """
- Extract information from PDF electricity bills
- Extract bill data from images using OCR
- Import electricity data from CSV files
- Manual bill entry
- Automatic validation of extracted values
"""
    )

    st.subheader("🔌 Appliance Management")

    st.markdown(
        """
- Upload appliance information
- Manage appliance records
- Store wattage and usage hours
- Calculate appliance consumption
"""
    )


with right_column:

    st.subheader("📊 Energy Analysis")

    st.markdown(
        """
- Electricity tariff calculation
- Daily energy consumption
- Monthly energy consumption
- Monthly electricity cost
- Bill contribution of each appliance
- Savings estimation
"""
    )

    st.subheader("💡 Recommendations")

    st.markdown(
        """
- Rule-based appliance suggestions
- Appliance name matching
- Knowledge-base driven recommendations
- Estimated monthly savings
- Estimated yearly savings
"""
    )

st.divider()


# --------------------------------------------------
# Main Modules
# --------------------------------------------------

st.header("📦 Main Project Modules")

modules_left, modules_right = st.columns(2)

with modules_left:

    st.markdown(
        """
### Frontend

- Home
- Analysis
- Suggestions
- About

### Backend

- main.py
- database.py
"""
    )

with modules_right:

    st.markdown(
        """
### Utilities

- extract_data.py
- analyze_data.py
- suggestions.py
- appliance_matcher.py
- visualizations.py

### Knowledge Base

- appliance_rules.json
"""
    )

st.divider()

# --------------------------------------------------
# Technology Stack
# --------------------------------------------------

st.header("🛠️ Technology Stack")

frontend_column, backend_column, utilities_column = st.columns(3)

with frontend_column:

    st.subheader("Frontend")

    st.markdown(
        """
- Streamlit
- Plotly
- Pandas
"""
    )

with backend_column:

    st.subheader("Backend")

    st.markdown(
        """
- FastAPI
- SQLite
- Pydantic
- Uvicorn
"""
    )

with utilities_column:

    st.subheader("Utilities")

    st.markdown(
        """
- NumPy
- pdfplumber
- pytesseract
- OpenCV
"""
    )

st.divider()


# --------------------------------------------------
# Application Workflow
# --------------------------------------------------

st.header("🔄 Application Workflow")

st.code(
"""
Upload Electricity Bill
            │
            ▼
Bill Extraction
(PDF / Image / CSV / Manual)
            │
            ▼
Upload Appliance Data
            │
            ▼
Energy Analysis
            │
            ▼
Visualization
            │
            ▼
Suggestion Engine
            │
            ▼
Save Analysis Record
""",
language="text"
)

st.markdown(
    """
Every stage of the workflow is handled by an independent module.
This modular design keeps the frontend lightweight while all
processing is performed by the backend services.
"""
)

st.divider()


# --------------------------------------------------
# Energy Analysis Engine
# --------------------------------------------------

st.header("⚡ Energy Analysis Engine")

st.markdown(
    """
The Energy Analysis Engine performs all mathematical calculations
required for appliance-wise electricity analysis.

For every appliance the backend calculates:

- Electricity tariff
- Daily energy consumption
- Monthly energy consumption
- Monthly operating cost
- Percentage contribution to the total bill
- Estimated monthly savings
- Estimated yearly savings
"""
)

st.code(
"""
Daily Consumption (kWh)

= (Wattage × Hours × Quantity) / 1000


Monthly Consumption

= Daily Consumption × 30


Electricity Tariff

= Total Bill / Metered Units


Monthly Appliance Cost

= Monthly Consumption × Tariff


Bill Share (%)

= Appliance Cost / Total Bill × 100
""",
language="text"
)

st.success(
    """
All calculations are performed inside
utils/analyze_data.py.
The Streamlit frontend only displays the results.
"""
)

st.divider()


# --------------------------------------------------
# Visualization Engine
# --------------------------------------------------

st.header("📈 Visualization")

st.markdown(
    """
Interactive charts are created using Plotly after the backend
returns analyzed appliance data.

Available visualizations include:

- Monthly consumption distribution
- Appliance comparison charts
- Monthly electricity cost comparison
- Bill contribution charts
- Daily vs monthly consumption
- Savings projection charts
- Efficiency gauge
"""
)

st.info(
    """
Visualization logic is isolated inside
utils/visualizations.py.
No energy calculations are performed inside the visualization
module.
"""
)

st.divider()


# --------------------------------------------------
# Suggestion Engine
# --------------------------------------------------

st.header("💡 Suggestion Engine")

st.markdown(
    """
The suggestion engine combines appliance analysis with the
knowledge base to generate practical recommendations.

For every appliance the backend:

1. Matches the appliance name.
2. Resolves common synonyms.
3. Finds the best matching rule.
4. Estimates possible savings.
5. Returns a recommendation with projected monthly and yearly
   savings.
"""
)

st.code(
"""
Appliance

      │

      ▼

Appliance Matcher

      │

      ▼

Knowledge Base

      │

      ▼

Analysis Engine

      │

      ▼

Energy Saving Suggestion
""",
language="text"
)

st.warning(
    """
Recommendations are deterministic and rule-based using the
knowledge base. They are not generated by a machine learning
model.
"""
)

st.divider()


# --------------------------------------------------
# Database
# --------------------------------------------------

st.header("🗄️ Database")

st.markdown(
    """
The application uses SQLite to store user information locally.

Stored information includes:

- Appliance records
- Saved analysis records
- Bill snapshots
- Appliance snapshots

Database operations are performed exclusively by
database.py through the FastAPI backend.
"""
)

st.info(
    """
The frontend never communicates directly with the database.
All database operations are performed through REST API
endpoints exposed by FastAPI.
"""
)

st.divider()

# --------------------------------------------------
# Knowledge Base
# --------------------------------------------------

st.header("📚 Knowledge Base")

st.markdown(
    """
The recommendation system is powered by a JSON-based knowledge
base located at:

• knowledge/appliance_rules.json

The knowledge base contains:

- Appliance synonyms
- Exact appliance rules
- Category-based rules
- Generic fallback rules
- Estimated saving percentages

The appliance matcher searches this knowledge base to determine
the most appropriate recommendation for each appliance.
"""
)

st.code(
"""
User Appliance Name
        │
        ▼
Normalize Name
        │
        ▼
Resolve Synonym
        │
        ▼
Exact Rule Match
        │
        ▼
Category Rule Match
        │
        ▼
Generic Rule
""",
language="text"
)

st.info(
    """
The knowledge base can be expanded by simply editing the JSON
file without changing any application code.
"""
)

st.divider()


# --------------------------------------------------
# Project Structure
# --------------------------------------------------

st.header("📂 Project Structure")

st.code(
"""
Smart_Energy_Advisor/

│
├── app.py
├── pages/
│     ├── Home.py
│     ├── Analysis.py
│     ├── Suggestions.py
│     └── About.py
│
├── backend/
│     ├── main.py
│     ├── database.py
│     ├── knowledge/
│     │      └── appliance_rules.json
│     └── utils/
│            ├── api_client.py
│            ├── analyze_data.py
│            ├── appliance_matcher.py
│            ├── extract_data.py
│            ├── suggestions.py
│            └── visualizations.py
│
├── tests/
└── data/
""",
language="text"
)

st.success(
    """
The project follows a modular architecture where each file has
a single responsibility, making the system easier to maintain
and test.
"""
)

st.divider()


# --------------------------------------------------
# Future Improvements
# --------------------------------------------------

st.header("🚀 Future Enhancements")

future_left, future_right = st.columns(2)

with future_left:

    st.markdown(
        """
### Planned Features

- Historical bill comparison
- Monthly consumption trends
- Enhanced OCR accuracy
- Multi-user support
- Appliance search
"""
    )

with future_right:

    st.markdown(
        """
### Possible Extensions

- Smart meter integration
- Cloud synchronization
- Export analysis reports
- Mobile application
- Dashboard analytics
"""
    )

st.divider()


# --------------------------------------------------
# User Guide
# --------------------------------------------------

st.header("📖 User Guide")

with st.expander("1️⃣ Upload Electricity Bill"):

    st.markdown(
        """
Upload your electricity bill using one of the supported formats:

- PDF
- Image
- CSV
- Manual entry

The backend extracts and validates the bill information before
it is stored in the current session.
"""
    )


with st.expander("2️⃣ Upload Appliance Data"):

    st.markdown(
        """
Upload an appliance CSV containing:

- appliance
- wattage
- hours_per_day
- quantity

The appliance list is used for energy consumption analysis.
"""
    )


with st.expander("3️⃣ Analyze Energy Consumption"):

    st.markdown(
        """
Navigate to the Analysis page to calculate:

- Electricity tariff
- Daily consumption
- Monthly consumption
- Monthly cost
- Bill contribution
- Estimated savings

Interactive charts are generated automatically.
"""
    )


with st.expander("4️⃣ View Suggestions"):

    st.markdown(
        """
The Suggestions page provides appliance-specific recommendations
generated from the knowledge base together with estimated
monthly and yearly savings.
"""
    )

st.divider()


# --------------------------------------------------
# Frequently Asked Questions
# --------------------------------------------------

st.header("❓ Frequently Asked Questions")

with st.expander("Does the application require an internet connection?"):

    st.write(
        """
No.

The application is designed to run locally.
The Streamlit frontend communicates with the local FastAPI
backend running on your computer.
"""
    )


with st.expander("Where are suggestions generated?"):

    st.write(
        """
Suggestions are generated by the FastAPI backend using the
knowledge base and the appliance matching engine.
"""
    )


with st.expander("Can I add new appliance rules?"):

    st.write(
        """
Yes.

New appliances, synonyms, and recommendation rules can be added
to knowledge/appliance_rules.json without modifying the analysis
engine.
"""
    )


with st.expander("Is my data stored online?"):

    st.write(
        """
No.

Data is stored locally using SQLite unless additional storage
options are implemented in future versions.
"""
    )

st.divider()


# --------------------------------------------------
# Version Information
# --------------------------------------------------

st.header("📌 Version Information")

version_left, version_right = st.columns(2)

with version_left:

    st.metric(
        "Application Version",
        "1.0.0"
    )

    st.metric(
        "Frontend",
        "Streamlit"
    )

    st.metric(
        "Backend",
        "FastAPI"
    )


with version_right:

    st.metric(
        "Database",
        "SQLite"
    )

    st.metric(
        "Visualization",
        "Plotly"
    )

    st.metric(
        "Knowledge Base",
        "JSON Rules"
    )

st.divider()


# --------------------------------------------------
# Acknowledgement
# --------------------------------------------------

st.header("🙏 Acknowledgement")

st.markdown(
    """
Smart Energy Advisor was developed as a modular software
engineering project demonstrating:

- FastAPI REST API development
- Streamlit frontend development
- SQLite database integration
- Energy consumption analysis
- Rule-based recommendation systems
- Modular software architecture

The project emphasizes clean architecture by separating the
frontend, backend, business logic, database operations, and
knowledge base into independent modules.
"""
)

st.divider()


if st.button(
    "🏠 Back to Home",
    type="primary"
):
    st.switch_page("pages/1_Home.py")