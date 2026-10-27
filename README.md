# 🧹 Data Cleaning Workbench

An interactive data cleaning and data quality analysis application built using Python, Pandas, NumPy, and Streamlit.

**Clean, analyze, validate, and export datasets through an easy-to-use web interface.**

<p align="center">
  <a href="https://data-cleaning-workbench-wyo3wdy3wnqcox2ata7vws.streamlit.app/">
    <img src="https://img.shields.io/badge/Live%20Demo-Open%20App-brightgreen?style=for-the-badge&logo=streamlit" alt="Live Demo"/>
  </a>
  <a href="https://github.com/Ashutosh-dutta07/data-cleaning-workbench">
    <img src="https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github" alt="GitHub Repository"/>
  </a>
</p>

## 🚀 Live Demo

**Try the application here:**

👉 https://data-cleaning-workbench-wyo3wdy3wnqcox2ata7vws.streamlit.app/

Upload your own CSV or Excel dataset and explore the available data cleaning and quality analysis features.

## 📌 Project Overview

Data Cleaning Workbench is a Python-based data analytics project designed to simplify common data preprocessing tasks.

It helps users identify data quality issues, handle missing values, remove duplicates, clean text, convert data types, treat outliers, compare before-and-after results, and export cleaned datasets.

The application provides an interactive interface so users can perform these operations without writing cleaning code manually.

## ✨ Features

### 📁 Dataset Upload & Overview
- Upload CSV and Excel files (`.csv`, `.xlsx`, `.xls`)
- Preview uploaded datasets
- View row and column counts
- Inspect column data types and unique values

### 🔎 Data Quality Analysis
- Missing-value counts and percentages
- Duplicate-row detection
- Data type inspection
- Unique-value analysis
- Descriptive statistics for numeric columns

### 🧹 Data Cleaning
- Remove duplicate rows
- Handle missing values using:
  - Drop rows
  - Mean
  - Median
  - Mode
  - Custom values
- Clean text by trimming whitespace and converting case
- Convert columns to string, integer, float, or datetime
- Rename columns
- Remove unwanted columns
- Detect and remove constant columns
- Detect and treat outliers using the Interquartile Range (IQR) method
- Remove outlier rows or cap values to IQR limits

### 📊 Before vs After Analysis
- Compare row and column counts
- Compare missing values and duplicate rows
- Review cleaning operation logs
- Preview the cleaned dataset

### 📤 Export
- Download cleaned datasets as CSV
- Download cleaned datasets as Excel
- View and download a data quality report
- Review the cleaning pipeline log

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Pandas | Data manipulation and cleaning |
| NumPy | Numerical operations |
| Streamlit | Interactive web interface |
| openpyxl | Excel file processing |

## 📂 Project Structure

```text
data-cleaning-workbench/
├── app.py
├── requirements.txt
├── sample_uncleaned_data.csv
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ashutosh-dutta07/data-cleaning-workbench.git
cd data-cleaning-workbench
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## 📖 How to Use

1. Open the [Live Demo](https://data-cleaning-workbench-wyo3wdy3wnqcox2ata7vws.streamlit.app/).
2. Upload a CSV or Excel dataset.
3. Review the dataset overview and data quality report.
4. Choose a cleaning operation from the sidebar.
5. Select the required column and cleaning strategy.
6. Apply the operation and review the updated dataset.
7. Compare before-and-after metrics.
8. Download the cleaned dataset and data quality report.

## 🎯 Project Objectives

- Simplify common data cleaning operations.
- Identify missing values, duplicates, and potential outliers.
- Improve dataset quality through interactive preprocessing.
- Demonstrate practical Python and data analytics skills.
- Provide downloadable cleaned datasets and quality reports.

## 🔮 Future Enhancements

- Automated data quality recommendations
- Interactive data visualizations
- Multi-column cleaning operations
- Undo and reset cleaning operations
- Advanced data validation rules

## 👨‍💻 Author

**Ashutosh Kumar**

- GitHub: [Ashutosh-dutta07](https://github.com/Ashutosh-dutta07)
- Project Repository: [Data Cleaning Workbench](https://github.com/Ashutosh-dutta07/data-cleaning-workbench)
- Live Demo: [Open Application](https://data-cleaning-workbench-wyo3wdy3wnqcox2ata7vws.streamlit.app/)

---

*Built with Python, Pandas, NumPy, and Streamlit.*
