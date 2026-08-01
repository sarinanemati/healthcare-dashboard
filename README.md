# Healthcare Analytical Dashboard

An interactive, production-ready web application built with **Streamlit**, **pandas** and **Plotly** for analyzing, visualizing, and filtering healthcare dataset from kaggle(link: https://www.kaggle.com/datasets/prasad22/healthcare-dataset). This tool allows healthcare administrators and data analysts to track patient admission trends, billing analytics, and hospital operational efficiency using side bar filters and plotly charts in real time, with the added capability of exporting dynamically generated PDF reports.

## 🚀 Key Features

- **Automated Age Grouping (Age Binning):** Automatically categorizes patient ages into standard clinical age brackets (`0-18`, `19-30`, etc.) for more structured statistical analysis.
- **Key Performance Indicators (KPIs):** Real-time tracking of critical metrics:
  - Total Patient Count
  - Average Billing Amount
  - Average Length of Stay
  - Active Hospital Count
- **Dynamic Multi-select Filtering:** Sidebar filters that instantly slice data by Gender, Medical Condition, Insurance Provider, and Admission Type.
- **Rich Plotly Visualizations:**
  - **Bar Chart:** Average billing amount segmented by medical condition.
  - **Pie Chart:** Distribution of admission types (e.g., Emergency, Elective, Urgent).
  - **Grouped Bar Charts:** Test result distribution segmented by age groups and gender.
  - **Horizontal Bar Chart:** Top 15 hospitals by average length of stay.
  - **Bar Chart:** Comparative billing analysis across insurance providers.
- **On-the-fly PDF Report Generation:** Creates and downloads an on-demand PDF report containing key metrics and a preview of the filtered dataset using the **ReportLab** library.
- **Interactive Data Table:** A searchable preview of the top 50 rows of the filtered dataset.

##  Installation & Setup

To run this project locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/healthcare-dashboard.git
cd healthcare-dashboard
### 2. Create a Virtual Environment using .venv
It is recommended to use a virtual environment to manage dependencies:
```
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS and Linux
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
Install the required packages using pip:
```bash
pip install streamlit pandas plotly reportlab
```
### 4. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```
Your default web browser should open automatically. If not, navigate to http://localhost:8501.

## Data Schema
By default, the application reads a CSV file named healthcare_dataset.csv. The input file must contain the following columns:

Name: Patient’s full name.
Age: Patient’s age (numeric).
Gender: Gender (e.g., Male / Female).
Medical Condition: Diagnosed medical condition.
Hospital: Admitting hospital name.
Insurance Provider: Patient’s health insurance provider.
Billing Amount: Total bill charged (numeric).
Admission Type: Type of admission (Emergency, Elective, Urgent).
Date of Admission: Admission date (datetime format).
Discharge Date: Discharge date (datetime format).
Test Results: Laboratory test outcome (Normal, Abnormal, Inconclusive).

## Code Architecture & Optimization
### Data Caching (@st.cache_data):
The CSV parser is cached to prevent re-reading and processing the entire dataset from scratch on every user filter interaction, boosting application response times.
### Feature Engineering:
Automated calculation of Length of Stay by subtracting the admission date from the discharge date.
Text-cleaning routines that strip trailing whitespaces from CSV column headers.
### Memory-Efficient PDF Generation:
The PDF generator writes the report to a io.BytesIO buffer rather than writing files to the host disk, ensuring stateless compatibility for cloud deployments

	
## Contributing
Contributions, issues, and feature requests are welcome!
## tutorial
Watch a comprehensive step-by-step demonstration of the project, including its features, code walkthrough, and deployment details
[Watch the Full Video Here ↗]((https://www.youtube.com/@buildwithsarina))**

<h2 align="center">
:dizzy: Ask me anything! :sparkles:<br><br>

<a href="../../issues/new">:speech_balloon: Ask a question</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a href="../../issues?q=is%3Aissue+is%3Aclosed+sort%3Aupdated-desc">:book: Read questions</a>
</h2>

