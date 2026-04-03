                                Hestabit Training Development
                                        Week 7 - Day 1

# RAG Architecture
## Multi-Format Semantic Retrieval System

---

## Overview

This project implements a modular backend architecture for a Retrieval-Augmented Generation (RAG) system. The current implementation focuses on establishing a reliable and scalable semantic retrieval pipeline capable of processing documents from multiple file formats.

The system is intentionally structured with clear separation between ingestion, preprocessing, embedding generation, vector indexing, and retrieval. This layered approach improves maintainability, enables independent testing of components, and allows seamless extension toward full LLM-based answer generation in future stages.

At its current stage, the system provides a production-ready semantic retrieval backbone.

---

## End-to-End Processing Flow

The architecture follows a sequential yet modular workflow:

```
Documents (.csv, .pdf, .txt, .docx)
            ↓
Raw Storage
            ↓
Text Extraction & Cleaning
            ↓
Chunking
            ↓
Embedding Generation
            ↓
FAISS Index Construction
            ↓
Semantic Retrieval
```

Each phase produces persistent artifacts, allowing reproducibility and simplifying debugging or reprocessing when required.

---

## Supported Document Formats

The ingestion layer supports both structured and unstructured sources:

* CSV (tabular data)
* PDF (document-based content)
* TXT (plain text files)
* DOCX (word documents)

This multi-format capability ensures flexibility in handling diverse data inputs without requiring format-specific system redesign.

---

## Project Structure

The project is organized to clearly separate logic from generated data:

```
src/
 ├── pipelines/
 │    └── ingest.py
 │
 ├── embeddings/
 │    └── embedder.py
 │
 ├── vectorstore/
 │    └── build_index.py
 │
 ├── retriever/
 │    └── query_engine.py
 │
data/
 ├── raw/        # Original source documents
 ├── cleaned/    # Extracted and normalized text
 └── chunks/     # Structured chunk output (chunks.json)
```

All executable logic resides inside `src/`, while the `data/` directory stores intermediate and processed artifacts. This separation keeps the repository clean and predictable.

---

## Architectural Layers

### Data Ingestion Layer

**Purpose:**
Convert multi-format documents into structured textual data suitable for downstream processing.

**Responsibilities:**

* Detect file type
* Extract textual content
* Store original files under `data/raw/`
* Normalize and clean extracted text
* Store cleaned output under `data/cleaned/`
* Split content into logically sized chunks

**Output:**
`chunks.json` stored inside `data/chunks/`

Chunking ensures that long documents are divided into manageable segments optimized for embedding and similarity search.

---

### Embedding Layer

**Purpose:**
Transform textual chunks into dense numerical vector representations.

**Responsibilities:**

* Load chunked content
* Generate embeddings
* Persist vector representations for reuse

Embedding generation is intentionally separated from index construction. This design allows:

* Rebuilding indexes without recomputing embeddings
* Switching vector databases if required
* Running controlled experiments on retrieval performance

---

### Vector Store Layer

**Purpose:**
Enable efficient similarity-based search over document embeddings.

**Responsibilities:**

* Load stored embeddings
* Construct FAISS index
* Maintain mapping between vectors and metadata

The FAISS index provides high-performance nearest-neighbor search, enabling scalable semantic retrieval even as document volume increases.

---

### Retrieval Layer

**Purpose:**
Perform semantic search based on user queries.

**Responsibilities:**

* Accept user query
* Convert query to embedding
* Execute similarity search
* Return top-k relevant document chunks

At this stage, the system returns semantically relevant context. Integration with a language model for response generation is planned as a subsequent enhancement.

---

## Core Design Principles

### Modularity

Each processing stage is independent:

* Ingestion
* Cleaning
* Chunking
* Embedding
* Indexing
* Retrieval

This isolation improves clarity and reduces cross-component dependency.

---

### Reproducibility

All intermediate artifacts are stored persistently under the `data/` directory.
This allows consistent rebuilding of the retrieval system without reprocessing everything from scratch.

---

### Extensibility

The architecture is prepared for future enhancements, including:

* LLM-based answer generation
* Prompt templating layer
* Source attribution in responses
* Metadata-based filtering
* Hybrid keyword and semantic search

The current structure ensures these additions can be implemented without restructuring existing modules.

---

### Scalability

By leveraging vector indexing, the system remains efficient as the dataset grows. The design supports gradual scaling without major architectural changes.

---

## Execution Workflow

To initialize the system from scratch:

1. Run ingestion pipeline
   → Stores raw documents, cleaned text, and chunked output

2. Generate embeddings
   → Converts text chunks into vector representations

3. Build vector index
   → Creates FAISS index for similarity search

4. Execute retriever
   → Performs semantic search against indexed data

Each stage can be rerun independently when updates are made to documents or processing logic.

---

## Current Capabilities

The system currently provides:

* Multi-format document ingestion
* Text normalization and structured storage
* Logical chunk segmentation
* Separate embedding generation
* FAISS-based similarity indexing
* Functional semantic retrieval engine

This forms a solid foundation for a complete Retrieval-Augmented Generation system.

---

#### Future Roadmap

Planned improvements include:

* Integration with local or API-based language models
* Context-aware prompt construction
* Response generation with source attribution
* Performance benchmarking and optimization
* Advanced filtering mechanisms

---
