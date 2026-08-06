<p align="center">
  <h1 align="center">⚡ Smart Energy Advisor</h1>
  <p align="center">
    A cloud-based electricity consumption analysis system built with Streamlit, FastAPI, and Supabase.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg">
  <img src="https://img.shields.io/badge/Streamlit-Frontend-red.svg">
  <img src="https://img.shields.io/badge/FastAPI-Backend-green.svg">
  <img src="https://img.shields.io/badge/Supabase-PostgreSQL-3FCF8E.svg">
</p>

---

## 🎯 Overview

**Smart Energy Advisor** is a cloud-based application that helps users analyze household electricity consumption, estimate appliance-wise energy usage, visualize usage patterns, and receive practical, rule-based recommendations for improving energy efficiency.

The application follows a modern three-tier architecture: a **Streamlit** frontend communicates with a **FastAPI** backend, which securely handles all data operations with a **Supabase PostgreSQL** database.

With Smart Energy Advisor, users can:

- 📊 Analyze household electricity consumption
- ⚡ Estimate appliance-wise energy usage
- 💰 Calculate appliance operating costs
- 📈 Visualize electricity consumption trends
- 💡 Receive rule-based energy-saving recommendations
- 📚 Store and review historical analyses

---

## ✨ Features

### 📄 Electricity Bill Management
- Upload electricity bills in PDF format
- Import bill information from CSV files
- Manual bill entry
- Automatic bill data validation

### 🔌 Appliance Management
- Upload appliance information via CSV
- Store appliance wattage, quantity, and usage hours
- Manage appliance records
- Appliance-wise energy consumption analysis

### 📊 Energy Analysis
Automatically calculates:
- Electricity tariff
- Daily and monthly energy consumption
- Monthly operating cost per appliance
- Appliance contribution to the electricity bill
- Estimated monthly and yearly savings

### 📈 Interactive Visualizations
- Appliance energy comparison
- Monthly consumption charts
- Electricity cost comparison
- Bill contribution charts
- Savings projections
- Energy efficiency indicators

### 💡 Rule-Based Recommendations
- Appliance-specific energy-saving suggestions
- Monthly and yearly savings estimation
- Practical energy conservation tips
- Knowledge-base driven recommendations (no ML required)

---

## 🧭 How It Works

1. **Upload Electricity Bill** — Provide bill data via PDF, CSV, or manual entry on the **Home** page. The app validates the input automatically.
2. **Upload Appliance Information** — Upload a CSV with appliance details (see format below).
3. **Analyze Consumption** — The **Analysis** page calculates tariff, daily/monthly consumption, appliance-wise cost, bill contribution, and estimated savings, all shown through interactive charts.
4. **View Suggestions** — The **Suggestions** page surfaces appliance-specific, rule-based energy-saving tips with estimated savings.
5. **Save and Review** — Save completed analyses and review them anytime on the **History** page.

### Appliance CSV Format

| Column          | Description            | Example         |
|-----------------|------------------------|-----------------|
| `appliance`     | Appliance name         | Air Conditioner |
| `wattage`       | Power rating (Watts)   | 1500            |
| `hours_per_day` | Daily usage hours      | 8               |
| `quantity`      | Number of appliances   | 2               |

```csv
appliance,wattage,hours_per_day,quantity
Air Conditioner,1500,8,2
Refrigerator,180,24,1
Television,100,5,2
Ceiling Fan,75,10,4
Washing Machine,500,1,1
```

---

## 🧮 Energy Consumption Calculations

**Daily Consumption (kWh)**
```
= (Wattage × Hours per Day × Quantity) ÷ 1000
```

**Monthly Consumption (kWh)**
```
= Daily Consumption × 30
```

**Electricity Tariff (₹/kWh)**
```
= Total Bill Amount ÷ Metered Units
```

**Monthly Appliance Cost (₹)**
```
= Monthly Consumption × Tariff
```

**Appliance Bill Contribution (%)**
```
= (Appliance Cost ÷ Total Bill) × 100
```

---

## 💡 Recommendation Engine

The recommendation engine is entirely **rule-based** — no machine learning is involved. Recommendations are generated from predefined appliance rules stored in a JSON knowledge base at `backend/knowledge/appliance_rules.json`.

**Workflow:**

```
User Appliance
      │
      ▼
Normalize Appliance Name
      │
      ▼
Appliance Matcher
      │
      ▼
Knowledge Base
      │
      ▼
Recommendation Rules
      │
      ▼
Estimated Savings
```

Each recommendation may include:
- Suggested improvements
- Better operating practices
- Monthly and yearly savings estimates

The knowledge base contains appliance synonyms, categories, recommendation rules, saving percentages, and generic fallback rules. **Adding support for a new appliance only requires updating the JSON file — no application code changes are needed.**

---

## ☁️ Architecture

```
User
  │
  ▼
Streamlit Community Cloud (Frontend)
  │
  ▼
FastAPI Backend (Render)
  │
  ├──────────────┬──────────────────────┐
  ▼              ▼                      ▼
Energy      Recommendation         Supabase
Analysis        Engine             PostgreSQL
```

The Streamlit frontend never communicates directly with the database — all operations flow through the FastAPI backend, which improves security, maintainability, and scalability. An active internet connection is required since all three components are cloud-hosted.

---

## 🏗️ Project Structure

```text
Smart_Energy_Advisor/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── knowledge/
│   │   └── appliance_rules.json
│   └── utils/
│       ├── analyze_data.py
│       ├── api_client.py
│       ├── appliance_matcher.py
│       ├── extract_data.py
│       ├── suggestions.py
│       └── visualizations.py
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Analysis.py
│   ├── 3_Suggestions.py
│   └── 4_History.py
│
├── data/
├── tests/
├── Landing_Page.py
├── _About.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Technology Stack

**Frontend**
- Streamlit — interactive web application framework
- Plotly — interactive charts and visualizations
- Pandas — data manipulation and analysis

**Backend**
- FastAPI — REST API development
- Uvicorn — ASGI web server
- Pydantic — data validation and serialization

**Database**
- Supabase PostgreSQL — cloud-hosted relational database

**Data Processing**
- NumPy — numerical computations
- pdfplumber — PDF text extraction

**Deployment**
- Streamlit Community Cloud — frontend hosting
- Render — backend hosting
- Supabase — database hosting

> **Note:** The project no longer uses OCR or image-processing libraries such as OpenCV or pytesseract.

### Dependencies

| Library    | Purpose                     |
|------------|-----------------------------|
| Streamlit  | Frontend web application    |
| FastAPI    | Backend REST API            |
| Uvicorn    | API server                  |
| Pandas     | Data processing             |
| NumPy      | Numerical calculations      |
| Plotly     | Interactive visualizations  |
| pdfplumber | PDF bill extraction         |
| Pydantic   | Data validation             |
| Requests   | API communication           |
| Supabase   | Database integration        |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- A Supabase project
- An active internet connection

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Smart_Energy_Advisor.git
cd Smart_Energy_Advisor
```

### 2. Create a Virtual Environment

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (or backend directory, if applicable):

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
BACKEND_URL=http://localhost:8000
```

Replace the placeholder values with your own Supabase project credentials.

### 5. Run the Application

**Start the backend:**
```bash
uvicorn backend.main:app --reload
```
Runs at `http://localhost:8000`

**Start the frontend** (in a new terminal):
```bash
streamlit run Landing_Page.py
```
The app will open automatically in your default browser.

---

## ☁️ Deployment

| Component | Platform                    |
|-----------|-----------------------------|
| Frontend  | Streamlit Community Cloud   |
| Backend   | Render                      |
| Database  | Supabase PostgreSQL         |

**Deployment Flow**

```
User
  │
  ▼
Streamlit Community Cloud
  │
  ▼
FastAPI Backend (Render)
  │
  ▼
Supabase PostgreSQL
  │
  ▼
Response Returned to User
```

Since the application communicates with cloud-hosted services, an active internet connection is required.

**Live Application**
- Frontend: *(add your Streamlit Cloud URL here)*
- Backend API: *(add your Render API URL here)*
- Database: Supabase PostgreSQL

---

## 🔧 Troubleshooting

**PDF Upload Issues**
- Ensure the PDF contains selectable text
- Verify the PDF is not password protected
- Check that the uploaded file is not corrupted

**CSV Upload Issues**
- Verify all required columns are present: `appliance`, `wattage`, `hours_per_day`, `quantity`
- Ensure column names are correctly spelled
- Confirm `wattage`, `quantity`, and usage hours contain numeric values

**Backend Connection Issues**
- Verify the Render backend is running
- Check that the backend URL is correctly configured
- Ensure your internet connection is active

**Database Connection Issues**
- Verify Supabase credentials are correctly configured
- Check that the database service is online
- Confirm the required tables exist

---

## 🚀 Future Enhancements

- 📈 Historical electricity bill comparison
- 📊 Monthly and yearly consumption trends
- 📄 Export analysis reports (PDF/Excel)
- 📱 Mobile-responsive interface
- 🌐 Multi-user authentication
- 🔔 Smart energy usage alerts
- 🔌 Smart meter integration
- ☀️ Renewable energy usage tracking
- 📉 Advanced dashboard analytics
- 🤖 Enhanced recommendation rules

---

## 📌 Version

| Component               | Version                             |
|-------------------------|-------------------------------------|
| Application             | 1.0.0                               |
| Frontend                | Streamlit                           |
| Backend                 | FastAPI                             |
| Database                | Supabase PostgreSQL                 |
| Deployment              | Streamlit Community Cloud + Render  |
| Recommendation Engine   | Rule-Based JSON                     |

---

## 🙏 Acknowledgements

Smart Energy Advisor was developed as a software engineering project to demonstrate modern full-stack Python application development, showcasing:

- Streamlit web application development
- FastAPI REST API development
- Cloud database integration with Supabase PostgreSQL
- Cloud deployment using Streamlit Community Cloud and Render
- Rule-based recommendation systems
- Interactive data visualization with Plotly
- Modular software architecture
- RESTful client-server communication

Special thanks to the open-source community and the developers of Python, Streamlit, FastAPI, Supabase, Plotly, Pandas, NumPy, pdfplumber, and Uvicorn.

---
## 📬 Contact

Questions, suggestions, or collaboration ideas? Open an issue or submit a pull request through the GitHub repository.

---

<p align="center"><b>⚡ Smart Energy Advisor — Analyze Smarter. Save Energy. Reduce Costs.</b></p>
