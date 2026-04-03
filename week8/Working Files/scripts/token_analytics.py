import json
import pandas as pd
import matplotlib.pyplot as plt

from transformers import AutoTokenizer

MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

lengths = []

with open("data/cleaned_dataset.jsonl") as f:
  for line in f:
    item = json.loads(line)

    tokens = tokenizer.encode(item["text"])
    lengths.append(len(tokens))

df = pd.DataFrame({"token_length": lengths})

print("\nDataset Statistics")
print("-------------------")
print("Samples:", len(lengths))
print("Mean:", df.token_length.mean())
print("Median:", df.token_length.median())
print("Max:", df.token_length.max())
print("Min:", df.token_length.min())

plt.hist(df.token_length, bins=40)
plt.title("Token Length Distribution Graph")
plt.xlabel("Token Count")
plt.ylabel("Frequency")

plt.savefig("token_distribution.png")

print("\nToken Analysis completed. \nGraph saved as token_distribution.png.")
