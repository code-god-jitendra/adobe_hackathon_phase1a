import csv

INPUT_CSV = "clean_data\candidates.csv"
OUTPUT_CSV = "candidates_cleaned.csv"

rows = []

# Read and filter rows
with open(INPUT_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        font_size = float(row['font_size'])
        body_font = float(row['body_font_size'])
        if font_size >= body_font:
            rows.append(row)

# Write cleaned rows
with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Cleaned CSV written to: {OUTPUT_CSV}")
