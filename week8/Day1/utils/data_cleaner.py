import json
import re

INPUT_FILE = "data/combined_dataset.jsonl"
OUTPUT_FILE = "data/cleaned_dataset.jsonl"

def normalize_text(text):
  text = text.strip()
  text = re.sub(r"\n+", "\n", text)
  text = re.sub(r"\s+", " ", text)
  return text

def valid_format(text):
  return (
      "### Instruction:" in text and
      "### Input:" in text and
      "### Output:" in text
  )

def clean_dataset():
  seen = set()
  cleaned = []

  duplicates = 0
  invalid = 0

  with open(INPUT_FILE) as f:
    for line in f:
      try:
        item = json.loads(line)
      except:
        invalid += 1
        continue

      text = normalize_text(item.get("text", ""))

      if not valid_format(text):
        invalid += 1
        continue

      if text in seen:
        duplicates += 1
        continue

      seen.add(text)
      cleaned.append({"text": text })

  with open(OUTPUT_FILE, "w") as f:
    for row in cleaned:
      f.write(json.dumps(row)+"\n")

  print("Cleaning completed")
  print("Final Samples:", len(cleaned))
  print("Duplicates Removed:", duplicates)
  print("Invalid Removed:", invalid)

if __name__ == "__main__":
  clean_dataset()
