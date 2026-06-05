from lxml import etree

file_path = r"C:\GenAI\earlywatch-analyzer\samples\PRD_20101571_310094606_2026-05-11_R_EWA 1.DOC"

ns = {
    "w": "http://schemas.microsoft.com/office/word/2003/wordml"
}

tree = etree.parse(file_path)

tables = tree.xpath("//w:tbl", namespaces=ns)

print("Total tables found:", len(tables))

for table_no, table in enumerate(tables[:10], start=1):
    print("\n" + "=" * 80)
    print(f"TABLE {table_no}")
    print("=" * 80)

    rows = table.xpath(".//w:tr", namespaces=ns)

    for row in rows[:10]:
        cells = row.xpath("./w:tc", namespaces=ns)
        values = []

        for cell in cells:
            text_parts = cell.xpath(".//w:t/text()", namespaces=ns)
            cell_text = " ".join(text_parts).strip()
            values.append(cell_text)

        print(" | ".join(values))