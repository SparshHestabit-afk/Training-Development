import os
import json
import numpy as np
import faiss

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

VECTORSTORE_METADATA_PATH = os.path.join(VECTORSTORE_DIR, "metadata.json")
VECTORSTORE_FAISS_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")

MODEL_NAME = "all-MiniLM-L6-v2"


class HybridRetriever:

    def __init__(self, vector_weight=0.7, keyword_weight=0.3):

        self.index = faiss.read_index(VECTORSTORE_FAISS_PATH)

        with open(VECTORSTORE_METADATA_PATH, "r") as f:
            self.metadata = json.load(f)

        self.texts = [item["text"] for item in self.metadata]

        self.model = SentenceTransformer(MODEL_NAME)

        tokenized_corpus = [doc.split() for doc in self.texts]
        self.bm25 = BM25Okapi(tokenized_corpus)

        self.vector_weight = vector_weight
        self.keyword_weight = keyword_weight


    # ----------------------------------------
    # Metadata Filters
    # ----------------------------------------

    def apply_filters(self, filters):

        if not filters:
            return list(range(len(self.metadata)))

        valid_indices = []

        for idx, item in enumerate(self.metadata):

            meta = item.get("metadata", {})

            if all(str(meta.get(k)) == str(v) for k, v in filters.items()):
                valid_indices.append(idx)

        return valid_indices


    # ----------------------------------------
    # Semantic Search
    # ----------------------------------------

    def semantic_search(self, query, candidate_indices, top_k):

        query_embedding = self.model.encode([query]).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(distances[0], indices[0]):

            if idx == -1:
                continue

            if idx not in candidate_indices:
                continue

            item = dict(self.metadata[idx])

            item["vector_score"] = float(score)
            item["retrieval_method"] = "vector"

            results.append(item)

        return results


    # ----------------------------------------
    # Keyword Search
    # ----------------------------------------

    def keyword_search(self, query, candidate_indices, top_k):

        tokenized_query = query.split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked = np.argsort(scores)[::-1]

        results = []

        for idx in ranked:

            if idx not in candidate_indices:
                continue

            item = dict(self.metadata[idx])

            item["keyword_score"] = float(scores[idx])
            item["retrieval_method"] = "keyword"

            results.append(item)

            if len(results) >= top_k:
                break

        return results


    # ----------------------------------------
    # Score Normalization
    # ----------------------------------------

    def normalize_scores(self, scores):

        if not scores:
            return []

        min_score = min(scores)
        max_score = max(scores)

        if max_score - min_score == 0:
            return [1.0 for _ in scores]

        return [(score - min_score) / (max_score - min_score) for score in scores]


    # ----------------------------------------
    # Hybrid Score Fusion
    # ----------------------------------------

    def fuse_scores(self, vector_results, keyword_results):

        combined = {}

        for item in vector_results:

            key = item["text"]
            combined.setdefault(key, item)
            combined[key]["vector_score"] = item.get("vector_score", 0)

        for item in keyword_results:

            key = item["text"]
            combined.setdefault(key, item)
            combined[key]["keyword_score"] = item.get("keyword_score", 0)

        docs = list(combined.values())

        vector_scores = [doc.get("vector_score", 0) for doc in docs]
        keyword_scores = [doc.get("keyword_score", 0) for doc in docs]

        norm_vector = self.normalize_scores(vector_scores)
        norm_keyword = self.normalize_scores(keyword_scores)

        for i, doc in enumerate(docs):

            doc["vector_score_norm"] = norm_vector[i]
            doc["keyword_score_norm"] = norm_keyword[i]

            doc["hybrid_score"] = (
                self.vector_weight * norm_vector[i]
                + self.keyword_weight * norm_keyword[i]
            )

        docs.sort(key=lambda x: x["hybrid_score"], reverse=True)

        return docs


    # ----------------------------------------
    # Deduplication
    # ----------------------------------------

    def deduplicate(self, docs):

        seen = set()
        unique = []

        for doc in docs:

            text_hash = hash(doc["text"])

            if text_hash in seen:
                continue

            seen.add(text_hash)
            unique.append(doc)

        return unique


    # ----------------------------------------
    # Main Retrieval
    # ----------------------------------------

    def retrieve(self, query, top_k=10, filters=None):

        candidate_indices = self.apply_filters(filters)

        vector_results = self.semantic_search(query, candidate_indices, top_k)

        keyword_results = self.keyword_search(query, candidate_indices, top_k)

        results = self.fuse_scores(vector_results, keyword_results)

        results = self.deduplicate(results)

        if len(results) == 0:
            results = keyword_results

        return results[:top_k]
    
# ------------------------------------------------
# Pipeline Test
# ------------------------------------------------

if __name__ == "__main__":

    from src.retriever.reranker import Reranker
    from src.pipelines.context_builder import ContextBuilder

    print("\nInitializing pipeline...\n")

    retriever = HybridRetriever()
    reranker = Reranker()
    context_builder = ContextBuilder()

    query = "Explain how credit underwriting works"

    filters = {
        "type": "pdf"
    }

    print("Query:", query)
    print("Filters:", filters)

    print("\nRunning Hybrid Retrieval...\n")

    docs = retriever.retrieve(
        query=query,
        top_k=10,
        filters=filters
    )

    print(f"Retrieved {len(docs)} documents\n")

    print("Running Cross-Encoder Reranking + MMR...\n")

    reranked_docs = reranker.rerank(
        query,
        docs,
        top_k=5
    )

    print(f"Top {len(reranked_docs)} documents selected\n")

    print("Building Context...\n")

    context_output = context_builder.build(reranked_docs)

    print("======== FINAL CONTEXT + SOURCE========\n")
    print(context_output["context"])
