# Smart AI Energy Advisor System

## Overview

The Smart AI Energy Advisor System is an intelligent, AI-powered Streamlit web application that analyzes electricity bills and appliance usage data to provide personalized energy-saving recommendations. The application helps households and businesses understand their energy consumption patterns, identify cost-saving opportunities, reduce carbon footprint, and receive actionable AI-powered recommendations.

The system follows a multi-page Streamlit architecture with four main user flows: data upload/extraction, consumption analysis, AI-powered suggestions, and system information. It processes PDF electricity bills, extracts relevant data using pattern matching, analyzes appliance-level energy consumption, and generates personalized recommendations with potential savings calculations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack**: Streamlit-based multi-page application
- **Design Pattern**: Multi-page app structure using Streamlit's native page routing
- **UI Components**: Custom CSS styling for enhanced user experience with feature boxes, responsive layouts, and themed color schemes
- **Visualization**: Plotly for interactive charts (pie charts, bar charts, gauge charts, cost comparisons)
- **Layout Strategy**: Wide layout with column-based responsive design for side-by-side comparisons

**Rationale**: Streamlit was chosen for rapid development and built-in session state management, eliminating the need for complex frontend frameworks while providing an interactive, data-focused user experience.

### Application Flow

**Multi-page Structure**:
1. **Main Entry** (`app.py`): Landing page with navigation and welcome interface
2. **Home Page** (`pages/1_Home.py`): File upload interface for PDF bills and CSV appliance data
3. **Analysis Page** (`pages/2_Analysis.py`): Displays consumption analytics, visualizations, and efficiency scores
4. **Suggestions Page** (`pages/3_Suggestions.py`): AI-powered recommendations and savings projections
5. **About Page** (`pages/4_About.py`): System documentation and usage guide

**Session State Management**: Uses Streamlit's session state to persist data across pages (`bill_data`, `appliance_data`, `raw_bill_text`)

**Rationale**: The multi-page approach separates concerns and provides a logical workflow from data input to actionable insights, matching typical user mental models.

### Data Processing Architecture

**PDF Data Extraction** (`utils/extract_data.py`):
- Uses `pdfplumber` library for PDF text extraction
- Regular expression patterns for parsing consumer details, billing dates, meter readings, and charges
- Handles multi-page PDFs with text concatenation
- Error handling with fallback values ('N/A', 0)

**Rationale**: pdfplumber provides reliable text extraction without complex OCR requirements, suitable for structured electricity bills with consistent formats.

**Energy Consumption Analysis** (`utils/analyze_data.py`):
- Appliance-level consumption calculations based on wattage, usage hours, and quantity
- Statistical summary generation (totals, averages, percentages)
- Consumption categorization (high/medium/low)
- Energy hog identification (appliances consuming >10% of total)
- Efficiency scoring algorithm (0-100 scale)
- Cost calculations with configurable per-kWh rates (default: ₹6.5/kWh)

**Rationale**: Modular calculation functions enable reusability across different pages and support extensibility for additional metrics.

### Visualization Layer

**Chart Generation** (`utils/visualize.py`):
- Plotly-based interactive visualizations
- Chart types: pie charts (consumption distribution), bar charts (appliance comparison), gauge charts (efficiency scores), projection charts (savings scenarios)
- Consistent color schemes and hover interactions
- Responsive sizing for different screen dimensions

**Rationale**: Plotly provides professional, interactive visualizations with minimal configuration, enhancing data comprehension through visual engagement.

### Data Flow

1. **Upload**: User uploads PDF bill and/or CSV appliance data
2. **Extraction**: System extracts structured data using pattern matching
3. **Storage**: Data persists in Streamlit session state
4. **Calculation**: Backend utilities calculate consumption, costs, and efficiency metrics
5. **Visualization**: Plotly generates interactive charts from calculated data
6. **Recommendations**: AI analysis produces personalized suggestions based on consumption patterns
7. **Display**: Multi-page interface presents insights progressively

**Rationale**: This unidirectional flow ensures data consistency and allows users to navigate freely between analysis views without re-processing.

### Recommendation Engine

**AI-Powered Suggestions**:
- Pattern-based recommendation generation using consumption thresholds
- Energy hog detection and prioritization
- Potential savings calculation with percentage reduction scenarios
- Action plan generation with step-by-step guidance
- Environmental impact tracking (CO₂ reduction estimates)

**Rationale**: Rule-based AI provides transparent, explainable recommendations that users can validate against their actual usage patterns.

### Configuration and Extensibility

**Hardcoded Constants**:
- Default electricity rate: ₹6.5/kWh
- Monthly calculation basis: 30 days
- Energy hog threshold: 10% of total consumption
- Efficiency score ranges: 0-100 scale

**Extensibility Points**:
- Modular utility functions support adding new metrics
- Visualization library separation enables chart type expansion
- Session state pattern supports additional data sources
- Page-based architecture accommodates new analysis views

**Rationale**: Configuration constants are centralized in calculation functions for easy updates, while modular design supports future enhancements.

## External Dependencies

### Core Libraries

**Streamlit**: Web application framework
- Purpose: Multi-page application structure, UI components, session state management
- Used for: Page routing, file uploads, interactive widgets, layout management

**Pandas**: Data manipulation and analysis
- Purpose: DataFrame operations for appliance data and consumption calculations
- Used for: Data transformation, aggregation, statistical operations

**NumPy**: Numerical computing
- Purpose: Mathematical calculations for consumption analysis
- Used for: Array operations, statistical computations

### Visualization

**Plotly**: Interactive charting library
- Purpose: Creating dynamic, interactive visualizations
- Used for: Pie charts, bar charts, gauge charts, cost projections
- Specific modules: `plotly.express`, `plotly.graph_objects`

### PDF Processing

**pdfplumber**: PDF data extraction
- Purpose: Extracting text content from electricity bill PDFs
- Used for: Multi-page text extraction, structured data parsing
- Alternative considered: PyPDF2 (pdfplumber chosen for better text extraction reliability)

### Data Format Support

**CSV Files**: Appliance usage data input
- Format: Columns expected - appliance name, wattage, hours per day, quantity
- Processing: Pandas DataFrame operations

**PDF Files**: Electricity bill input
- Format: Text-based PDFs with structured bill information
- Processing: pdfplumber extraction + regex parsing

### File System

**Local File Storage**: No database required
- Session-based data persistence using Streamlit's session state
- Uploaded files processed in-memory without permanent storage
- Sample data provided in `data/sample_bill.txt` for testing

**Rationale**: In-memory processing eliminates database complexity for single-session use cases, while session state provides sufficient persistence for the analysis workflow.

### Regular Expressions

**Pattern Matching**: Data extraction from unstructured text
- Consumer number patterns
- Date parsing patterns
- Numerical value extraction (meter readings, units, amounts)
- Multi-format support through flexible regex patterns

**Rationale**: Regex provides flexible text parsing for varying bill formats without requiring machine learning models.