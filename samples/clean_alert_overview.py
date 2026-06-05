import csv

input_csv = r"C:\GenAI\earlywatch-analyzer\samples\alert_overview.csv"
output_csv = r"C:\GenAI\earlywatch-analyzer\samples\alert_overview_clean.csv"

clean_rows = []

current_topic = None

with open(input_csv, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        topic = row["Topic"].strip()
        subtopic = row["Subtopic"].strip()

        if topic:
            current_topic = topic
            clean_rows.append({
                "Topic": current_topic,
                "Subtopic": ""
            })

        if subtopic:
            clean_rows.append({
                "Topic": current_topic,
                "Subtopic": subtopic
            })

with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Topic", "Subtopic"])
    writer.writeheader()
    writer.writerows(clean_rows)

print(f"Saved: {output_csv}")