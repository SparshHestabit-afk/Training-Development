                                    Hestabit Training Development
                                        Week 7 - Day 5

# Deployment Notes — Enterprise GenAI RAG System

## 1. Overview

This document outlines the deployment architecture, configuration strategy, and operational workflow of the **Enterprise Knowledge Intelligence System** developed during Week-7 of the GenAI Engineering module. The system integrates multiple Retrieval-Augmented Generation (RAG) components to enable intelligent querying over heterogeneous enterprise data sources including documents, images, and structured databases.

The objective of this deployment layer is to expose the RAG capabilities through a clean, production-oriented interface while ensuring extensibility, traceability, and reliability.

The deployed system supports three primary interaction modes:

* **Text-based document question answering**
* **Image understanding and similarity retrieval**
* **Natural language to SQL querying**

These capabilities are delivered through REST API endpoints powered by **FastAPI**, allowing the platform to function as a modular backend service.

---

## 2. Deployment Architecture

The system follows a modular architecture in which each major capability (text retrieval, image reasoning, SQL querying) is implemented as an independent pipeline. These pipelines are coordinated through an API layer that manages requests, context assembly, model inference, and evaluation.

High-level flow:
```
User Request → API Endpoint → Query Router → Retrieval Pipeline → Context Builder → LLM Generation → Evaluation → Response
```
Key architectural components include:

* **API Layer:** FastAPI service exposing system endpoints
* **Retriever Layer:** Hybrid retrieval engine combining semantic search and keyword matching
* **Generator Layer:** Local or hosted LLM used to produce final responses
* **Evaluation Layer:** Faithfulness and hallucination detection module
* **Memory Layer:** Short-term conversational memory for contextual continuity
* **Logging System:** Persistent storage of user interactions for debugging and analysis

This layered approach ensures that each component can evolve independently without affecting the rest of the system.

---

## 3. API Service

The API is implemented using **FastAPI**, chosen for its performance, asynchronous capabilities, and automatic documentation generation.

The following endpoints are exposed:
```
`/ask`
```
Handles document-based queries.
The request is processed through the hybrid retriever, relevant context is constructed, and the language model generates a response.

Typical workflow:

1. User submits a question
2. System retrieves relevant document chunks
3. Context is assembled
4. LLM generates an answer
5. Evaluation module checks answer faithfulness
6. Memory and logs are updated

---

```
`/ask-image`
```

Processes image-related queries.
The system retrieves visually similar images using CLIP embeddings and returns associated metadata including captions and OCR content.

This endpoint supports:

* Diagram retrieval
* Image similarity search
* Visual document understanding

---

```
`/ask-sql`
```
Enables natural language querying of structured datasets.
The system converts a user question into SQL using the language model, validates the generated query, executes it against the PostgreSQL database, and returns summarized results.

Safety mechanisms include:

* SQL query validation
* restriction to SELECT operations
* injection prevention

---

## 4. Model Configuration Strategy

A **provider-switch configuration** is used to support both local and cloud-hosted language models without altering the main pipeline logic.

Configuration is defined in:

```
src/config/model.yaml
```

Example configuration:

```
provider: local
model_name: llama3.2
api_key_env: GOOGLE_API_KEY
```

Supported providers:

| Provider |     Model Source       |
| -------- | ---------------------- |
| Local    | Ollama llama3.2 model  |
| Online   | Gemini API             |

This design ensures that the same application can run in:

* fully offline environments
* enterprise controlled deployments
* cloud assisted inference mode

---

## 5. Conversational Memory

The system implements a lightweight memory mechanism that stores the **last five user interactions**.

Purpose of memory:

* preserve conversational continuity
* provide context for follow-up questions
* improve response relevance

Memory is maintained in a deque structure and injected into prompts before model inference.

Example memory structure:

```
User: Explain credit underwriting
Assistant: Credit underwriting refers to...
```

This information is appended to the prompt during response generation.

---

## 6. Logging and Traceability

All interactions are recorded in:

```
CHAT-LOGS.json
```

Each entry contains:

* timestamp
* user query
* generated response

Example entry:

```
{
  "timestamp": "2026-03-09T16:40:21",
  "query": "Explain credit underwriting",
  "answer": "Credit underwriting is..."
}
```

Logging provides several operational advantages:

* debugging failed queries
* evaluating model behaviour
* collecting feedback for system improvement

---

## 7. Evaluation and Hallucination Detection

To improve reliability, the system includes a **RAG evaluation module**.

Two evaluation metrics are computed:

### Faithfulness Score

Measures semantic similarity between:

* retrieved context
* generated answer

Scores closer to **1.0** indicate strong grounding in source documents.

---

### Hallucination Detection

If the similarity score falls below a defined threshold, the system flags the answer as potentially hallucinated.

Example response structure:

```
{
 "answer": "...",
 "faithfulness_score": 0.72,
 "hallucination": false
}
```

This mechanism helps identify responses that may not be adequately supported by retrieved evidence.

---

## 8. Deployment Execution

To start the API server:

```
uvicorn src.deployment.app:app --reload
```

The interactive API documentation is automatically generated and accessible at:

```
http://127.0.0.1:8000/docs
```

This interface allows testing of all endpoints directly through the browser.

---

## 9. Operational Considerations

When deploying the system in a production environment, the following considerations should be addressed:

### Model Hosting

Local deployment using Ollama ensures:

* privacy
* low latency
* independence from external APIs

However, cloud models may offer stronger reasoning capabilities depending on the use case.

---

### Scaling

FastAPI services can be scaled using:

* containerization (Docker)
* reverse proxies (NGINX)
* orchestration frameworks (Kubernetes)

---

### Monitoring

Operational monitoring may include:

* request latency tracking
* evaluation score distribution
* system error logs

Such monitoring is useful for identifying performance bottlenecks and model drift.

---
