import os
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.cftc.gov"
START_URL = (
    f"{BASE_URL}/MarketReports/CommitmentsofTraders/HistoricalViewable/index.htm"
)

# Create the base directory
BASE_DIR = "cot_reports"
os.makedirs(BASE_DIR, exist_ok=True)

# Step 1: Load the main index page
response = requests.get(START_URL)
soup = BeautifulSoup(response.content, "html.parser")

# Step 2: Extract date links
links = soup.find_all("a", href=True)
report_links = []
for link in links:
    href = link["href"]
    text = link.get_text(strip=True)
    if (
        href.startswith("/MarketReports/CommitmentsofTraders/HistoricalViewable/cot")
        and text
    ):
        report_links.append((f"{BASE_URL}{href}", f"{href[-6:][:2]}-{href[-6:][2:4]}-{href[-6:][4:]}"))



# Step 3: Process each report link
for report_url, date_text, in report_links:
    print(f"\n🔍 Processing: {date_text} -> {report_url}")
    

    try:
        # Step 3a: Load report page
        r = requests.get(report_url)
        report_soup = BeautifulSoup(r.content, "html.parser")

        # Step 3b: Locate Legacy Commitments section
        legacy_header = report_soup.find(
            "h2", string=lambda s: s and "Legacy Commitments of Traders" in s
        )
        if not legacy_header:
            print("❌ No 'Legacy Commitments' section found.")
            continue

        # Step 3c: Find tables following the header
        tables = legacy_header.find_all_next("table")

        short_link = None

        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if not cells:
                    continue
                row_text = " ".join(cell.get_text(strip=True) for cell in cells)
                if "Commodity Exchange Incorporated" in row_text:
                    # Find the short form under Futures Only
                    for a in row.find_all("a", href=True):
                        if "short" in a.get_text(strip=True).lower():
                            short_link = BASE_URL + a["href"]
                            break
                    break
            if short_link:
                break

        if short_link:
            print(f"➡️ Found short format link: {short_link}")
            short_resp = requests.get(short_link)
            short_filename = os.path.join(BASE_DIR, f"{date_text}.html")
            with open(short_filename, "wb") as f:
                f.write(short_resp.content)
            print(f"✅ Saved: {short_filename}")
        else:
            print(
                "❌ No 'short format' link found for 'Commodity Exchange Incorporated'."
            )

        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Error on {report_url}: {e}")
