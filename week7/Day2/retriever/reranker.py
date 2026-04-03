import os
import json
import numpy as np
import faiss

from sentence_transformers import CrossEncoder, SentenceTransformer

CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

class Reranker:

    def __init__(self, lambda_param=0.6):

        self.cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

        self.lambda_param = lambda_param

    # ----------------------------------------
    # Cross Encoder Reranking
    # ----------------------------------------

    def cross_encoder_rerank(self, query, documents):

        if not documents:
            return documents

        doc_texts = [doc["text"] for doc in documents]

        pairs = [[query, text] for text in doc_texts]

        scores = self.cross_encoder.predict(pairs)

        for doc, score in zip(documents, scores):
            doc["rerank_score"] = float(score)

        ranked_docs = sorted(
            documents,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return ranked_docs


    # ----------------------------------------
    # Max Marginal Relevance
    # ----------------------------------------

    def mmr(self, query, documents, top_k):

        if len(documents) <= top_k:
            return documents

        doc_texts = [doc["text"] for doc in documents]

        doc_embeddings = self.embedder.encode(doc_texts)
        query_embedding = self.embedder.encode([query])[0]

        selected = []
        selected_indices = []

        candidate_indices = list(range(len(documents)))

        similarity_to_query = np.dot(doc_embeddings, query_embedding)

        first_idx = int(np.argmax(similarity_to_query))

        selected.append(documents[first_idx])
        selected_indices.append(first_idx)

        candidate_indices.remove(first_idx)

        while len(selected) < top_k and candidate_indices:

            mmr_scores = []

            for idx in candidate_indices:

                relevance = similarity_to_query[idx]

                diversity = max(
                    np.dot(doc_embeddings[idx], doc_embeddings[j])
                    for j in selected_indices
                )

                mmr_score = (
                    self.lambda_param * relevance
                    - (1 - self.lambda_param) * diversity
                )

                mmr_scores.append((mmr_score, idx))

            _, best_idx = max(mmr_scores)

            selected.append(documents[best_idx])
            selected_indices.append(best_idx)

            candidate_indices.remove(best_idx)

        return selected


    # ----------------------------------------
    # Full Reranking Pipeline
    # ----------------------------------------

    def rerank(self, query, documents, top_k=5):

        ranked_docs = self.cross_encoder_rerank(query, documents)

        diversified_docs = self.mmr(query, ranked_docs, top_k)

        return diversified_docs