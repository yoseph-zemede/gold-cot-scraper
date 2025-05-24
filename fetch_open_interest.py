import os
import re
import pandas as pd

SOURCE_DIR = 'cot_reports'
OUTPUT_FILE = 'gold_open_interest.xlsx'

records = []

for filename in os.listdir(SOURCE_DIR):
    if not filename.endswith('.html'):
        continue

    # Get date string from filename (remove .html extension)
    date_str = os.path.splitext(filename)[0]

    filepath = os.path.join(SOURCE_DIR, filename)
    with open(filepath, "r", encoding="iso-8859-1") as file:
        html = file.read()

    # Extract content inside <pre> tags
    match = re.search(r"<pre[^>]*>(.*?)</pre>", html, re.DOTALL)
    if not match:
        print(f"⚠️ Skipping {filename}: <pre> tag not found.")
        continue

    pre_content = match.group(1)

    # Extract Gold section
    gold_match = re.search(
        r"GOLD - COMMODITY EXCHANGE INC\..*?(?=\n[A-Z ]+ - COMMODITY EXCHANGE INC\.|<!--/ih:includeHTML-->)",
        pre_content,
        re.DOTALL
    )
    if not gold_match:
        print(f"⚠️ Skipping {filename}: Gold section not found.")
        continue

    gold_text = gold_match.group(0)

    # Extract Open Interest
    try:
        oi_match = re.search(r"OPEN INTEREST:\s+([\d,]+)", gold_text)
        open_interest = int(oi_match.group(1).replace(",", ""))
    except Exception as e:
        print(f"⚠️ Skipping {filename}: Open Interest parsing error - {e}")
        continue

    records.append((date_str, open_interest))

# Sort and save to Excel
if records:
    df = pd.DataFrame(records, columns=["Date", "Open Interest"])
    df.sort_values("Date", inplace=True)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ All Open Interest data saved to: {OUTPUT_FILE}")
else:
    print("⚠️ No valid data was extracted.")
