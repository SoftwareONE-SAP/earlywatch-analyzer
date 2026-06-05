from lxml import etree
import csv

file_path = r"C:\GenAI\earlywatch-analyzer\samples\PRD_20101571_310094606_2026-05-11_R_EWA 1.DOC"
output_csv = r"C:\GenAI\earlywatch-analyzer\samples\alert_overview.csv"

ns = {
    "w": "http://schemas.microsoft.com/office/word/2003/wordml"
}

tree = etree.parse(file_path)
tables = tree.xpath("//w:tbl", namespaces=ns)

alert_table = None

for table in tables:
    table_text = " ".join(table.xpath(".//w:t/text()", namespaces=ns))

    if "Topic Rating" in table_text and "Subtopic" in table_text:
        alert_table = table
        break

if alert_table is None:
    raise Exception("Alert Overview table not found")

rows_out = []

rows = alert_table.xpath(".//w:tr", namespaces=ns)

for row in rows:
    cells = row.xpath("./w:tc", namespaces=ns)
    values = []

    for cell in cells:
        text_parts = cell.xpath(".//w:t/text()", namespaces=ns)
        cell_text = " ".join(text_parts).strip()
        values.append(cell_text)

    rows_out.append(values)

with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows_out)

print(f"Saved: {output_csv}")