# CFTC Gold Report Scraper & Analyzer

This project automates the extraction and analysis of **Gold futures position data** from the U.S. CFTC (Commodity Futures Trading Commission) "Commitments of Traders" reports.

## 🧠 What It Does

- 📥 **Scrapes** all CMX (COMEX) futures-only reports from **2005 to 2025**.
- 🔍 **Extracts only the GOLD** section from each `.html` report.
- 📊 **Exports each report** as a clean Excel table.
- 📚 **Combines** all data into a single Excel file for historical analysis.

## 📂 File Structure

- `cot-reports/` — Raw downloaded HTML reports
- `excels/` — Excel files per date 
- `merged/` — merged master file
- `fetch_pages.py` — Downloads all reports and Extracts gold tables from raw HTML
- `convert_to_excel.py` — Converts all .html reports to excel file
- `merge.py.py` — Merge all excel files into one master excel file
- `fetch_open_interest.py` — Extracts the open interest from the gold tables and save them into one file

## 🛠️ Tech Stack

- Python 3
- `requests`, `re`, `pandas`, `openpyxl`
- Manual HTML parsing (no JS rendering required)

## 🧪 Sample Use Case

Clients can use the final Excel dataset to:

- Track historical market sentiment toward gold
- Build time-series models for price prediction
- Visualize trader positions by category

## 📌 Sample Output

| NON-COMM_LONG | COMM_SHORT | ... | DATE       |
|---------------|------------|-----|------------|
| 297316        | 404930     | ... | 2009-12-01 |
| ...           | ...        | ... | ...        |

## 📈 Try It

```bash
pip install -r requirements.txt
