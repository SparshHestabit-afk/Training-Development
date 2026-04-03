import json
import numpy as np

from transformers import AutoTokenizer

INPUT_FILE = "data/cleaned_dataset.jsonl"
OUTPUT_FILE = "data/filtered_dataset.jsonl"

MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

data = []
lengths = []

# Load dataset
with open(INPUT_FILE) as f:
    for line in f:
        item = json.loads(line)
        tokens = tokenizer.encode(item["text"])
        length = len(tokens)

        item["token_length"] = length
        
        data.append(item)
        lengths.append(length)

lengths = np.array(lengths)

# Compute IQR
Q1 = np.percentile(lengths, 25)
Q3 = np.percentile(lengths, 75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print("IQR Statistics")
print("----------------")
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Bound:", lower_bound)
print("Upper Bound:", upper_bound)

kept = 0
removed = 0

with open(OUTPUT_FILE, "w") as out:
    for item in data:
        length = item["token_length"]

        if lower_bound <= length <= upper_bound:
            del item["token_length"]
            out.write(json.dumps(item) + "\n")
            kept += 1
        else:
            removed += 1

print("\nFiltering Completed")
print("Kept:", kept)
print("Removed:", removed)
