# Smart-Energy-Advisor-

# Smart AI Energy Advisor System ⚡

An intelligent, AI-powered Streamlit web application that analyzes electricity bills and appliance usage data to provide personalized energy-saving recommendations.

## 🎯 Overview

The Smart AI Energy Advisor System helps households and businesses:
- 📊 Analyze energy consumption patterns
- 💰 Identify opportunities to save money
- 🌍 Reduce carbon footprint
- 💡 Get AI-powered recommendations

## ✨ Features

### 📄 Bill Analysis
- Extract data from PDF electricity bills automatically
- Parse consumer details, billing dates, and consumption data
- Support for various bill formats

### 📊 Consumption Analysis
- Appliance-wise energy breakdown
- Interactive visualizations with Plotly
- Daily, monthly, and annual cost calculations
- Consumption category classification

### 💡 AI Recommendations
- Personalized energy-saving suggestions
- Energy hog detection (appliances consuming >10% total energy)
- Potential savings calculator
- Step-by-step action plans

### 📈 Advanced Analytics
- Efficiency scoring (0-100 scale)
- Consumption pattern analysis
- Calculated vs actual consumption comparison
- Environmental impact tracking (CO₂ reduction)

## 🏗️ Project Structure

```
smart_ai_energy_advisor/
│
├── app.py                      # Main Streamlit application entry point
├── pages/
│   ├── 1_Home.py              # File upload and data extraction
│   ├── 2_Analysis.py          # Energy consumption analysis
│   ├── 3_Suggestions.py       # AI-powered recommendations
│   └── 4_About.py             # About and user guide
│
├── utils/
│   ├── extract_data.py        # PDF extraction utilities
│   ├── analyze_data.py        # Analysis and calculations
│   └── visualize.py           # Plotly visualizations
│
├── data/
│   ├── sample_bill.txt        # Sample electricity bill
│   ├── appliance_data.csv     # Sample appliance data
│
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## 📦 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **pdfplumber**: PDF text extraction
- **pytesseract**: OCR for scanned documents
- **plotly**: Interactive data visualizations
- **scikit-learn**: Machine learning and pattern analysis

## 🚀 Getting Started

### Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install streamlit pandas numpy pdfplumber pytesseract plotly scikit-learn
```

### Running the Application

```bash
streamlit run app.py --server.port 5000
```

The application will open in your browser at `http://localhost:5000`

## 📖 How to Use

### Step 1: Upload Data (Home Page)

1. **Upload Electricity Bill**: Upload your PDF electricity bill
   - The system automatically extracts consumer details, billing dates, units consumed, and total amount
   
2. **Upload Appliance Data**: Upload a CSV file with your appliance usage
   - Required columns: `appliance`, `wattage`, `hours_per_day`, `quantity`
   - Or use the sample data to explore features

### Step 2: View Analysis (Analysis Page)

- View comprehensive consumption overview
- See efficiency score and metrics
- Explore interactive charts:
  - Energy distribution pie chart
  - Consumption comparison bar chart
  - Cost vs consumption analysis
  - Category breakdown
- Review top energy consumers
- Download detailed reports

### Step 3: Get Recommendations (Suggestions Page)

- View personalized energy-saving recommendations
- Calculate potential savings with interactive slider
- Get action plans:
  - Immediate actions (this week)
  - Short-term goals (this month)
  - Long-term plans (3-6 months)
- See environmental impact (CO₂ reduction)

### Step 4: Learn More (About Page)

- Understand how the system works
- Read the comprehensive user guide
- Troubleshooting tips
- FAQ section

## 📊 Sample Data

The project includes sample data to help you get started:

### Sample Appliance Data CSV

```csv
appliance,wattage,hours_per_day,quantity
Air Conditioner,1500,8,2
Refrigerator,150,24,1
Washing Machine,500,1,1
Television,100,5,2
...
```

### Required CSV Format

| Column | Description | Example |
|--------|-------------|---------|
| appliance | Name of the appliance | Air Conditioner |
| wattage | Power consumption in watts | 1500 |
| hours_per_day | Average daily usage hours | 8 |
| quantity | Number of units | 2 |

## 🧮 How Calculations Work

### Energy Consumption
```
Daily Consumption (kWh) = (Wattage × Hours × Quantity) / 1000
Monthly Consumption (kWh) = Daily Consumption × 30
```

### Cost Calculation
```
Monthly Cost (₹) = Monthly Consumption × Rate per kWh
(Default rate: ₹6.50/kWh)
```

### Efficiency Score
```
Coefficient of Variation = (Std Dev / Mean) × 100
Efficiency Score = max(0, 100 - Coefficient of Variation)
```

Higher score = more balanced consumption across appliances

## 💡 Energy Saving Tips

### Quick Wins
- Switch to LED bulbs (75% energy savings)
- Set AC to 24-26°C
- Unplug devices when not in use
- Use smart power strips

### Long-term Investments
- 5-star rated appliances
- Solar water heater
- Inverter-based appliances
- Solar panels

## 🌍 Environmental Impact

The system calculates environmental benefits:
- CO₂ emissions reduced (kg)
- Equivalent trees planted
- Carbon footprint reduction

**Formula**: ~0.82 kg CO₂ per kWh (India average)

## 🔧 Troubleshooting

### PDF Extraction Issues
- Ensure PDF contains text (not just scanned images)
- Check PDF is not password-protected
- Try the sample bill to test features

### CSV Upload Fails
- Verify all required columns are present
- Check column names spelling
- Ensure numeric values don't contain text

### Unexpected Analysis Results
- Verify appliance wattage is correct
- Check hours_per_day are realistic (0-24)
- Confirm quantity values

## 🚀 Future Enhancements

- 🔮 Predictive analytics with ML models
- 📱 Mobile app version
- 🔔 Smart alerts for consumption spikes
- 📅 Historical tracking across months
- 🌤️ Weather data integration
- 🏆 Gamification features
- 🔌 IoT smart meter integration

## 📝 License

This project is open-source and available for educational and commercial use.

## 🙏 Acknowledgments

Built with:
- Python & Streamlit
- Plotly for visualizations
- PDFPlumber for PDF extraction
- Pandas for data analysis

## 📧 Support

For questions, feedback, or support, please refer to the About page in the application.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Made with**: ❤️ and AI

Start your journey towards energy efficiency today! 💚
