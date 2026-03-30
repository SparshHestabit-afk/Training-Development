
import time
import torch
import csv
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from peft import PeftModel

# ------------------------------------------------
# Configuration
# ------------------------------------------------

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
FINETUNED_PATH = "/content/week8/content/week8/adapters"
FP16_MODEL = "/content/week8/content/week8/quantized/model-fp16"

PROMPTS = [
"Explain what Docker containers are.",
"Explain Kubernetes orchestration.",
"What is machine learning in simple terms?",
"If a server processes 200 requests per minute, how many requests in 5 minutes?",
"Alice joined Google as a Data Scientist in 2022. Extract structured information."
]

RESULT_FILE = "/content/week8/content/week8/benchmarks/results.csv"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ------------------------------------------------
# Helper Functions
# ------------------------------------------------

def get_peak_vram():
  return torch.cuda.max_memory_allocated() / (1024**2)

def structured_accuracy(pred):
  if "name" in pred and "company" in pred:
    return 1
  return 0

def benchmark_model(model_name, model, tokenizer):

  results = []
  model.eval()

  for prompt in PROMPTS:

      inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

      torch.cuda.empty_cache()
      torch.cuda.reset_peak_memory_stats()

      # Warm-up
      with torch.no_grad():
          _ = model.generate(**inputs, max_new_tokens=10)

      start = time.perf_counter()

      with torch.no_grad():
          outputs = model.generate(
              **inputs,
              max_new_tokens=100
          )

      end = time.perf_counter()

      latency = end - start
      tokens_generated = outputs.shape[-1] - inputs["input_ids"].shape[-1]
      tokens_per_sec = tokens_generated / latency if latency > 0 else 0

      output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
      peak_vram = get_peak_vram()
      acc = structured_accuracy(output_text)

      results.append({
          "model": model_name,
          "prompt": prompt,
          "latency": latency,
          "tokens_per_sec": tokens_per_sec,
          "peak_vram_MB": peak_vram,
          "accuracy": acc,
          "output": output_text
      })

      print(f"\n[{model_name}] Prompt: {prompt}")
      print(f"Latency: {latency:.3f}s | Tokens/sec: {tokens_per_sec:.2f} | VRAM: {peak_vram:.2f} MB | Acc: {acc}")

  return results

# -----------------------------------------------
# Streaming Output Test
# ------------------------------------------------

def streaming_test(model, tokenizer):

  print("\n===== STREAMING OUTPUT TEST =====\n")

  prompt = "Explain what Docker containers are in simple terms."
  inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

  streamer = TextStreamer(tokenizer)

  with torch.no_grad():
      model.generate(
          **inputs,
          max_new_tokens=100,
          streamer=streamer
      )

# ------------------------------------------------
# Batch Inference Test
# ------------------------------------------------

def batch_inference_test(model, tokenizer):

  print("\n===== BATCH INFERENCE TEST =====\n")

  prompts = [
      "Explain Docker containers.",
      "Explain Kubernetes.",
      "Explain machine learning."
  ]

  inputs = tokenizer(prompts, return_tensors="pt", padding=True).to(DEVICE)

  with torch.no_grad():
      outputs = model.generate(
          **inputs,
          max_new_tokens=100
      )

  decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)

  for i, out in enumerate(decoded):
      print(f"\nPrompt {i+1} Output:\n{out}")

# ------------------------------------------------
# Main Execution
# ------------------------------------------------

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

print("Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
  BASE_MODEL,
  torch_dtype=torch.float16,
  device_map="auto"
)

print("Loading fine-tuned model...")
base_for_ft = AutoModelForCausalLM.from_pretrained(
  BASE_MODEL,
  torch_dtype=torch.float16,
  device_map="auto"
)

finetuned_model = PeftModel.from_pretrained(
  base_for_ft,
  FINETUNED_PATH
)

print("Loading merged FP16 model...")
fp16_model = AutoModelForCausalLM.from_pretrained(
  FP16_MODEL,
  torch_dtype=torch.float16,
  device_map="auto"
)

results = []

print("\nRunning Base Model Benchmark...")
results += benchmark_model("base_model", base_model, tokenizer)

print("\nRunning Fine-tuned Model Benchmark...")
results += benchmark_model("finetuned_model", finetuned_model, tokenizer)

print("\nRunning FP16 Model Benchmark...")
results += benchmark_model("fp16_model", fp16_model, tokenizer)

# Streaming demo

streaming_test(base_model, tokenizer)

# Batch inference demo

batch_inference_test(base_model, tokenizer)

# ------------------------------------------------
# Save CSV Results
# ------------------------------------------------

print("\nSaving benchmark results...")

os.makedirs(os.path.dirname(RESULT_FILE), exist_ok=True)

with open(RESULT_FILE, "w", newline="") as f:

  writer = csv.DictWriter(
      f,
      fieldnames=[
          "model",
          "prompt",
          "latency",
          "tokens_per_sec",
          "peak_vram_MB",
          "accuracy",
          "output"
      ]
  )

  writer.writeheader()

  for r in results:
      writer.writerow(r)

print("Benchmark completed successfully.")
