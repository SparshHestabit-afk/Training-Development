import json
import random

INPUT_FILE = "data/filtered_dataset.jsonl"
TRAIN_FILE = "data/train.jsonl"
VAL_FILE = "data/val.jsonl"

SPLIT_RATIO = 0.8

#--Loading the dataset--
data = []
with open(INPUT_FILE) as f:
  for line in f:
    data.append(json.loads(line))

print("Total Sample:", len(data))

#--Shuffling the dataset--
random.shuffle(data)

#--Splitting the dataset--
split_index = int(len(data) * SPLIT_RATIO)

train_data = data[:split_index]
val_data = data[split_index:]

#--Saving the training data
with open(TRAIN_FILE, "w") as f:
  for item in train_data:
    f.write(json.dumps(item)+"\n")

#--Saving the validation data
with open(VAL_FILE, "w") as f:
  for item in val_data:
    f.write(json.dumps(item)+"\n")

print("\nDataset Split Completed")
print("Split Ratio:", SPLIT_RATIO)
print("Train samples:", len(train_data))
print("Validation samples:", len(val_data))
