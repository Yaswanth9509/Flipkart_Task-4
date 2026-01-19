# Maritime Fleet Performance Analytics

## Project Overview

Maritime Fleet Performance Analytics is a comprehensive data analysis system designed to process, analyze, and report on maritime vessel performance metrics. The application integrates multiple data sources to provide insights into fuel efficiency, operational performance, maintenance patterns, environmental conditions, and risk assessment for maritime fleets.

## Purpose

This system automates the analysis of maritime fleet operations by:
- Integrating data from multiple maritime sources
- Calculating key performance indicators (KPIs)
- Assessing operational risks and maintenance needs
- Generating comprehensive analytical reports
- Providing interactive dashboards for data visualization

## Project Structure

```
.
├── app.py                           # Main interactive application entry point
├── core_data_pipeline.py            # Data generation and integration module
├── analytics_engine.py              # Metrics calculation and analysis engine
├── output_manager.py                # Reporting and data validation module
├── requirements.txt                 # Python dependencies
├── data/                            # Input data directory
│   ├── dataset_A_specs.csv          # Vessel specifications
│   ├── dataset_B_nav.csv            # Navigation logs
│   ├── dataset_C_env.csv            # Environmental conditions
│   ├── dataset_D_fuel.csv           # Fuel consumption data
│   ├── dataset_E_maint.csv          # Maintenance incidents
│   ├── environmental_conditions.csv
│   ├── fuel_consumption.csv
│   ├── maintenance_incidents.csv
│   ├── navigation_logs.csv
│   └── ship_specifications.csv
└── output/                          # Generated reports and analysis
    ├── data_summary.csv             # Summary statistics
    ├── executive_summary.txt        # Executive report
    ├── integrated_data.csv          # Merged dataset
    └── vessel_metrics.csv           # Calculated metrics
```

## Core Components

### 1. Main Application (app.py)
- **Class:** InteractiveApp
- **Purpose:** Provides a user-friendly command-line interface for orchestrating the entire data pipeline
- **Features:**
  - Interactive menu system
  - Quick analysis workflow
  - Data loading options
  - Advanced analysis features
  - Dashboard generation

### 2. Data Pipeline (core_data_pipeline.py)
- **Class:** DataPipeline
- **Purpose:** Generates synthetic data and integrates multiple data sources
- **Capabilities:**
  - Generate synthetic vessel specifications
  - Create navigation logs
  - Generate environmental records
  - Generate fuel consumption data
  - Generate maintenance incident records
  - Merge all data sources into integrated dataset

### 3. Analytics Engine (analytics_engine.py)
- **Class:** AnalyticsEngine
- **Purpose:** Calculates performance metrics, risk assessments, and provides analytical insights
- **Metrics Include:**
  - Fuel efficiency metrics
  - Operational performance indicators
  - Engine performance analysis
  - Environmental impact assessment
  - Maintenance pattern analysis
  - Risk assessment and scoring

### 4. Output Manager (output_manager.py)
- **Class:** OutputManager
- **Purpose:** Validates data quality and generates multi-format reports
- **Features:**
  - Data validation and quality checks
  - Multi-format reporting (CSV, PDF, Excel)
  - Executive summaries
  - Detailed analytical reports
  - Visualization generation

## Technical Stack

### Dependencies
- **pandas (2.0.3)** - Data manipulation and analysis
- **numpy (1.24.3)** - Numerical computing
- **matplotlib (3.7.2)** - Data visualization
- **seaborn (0.12.2)** - Statistical visualization
- **plotly (5.16.1)** - Interactive visualizations
- **folium (0.14.0)** - Geographic mapping
- **geopandas (0.13.2)** - Geospatial data analysis
- **streamlit (1.27.0)** - Interactive dashboard framework
- **scikit-learn (1.3.0)** - Machine learning utilities
- **reportlab (4.0.4)** - PDF report generation
- **openpyxl (3.1.2)** - Excel file handling

### Python Version
- Python 3.8 or higher recommended

## Installation and Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
python -c "import pandas; print('Installation successful')"
```

## Running the Application

### Starting the Interactive Application
```bash
python app.py
```

This launches the main menu with the following options:

1. **Quick Analysis** - Automatically generates data, performs analysis, and generates reports
2. **Load Your Own Data** - Loads external CSV files for analysis
3. **Advanced Options** - Access specialized analysis features
4. **Launch Dashboard** - Starts the interactive Streamlit dashboard
5. **Exit** - Close the application

### Quick Analysis Workflow
The quick analysis option performs the following steps automatically:
1. Generates 50 vessels with 5000 navigation records
2. Creates environmental, fuel, and maintenance datasets
3. Integrates all data sources
4. Calculates comprehensive metrics
5. Validates data quality
6. Generates reports in multiple formats

## Output Files

The application generates the following output files in the `output/` directory:

1. **integrated_data.csv** - Complete merged dataset with all records
2. **vessel_metrics.csv** - Calculated performance metrics for each vessel
3. **data_summary.csv** - Summary statistics and aggregate metrics
4. **executive_summary.txt** - High-level analysis summary for stakeholders
5. **visualizations/** - Generated charts and graphs (if visualization enabled)

## Key Features

### Data Integration
- Seamlessly combines vessel specifications, navigation logs, environmental data, fuel consumption, and maintenance records
- Maintains referential integrity across datasets
- Handles missing data appropriately

### Performance Metrics
- Fuel efficiency per vessel
- Operational speed and utilization rates
- Engine performance indicators
- Environmental compliance metrics
- Maintenance cost trends

### Risk Assessment
- Identifies high-risk vessels based on multiple factors
- Calculates maintenance urgency scores
- Flags environmental compliance issues
- Alerts for fuel efficiency anomalies

### Reporting
- Executive summaries for management
- Detailed technical reports for operations teams
- Visual dashboards for real-time monitoring
- Exportable data in multiple formats (CSV, PDF, Excel)

## Data Processing Flow

```
Raw Data Sources
    |
    v
Data Pipeline
    |
    +-> Validate Input
    +-> Generate/Load Data
    +-> Integrate Datasets
    |
    v
Analytics Engine
    |
    +-> Calculate Metrics
    +-> Assess Risks
    +-> Generate Insights
    |
    v
Output Manager
    |
    +-> Validate Results
    +-> Format Reports
    +-> Generate Outputs
    |
    v
Output Files & Dashboard
```

## Usage Examples

### Example 1: Quick Analysis
```
Option 1: Quick Analysis
- System generates synthetic data
- Analyzes 50 vessels
- Creates comprehensive report
- Output saved to output/ directory
```

### Example 2: Load Custom Data
```
Option 2: Load Your Own Data
- Provide paths to your CSV files
- System validates format
- Performs analysis
- Generates customized reports
```

### Example 3: Advanced Analysis
```
Option 3: Advanced Options
- Specify custom analysis parameters
- Choose specific metrics to calculate
- Select custom date ranges
- Export in preferred format
```

## Data Validation

The output manager performs comprehensive data validation including:
- Missing value detection and reporting
- Data type verification
- Range and boundary checks
- Duplicate record identification
- Referential integrity validation
- Statistical consistency checks

## Configuration

Configuration can be customized by modifying:

1. **DataPipeline parameters** in app.py:
   - `num_vessels`: Number of vessels to generate (default: 50)
   - `nav_records`: Navigation records per vessel (default: 5000)

2. **Analytics parameters** in analytics_engine.py:
   - Threshold values for risk assessment
   - Metric calculation methods
   - Visualization style preferences

3. **Output parameters** in output_manager.py:
   - Report format preferences
   - Output directory location
   - File naming conventions

## Troubleshooting

### Issue: Missing Dependencies
**Solution:** Reinstall requirements
```bash
pip install --upgrade -r requirements.txt
```

### Issue: File Not Found Errors
**Solution:** Ensure you're running from the project root directory
```bash
cd "c:\Users\yaswa\OneDrive\Desktop\Flipkart Project\Task-4"
```

### Issue: Permission Errors on Output
**Solution:** Verify write permissions on the output directory
```bash
# Windows
icacls output /grant %USERNAME%:F /T
```

### Issue: Out of Memory with Large Datasets
**Solution:** Reduce dataset size or increase system memory
- Modify `num_vessels` in app.py
- Process data in batches

## Performance Considerations

- Quick analysis with default settings takes 2-5 minutes
- Larger datasets may require more processing time
- Dashboard launch may take 30-60 seconds on first run
- Visualization generation is memory-intensive for large datasets

## Future Enhancements

Potential improvements for future versions:
- Real-time data streaming integration
- Machine learning-based predictive maintenance
- Advanced geospatial analysis
- Mobile application support
- API for external integrations
- Multi-language support
- Enhanced custom reporting options

## Support and Documentation

For issues or questions:
1. Check the troubleshooting section above
2. Review the individual module docstrings
3. Examine generated logs in the output directory
4. Refer to the interactive help within the application

## Version Information

- Application Version: 1.0
- Last Updated: January 2026
- Python Compatibility: 3.8+

## Notes

- Synthetic data generated includes realistic maritime patterns
- All timestamps use UTC for consistency
- Distance measurements are in nautical miles (nm)
- Fuel quantities are measured in liters
- Vessel IDs range from V001 to VXXX based on vessel count
- Seed value (42) ensures reproducible synthetic data generation

---

**Maritime Fleet Performance Analytics** - Comprehensive Maritime Operations Intelligence
