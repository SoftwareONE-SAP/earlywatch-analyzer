from lxml import etree

file_path = r"C:\GenAI\earlywatch-analyzer\samples\PRD_20101571_310094606_2026-05-11_R_EWA 1.DOC"

ns = {
    "w": "http://schemas.microsoft.com/office/word/2003/wordml"
}

tree = etree.parse(file_path)

# Extract all visible text
texts = tree.xpath("//w:t/text()", namespaces=ns)

print("Total text fragments found:", len(texts))
print("\nFirst 50 text fragments:\n")

for t in texts[:50]:
    print(t)