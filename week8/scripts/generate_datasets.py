import json
import random

TARGET_SIZE = 1000

#-QA Dataset-
qa_topics = {
"Docker": "Docker is a platform that runs applications inside containers.",
"Kubernetes": "Kubernetes manages containerized applications across clusters.",
"Git": "Git is a version control system used to track code changes.",
"Machine Learning": "Machine learning allows computers to learn patterns from data.",
"Python": "Python is a programming language used in AI, automation and web development.",
"Databases": "A database stores structured information for easy retrieval.",
"Cloud Computing": "Cloud computing provides computing services over the internet.",
"Neural Networks": "Neural networks are AI models inspired by the human brain."
}

qa_templates = [
"What is {}?",
"Explain {}.",
"Describe {} in simple terms.",
"What is the purpose of {}?",
"How does {} work?"
]

#-Reasoning Dataset-
def generate_reasoning():
  a = random.randint(50,300)
  b = random.randint(2,15)

  return {
      "instruction": "Solve step by step",
      "input": f"If a server processes {a} requests per minute, how many requests in {b} minutes?",
      "output": f"Requests per minute = {a}. Time = {b} minutes. Total = {a*b} requests."
  }

#-Extraction Dataset-
names = ["Alice", "Bob", "Charlie", "Alpha", "Delta", "David", "Emma", "Johnny", "Joey"]
companies = ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Hestabit"]
roles = ["Software Engineer", "Data Scientist", "Product Manager", "ML Engineer", "Human Resource Manager"]

def generate_extraction():
  name = random.choice(names)
  company = random.choice(companies)
  role = random.choice(roles)
  year = random.randint(2019, 2026)

  text = f"{name} joined {company} as a {role} in {year}."

  return {
      "instruction": "Extract structired information from the text",
      "input": text,
      "output": {
          "name": name,
          "company": company,
          "role": role,
          "year": year
      }
  }

#-----Saving Function--
def save_jsonl(data, filename):
  with open(filename, "w") as f:
    for item in data:
      f.write(json.dumps(item)+"\n")

#---Generating Data---
qa_dataset = []

for _ in range(TARGET_SIZE):
    topic, answer = random.choice(list(qa_topics.items()))
    template = random.choice(qa_templates)

    question = template.format(topic)

    qa_dataset.append({
        "instruction": "Answer the question",
        "input": question,
        "output": answer
    })

reasoning_dataset = [generate_reasoning() for _ in range(TARGET_SIZE)]
extraction_dataset = [generate_extraction() for _ in range(TARGET_SIZE)]

save_jsonl(qa_dataset, "data/qa_dataset.jsonl")
save_jsonl(reasoning_dataset, "data/reasoning_dataset.jsonl")
save_jsonl(extraction_dataset, "data/extraction_dataset.jsonl")

print("Datasets generated successfully")
