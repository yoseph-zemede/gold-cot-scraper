import re
import os
import pandas as pd
from datetime import datetime

SOURCE_DIR = 'cot_reports'
OUTPUT_DIR = 'excels'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Helper to parse numbers
def parse_numbers(line):
    numbers = re.findall(r"-?\d[\d,]*\.?\d*", line)
    return [float(n.replace(",", "")) if '.' in n else int(n.replace(",", "")) for n in numbers]

# Column headers
columns = [
    "NON-COMM_LONG", "NON-COMM_SHORT", "SPREADS",
    "COMM_LONG", "COMM_SHORT", "TOTAL_LONG", "TOTAL_SHORT",
    "NONREPORT_LONG", "NONREPORT_SHORT"
]

# Patterns for labeled lines
labels = {
    "COMMITMENTS": r"^COMMITMENTS",
    "CHANGES": r"^CHANGES FROM",
    "PERCENTAGE": r"^PERCENT OF OPEN INTEREST",
    "TRADERS": r"^NUMBER OF TRADERS"
}

# Process each HTML file
for filename in os.listdir(SOURCE_DIR):
    if not filename.endswith('.html'):
        continue

    filepath = os.path.join(SOURCE_DIR, filename)

    with open(filepath, "r", encoding="iso-8859-1") as file:
        html = file.read()

    match = re.search(r"<pre[^>]*>(.*?)</pre>", html, re.DOTALL)
    if not match:
        print(f"⚠️ Skipping {filename}: <pre> tag not found.")
        continue

    pre_content = match.group(1)

    gold_match = re.search(
        r"GOLD - COMMODITY EXCHANGE INC\..*?(?=\n[A-Z ]+ - COMMODITY EXCHANGE INC\.|<!--/ih:includeHTML-->)",
        pre_content,
        re.DOTALL
    )

    if not gold_match:
        print(f"⚠️ Skipping {filename}: Gold section not found.")
        continue

    gold_text = gold_match.group(0).strip()
    lines = gold_text.splitlines()

    try:
        date_line = next(line for line in lines if "FUTURES ONLY POSITIONS AS OF" in line)
        date_match = re.search(r"AS OF (\d{2}/\d{2}/\d{2})", date_line)
        if not date_match:
            raise ValueError("Date not found.")
        raw_date = date_match.group(1)
        report_date = datetime.strptime(raw_date, "%m/%d/%y").strftime("%Y-%m-%d")
    except Exception as e:
        print(f"⚠️ Skipping {filename}: {e}")
        continue

    data_lines = {}
    for label, pattern in labels.items():
        for i, line in enumerate(lines):
            if re.match(pattern, line.strip()):
                data_lines[label] = lines[i + 1]  # actual data is next line
                break

    df = pd.DataFrame(index=columns)
    try:
        for label, raw_line in data_lines.items():
            values = parse_numbers(raw_line)
            if label == "TRADERS":
                values += [float("nan")] * 2  # pad with NaNs
            if len(values) != len(columns):
                raise ValueError(f"{label} row has {len(values)} values, expected {len(columns)}")
            df[label.title()] = values
    except Exception as e:
        print(f"⚠️ Skipping {filename}: {e}")
        continue

    output_filename = os.path.splitext(filename)[0] + ".xlsx"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    df.to_excel(output_path, sheet_name="Gold")
    print(f"✅ Exported: {output_path}")
    