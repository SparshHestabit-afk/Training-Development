# Week 8 Capstone — Local LLM API Deployment

## Overview

This project implements a **production-ready local LLM API** built using a quantized language model.
The system is optimized for **low-resource environments**, enabling efficient inference on consumer-grade hardware.

The API supports:

* Text generation
* Multi-turn chat
* Streaming responses
* Configurable sampling parameters

This solution is designed to be **RAG-ready** and easily integrable into agent-based systems.

---

## Objectives

* Deploy a fine-tuned LLM as a local microservice
* Optimize inference using quantized models
* Implement scalable and modular API architecture
* Enable real-time and batch inference capabilities

---

## Model Details

| Component        | Description              |
| ---------------- | ------------------------ |
| Base Model       | TinyLlama 1.1B Chat      |
| Fine-tuning      | LoRA / QLoRA             |
| Quantization     | 4-bit / GGUF             |
| Inference Engine | Transformers + llama.cpp |

---

##  Project Structure

```
deploy/
│
├── app.py              # FastAPI server
├── model_loader.py     # Model initialization & caching
├── config.py           # Configurations (paths, params)
│
├── ../quantized/       # Quantized models (INT4 / GGUF)
├── ../adapters/        # LoRA adapters
├── ../benchmarks/      # Benchmark results
```

---

##  Features

###  Core API Endpoints

#### 1. POST `/generate`

* Single prompt text generation
* Stateless response

#### 2. POST `/chat`

* Multi-turn conversation
* Maintains chat history

---

### Inference Features

* Quantized model inference (INT4 / GGUF)
* Token streaming support
* Batch inference capability
* Low-latency response

---

### Sampling Controls

* `temperature` — controls randomness
* `top_k` — limits candidate tokens
* `top_p` — nucleus sampling

---

### System Capabilities

* Infinite chat mode
* System + user prompt handling
* Request logging with unique IDs
* Model caching for faster responses

---

## API Usage

### 🔹 Generate Endpoint

```bash
POST /generate
```

#### Request Body

```json
{
  "prompt": "Explain Docker containers",
  "max_tokens": 100,
  "temperature": 0.7,
  "top_p": 0.9
}
```

---

### 🔹 Chat Endpoint

```bash
POST /chat
```

#### Request Body

```json
{
  "message": "What is Kubernetes?",
  "history": [],
  "temperature": 0.7
}
```

---

## Installation & Setup

### 1. Clone Repository

```bash
git clone <repo-url>
cd week8-project
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run Server

```bash
uvicorn deploy.app:app --host 0.0.0.0 --port 8000
```

---

## Benchmark Insights

The system has been tested across multiple model formats:

| Model Type | Speed         | Memory | Accuracy    |
| ---------- | ------------- | ------ | ----------- |
| FP16       | Slow          | High   | High        |
| INT8       | Medium        | Medium | High        |
| INT4       | Fast          | Low    | Slight drop |
| GGUF       | Fastest (CPU) | Lowest | Slight drop |

---

## Production Considerations

* Use **GGUF models** for CPU deployment
* Use **INT4 models** for GPU-constrained environments
* Enable batching for high-throughput systems
* Add caching layer for repeated queries

---

## Future Improvements

* Integrate with vector database for RAG
* Add authentication layer
* Deploy via Docker / Kubernetes
* Build UI (Streamlit / React)

---

## Optional Add-ons

* Dockerfile for containerization
* CLI interface for local usage
* Streamlit UI for interactive demo

---

## Conclusion

This project demonstrates a complete pipeline from:

* Model fine-tuning
* Quantization
* Optimization
* Deployment

It provides a strong foundation for building **scalable LLM-powered applications**.

---

