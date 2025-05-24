import os
import pandas as pd

EXCEL_DIR = 'excels'
MERGED_DIR = 'merged'
os.makedirs(MERGED_DIR, exist_ok=True)

merged_rows = []

for filename in os.listdir(EXCEL_DIR):
    if not filename.endswith('.xlsx'):
        continue

    filepath = os.path.join(EXCEL_DIR, filename)
    
    try:
        # Load Excel and read only the 'Commitments' column
        df = pd.read_excel(filepath, index_col=0)

        # Extract date from filename assuming format like: gold_table_2025-05-10.xlsx
        date_str = filename.split("_")[-1].replace(".xlsx", "")
        
        row = df['Commitments']

        merged_rows.append({
            "Date": date_str,
            ("Commercial", "Long"): row["COMM_LONG"],
            ("Commercial", "Short"): row["COMM_SHORT"],
            ("Non-Commercial", "Long"): row["NON-COMM_LONG"],
            ("Non-Commercial", "Short"): row["NON-COMM_SHORT"],
            ("Non-Reportable", "Long"): row["NONREPORT_LONG"],
            ("Non-Reportable", "Short"): row["NONREPORT_SHORT"],
        })

    except Exception as e:
        print(f"⚠️ Skipping {filename}: {e}")
        continue

# Create DataFrame with MultiIndex columns
merged_df = pd.DataFrame(merged_rows)
merged_df.sort_values("Date", inplace=True)

# Define desired column order
columns_order = [
    "Date",
    ("Commercial", "Long"), ("Commercial", "Short"),
    ("Non-Commercial", "Long"), ("Non-Commercial", "Short"),
    ("Non-Reportable", "Long"), ("Non-Reportable", "Short")
]
merged_df = merged_df[columns_order]

# Save to Excel with multi-level headers
output_path = os.path.join(MERGED_DIR, "merged_data.xlsx")
merged_df.to_excel(output_path, index=False)
print(f"✅ Merged data saved to: {output_path}")
