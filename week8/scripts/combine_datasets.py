import json

files = [
    "data/qa_dataset.jsonl",
    "data/reasoning_dataset.jsonl",
    "data/extraction_dataset.jsonl"
]

combined = []

for file in files:
  with open(file) as f:
    for line in f:
      item = json.loads(line)

      prompt = f"""### Instruction: {item['instruction']}

### Input: {item['input']}

###  Output: {item['output']}
"""

      combined.append({"text": prompt})

with open("data/combined_dataset.jsonl", "w") as f:
  for item in combined:
    f.write(json.dumps(item)+"\n")

print("Combined Dataset Created")
print("Total Samples:", len(combined))
